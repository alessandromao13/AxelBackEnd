from langchain_community.graphs import NetworkxEntityGraph
from src.persistence.mongoDB import save_graph_document


def make_graph(text, final_triplets, topic, summary, user_id=None):
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
