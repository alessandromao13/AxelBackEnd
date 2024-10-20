from langchain.chains import GraphQAChain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

from src.llm.ollama_chat import OllamaChatLLM
from src.llm.ollama_prod import OllamaProdLLM
from src.persistence.mongoDB import get_graph_by_id, load_or_create_thread, \
    load_chat_history, update_current_thread
from src.services.context_retriever import build_context
from src.services.hf_triplets import chunk_text
from src.services.prompt_service import get_chat_template, get_topic_and_summary_template, \
    get_chat_template_no_context, get_triplet_production_template


def create_graph_chain(graph):
    llm = OllamaChatLLM()
    template = get_chat_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "query", "chat_history"],
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    chain = GraphQAChain.from_llm(
        llm=llm,
        prompt=prompt,
        graph=graph,
        verbose=True,
        memory=memory
    )
    return chain


def create_chain(visited_nodes):
    llm = OllamaChatLLM()
    if not visited_nodes:
        print("++++ NO VISITED NODES, JUST CHATTING")
        template = get_chat_template_no_context()
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "query", "chat_history"],
        )
    else:
        print("++++ FOUND SOME NODES")
        template = get_chat_template()
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "query", "chat_history"],
        )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def create_summarization_chain():
    llm = OllamaProdLLM()
    template = get_topic_and_summary_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def extract_llm_response(llm_result):
    return llm_result['text']


def execute_chat_request(query, context, llm_chain, history):
    print(f"INVOKING CHAIN WITH query: {query}, context: {context}")
    llm_result = llm_chain.invoke({"query": query, "context": context, "chat_history": history})
    return extract_llm_response(llm_result)


def execute_chat_system(user_query, user_id, graph_id, thread_id):
    # Thread And LLM Memory management
    current_thread_document = load_or_create_thread(thread_id, graph_id, user_id)
    chat_history = load_chat_history(current_thread_document)
    print("++ Current Thread", current_thread_document)
    print("++ Chat History", chat_history)

    # RAG Management and Context
    graph = get_graph_by_id(graph_id)
    got_context, visited_nodes, visited_edges = build_context(graph, user_query, graph_id)
    print("GOT CONTEXT", got_context)
    print("GOT VISITED NODES", visited_nodes)
    print("GOT VISITED EDGES", visited_edges)
    chain = create_chain(visited_nodes)
    # LLM Setup and execution
    print("GOT CONTEXT", got_context)
    llm_result = execute_chat_request(user_query, got_context, chain, chat_history)
    #  Memory Management
    update_current_thread(user_query, llm_result, current_thread_document)
    return {"llm_res": llm_result, "context": got_context, "nodes": visited_nodes, "edges": visited_edges,
            "thread_id": current_thread_document['thread_id']}


#  fixme chat system test
# if __name__ == '__main__':
#     print("STARTING")
#     res = execute_chat_system("What about the document? what is the general focus?", "1234", "7", "79")
#     print("+", res)
