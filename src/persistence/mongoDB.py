import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from langchain.schema import HumanMessage, AIMessage
from langchain_community.graphs import NetworkxEntityGraph
from pymongo import MongoClient

client = MongoClient("mongodb+srv://alessandromao:12345@graphragcluster.dse1t.mongodb.net/")
db = client['Axel']
graphs_coll = db['graphs']
threads_coll = db['threads']
graph_creation_coll = db['graph_creation_tmp']
failed_runs_coll = db['failed_runs']
documents_coll = db['documents']


def get_threads_by_user_id(user_id):
    try:
        result = threads_coll.find({"user_id": str(user_id)})
        print("++ FOUND THREADS", result)
        threads_list = list(result)
        if threads_list:
            return serialize_mongo_document(threads_list)
        else:
            print(f"No thread found for user {user_id}")
            return []

    except Exception as e:
        print(f"get_threads_by_user_id(user_id) - Error {e}")
    return None


def save_graph_document(graph_document):
    try:
        graph_document['graph_id'] = str(count_graph_id())
        result = graphs_coll.insert_one(graph_document)
        if result.inserted_id:
            print(f"+++ GRAPH SAVED SUCCESSFULLY WITH ID: {result.inserted_id} +++")
        else:
            print("+++ ERROR SAVING GRAPH: No ID returned +++")
    except Exception as e:
        print(f"+++ ERROR SAVING GRAPH: {str(e)} +++")


def count_graph_id():
    return graphs_coll.count_documents({})


def count_thread_id():
    return threads_coll.count_documents({})


def remove_thread_by_id(thread_id):
    threads_coll.delete_one({"thread_id": str(thread_id)})


def get_graph_by_id(graph_id):
    if graph_id:
        try:
            result = graphs_coll.find_one({"graph_id": str(graph_id)})
            if result:
                return load_graph_from_document(serialize_mongo_document(result))
            else:
                print("+++ ERROR RETRIEVING GRAPH +++")
        except Exception as e:
            print(f"+++ ERROR RETRIEVING GRAPH: {str(e)} +++")
    else:
        print(f"+++ ERROR INSERT GRAPH ID +++")


def get_context_from_graph_summary(graph_id):
    if graph_id:
        try:
            result = graphs_coll.find_one({"graph_id": str(graph_id)})
            if result:
                return ("Documents Title: \n" + result['topic'] + "\n" + "Documents Summary: \n" + result['summary']
                        + "\n")
            else:
                print("+++ ERROR RETRIEVING GRAPH +++")
        except Exception as e:
            print(f"+++ ERROR RETRIEVING GRAPH: {str(e)} +++")
    else:
        print(f"+++ ERROR INSERT GRAPH ID +++")


def get_graph_by_user_id(user_id):
    if user_id:
        try:
            results = graphs_coll.find({"user_id": user_id})
            if results:
                results = [serialize_mongo_document(result) for result in results]
                return results
            else:
                print(f"+++ ERROR RETRIEVING GRAPHS FOR USER {user_id} +++")
        except Exception as e:
            print(f"+++ ERROR RETRIEVING GRAPH: {str(e)} - User id: {user_id} +++")
    else:
        print(f"+++ ERROR INSERT USER ID +++")


def get_user_threads(user_id: str):
    try:
        threads_found = threads_coll.find({"user_id": user_id})
        return threads_found
    except Exception as e:
        print(f"+++ ERROR RETRIEVING THREADS {e} +++")
        return None


def load_graph_from_document(graph_document):
    graph = NetworkxEntityGraph()
    for node in graph_document['nodes']:
        graph._graph.add_node(node)
    for relation in graph_document['relations']:
        head = relation['head']
        tail = relation['tail']
        rel_type = relation['relation']
        graph._graph.add_edge(head, tail, relation=rel_type)
    return graph


def get_possible_entities(graph_id):
    try:
        result = graphs_coll.find_one({"graph_id": graph_id})
        if result:
            return str(result['nodes'])
    except Exception as e:
        print(f"+++ ERROR RETRIEVING NODES: {str(e)} +++")


def serialize_mongo_document(document):
    if type(document) == list:
        result = []
        for sub_doc in document:
            if '_id' in sub_doc:
                del sub_doc['_id']
            result.append(sub_doc)
        return result
    else:
        if '_id' in document:
            del document['_id']
        return document


