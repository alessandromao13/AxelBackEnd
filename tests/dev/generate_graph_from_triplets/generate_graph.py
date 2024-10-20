from langchain_community.graphs import NetworkxEntityGraph
from src.persistence.mongoDB import save_graph_document, get_triplet_chunks_by_user_id


def collect_triplet_chunks(user_id):
    final_triplets = []
    found_chunks = get_triplet_chunks_by_user_id(user_id)
    for chunk in found_chunks:
        for triplet in chunk['graph_piece']:
            if 'rel' in triplet and 'src' in triplet and 'dst' in triplet:
                triplet_doc = {"source": chunk['text_chunk'], "head": triplet['src'], "tail": triplet['dst'], "type": triplet['rel']}
                final_triplets.append(triplet_doc)
    return final_triplets


def generate_knowledge_graph(text, final_triplets, topic, summary, user_id=None):
    graph = NetworkxEntityGraph()
    graph_document = {"text_source": text, "user_id": "",
                      "graph_id": "", "topic": topic, "summary": summary,
                      "nodes": [], "relations": []
                      }
    for triplet in final_triplets:
        head = triplet['head']
        tail = triplet['tail']
        relation = triplet['type']
        source = triplet['source']
        if type(head) is not list and type(tail) is not list:
            graph._graph.add_node(head)
            graph._graph.add_node(tail)
            graph._graph.add_edge(head, tail, relation=relation)
            if head not in graph_document['nodes']:
                graph_document['nodes'].append(head)
            if tail not in graph_document['nodes']:
                graph_document['nodes'].append(tail)
            edge = {"head": head, "tail": tail, "relation": relation, "source": source, "usage_weight": 0.0}
            if edge not in graph_document['relations']:
                graph_document['relations'].append(edge)
            if user_id:
                graph_document['user_id'] = user_id
    print("Number of unique triplets added to the graph:", len(final_triplets))
    save_graph_document(graph_document)
    return graph