def update_edge_usage(graph_id, edge):
    try:

        graph_to_update = graphs_coll.find_one({"graph_id": str(graph_id)})
        if graph_to_update:
            for found_edge in graph_to_update['relations']:
                if (found_edge['head'] == edge['head'] and found_edge['tail'] == edge['tail']
                        and found_edge['relation'] == edge['relation']):
                    found_edge['usage_weight'] += 1
                    graphs_coll.update_one({"graph_id": str(graph_id)}, {"$set": graph_to_update})
                    print("++ EDGE WEIGHT UPDATED SUCCESSFULLY")
        else:
            print(f"ON GRAPH FOUND WITH ID {graph_id}")

    except Exception as e:
        print(f"update_edge_usage - ERROR RETRIEVING GRAPH: {str(e)}")


# OK
def load_or_create_thread(thread_id, graph_id, user_id):
    try:
        if thread_id:
            found_thread = threads_coll.find_one({"thread_id": str(thread_id), "user_id": str(user_id)})
            return found_thread
        else:
            return create_new_thread(user_id, graph_id)
    except Exception as e:
        print(f"+++ ERROR IN THREAD LOADING {e}")

    return None


# OK
def create_new_thread(user_id, graph_id):
    created_thread_id = str(count_thread_id())
    created_thread_document = {"thread_id": created_thread_id, "user_id": str(user_id), "graph_id": str(graph_id),
                               "messages": []}
    threads_coll.insert_one(created_thread_document)
    return created_thread_document


# OK
def load_chat_history(found_thread):
    chat_history = []
    for message in found_thread['messages']:
        if message['from'] == "BOT":
            chat_history.extend(
                [
                    AIMessage(content=message['content']),
                ]
            )
        elif message['from'] == "USER":
            chat_history.extend(
                [
                    HumanMessage(content=message['content']),
                ]
            )
    return chat_history


# OK
def update_current_thread(user_query, llm_result, current_thread):
    if user_query:
        current_thread['messages'].append({"from": "USER", "content": user_query})
        threads_coll.update_one({"thread_id": str(current_thread['thread_id'])}, {"$set": current_thread})
    if llm_result:
        current_thread['messages'].append({"from": "BOT", "content": llm_result})
        threads_coll.update_one({"thread_id": str(current_thread['thread_id'])}, {"$set": current_thread})


def save_partial_graph(document, run_num, text_chunk, user_id):
    graph_creation_coll.insert_one({"user_id": user_id, "run": run_num, "text_chunk": text_chunk, "graph_piece": document})


def clear_coll():
    graph_creation_coll.delete_many({})
    failed_runs_coll.delete_many({})


def save_failed_chunk(chunk_dict, run_num):
    failed_runs_coll.insert_one({"run_num": run_num, "fail": chunk_dict})


def check_failed_chunk(run_num):
    return failed_runs_coll.find({"run_num": run_num})


def get_triplet_chunks_by_user_id(user_id):
    return graph_creation_coll.find({"user_id": user_id})


def save_user_rag_document(document_id, rag_id, user_id):
    try:
        insertion_result = documents_coll.insert_one({"document_id": document_id, "rag_id": rag_id, "user_id": user_id})
        if not insertion_result:
            print("ERROR IN DOCUMENT INSERTION")
    except Exception as e:
        print(f"+++ ERROR IN DOCUMENT INSERTION: {str(e)}")


def get_rags_by_user_id(user_id):
    try:
        user_documents = []
        results = documents_coll.find({"user_id": user_id})
        for document in results:
            user_documents.append({
                "title": document['title'],
                "rag_id": document['rag_id'],
                "document_id": document['document_id'],
                "document": get_document_by_document_id(document['document_id'], user_id)
                })

        if not results:
            print("ERROR IN DOCUMENTS RETRIEVAL")
            return None
        else:
            return user_documents
    except Exception as e:
        print(f"+++ ERROR IN DOCUMENT RETRIEVAL: {str(e)}")


def get_document_by_document_id(document_id: str, user_id: str):
    user_directory = f"../assets/pdf/{user_id}"
    if not os.path.isdir(user_directory):
        raise HTTPException(status_code=404, detail=f"User directory {user_directory} does not exist.")
    for file_name in os.listdir(user_directory):
        file_without_extension = os.path.splitext(file_name)[0]
        if file_without_extension == document_id:
            document_path = os.path.join(user_directory, file_name)
            if not os.path.isfile(document_path):
                raise HTTPException(status_code=404, detail="Document not found.")
            return FileResponse(path=document_path, media_type='application/pdf', filename=file_name)
    raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found for user {user_id}.")
