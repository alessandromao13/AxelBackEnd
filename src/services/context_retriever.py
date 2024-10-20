import re
import networkx as nx
from langchain_core.prompts import PromptTemplate

from src.llm.ollama_prod import OllamaProdLLM
from src.persistence.mongoDB import get_possible_entities, update_edge_usage, get_graph_by_id, get_context_from_graph_summary
from src.services.prompt_service import get_entity_recognition_template


def build_context(got_graph, query, graph_id):
    return build_context_from_graph(got_graph, query, graph_id)


def build_backup_context(query, used_graph_id):
    return get_context_from_graph_summary(used_graph_id)


def build_context_from_graph(got_graph, query, graph_id):
    all_triplets = []
    entities = get_entities_in_query(query, graph_id)
    print("++ Entities found in query", entities)
    if len(entities) > 0:
        for entity in entities:
            if got_graph.has_node(entity):
                got_triplets = get_entity_knowledge(entity, got_graph, graph_id)
                print("++ Got triplets", got_triplets)
                all_triplets.extend(got_triplets)
        context = "\n".join(all_triplets)
        if not entities:
            context = get_context_from_graph_summary(graph_id)
            print("++ no entities, got contex from graph summary", context)
        return context, entities, all_triplets
    else:
        context = get_context_from_graph_summary(graph_id)
        return context, None, None


def get_entities_in_query(query, graph_id):
    template = get_entity_recognition_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["user_query", "entities"],
    )
    model = OllamaProdLLM()
    chain = prompt | model
    possible_ents = get_possible_entities(graph_id)
    print("++++ POSSIBLE ENTITIES", possible_ents)
    print("++ Template ", template)
    print("++ Prompt", prompt)
    print("+++ LLM Lorading +++")
    response = chain.invoke({"user_query": query, "entities": get_possible_entities(graph_id)})
    print("+++ RES +++", response)
    entities = extract_entities(response, possible_ents)
    print("ENTITIES FOUND", entities)
    print("TYPE ENTITIES FOUND", type(entities))
    return entities


def extract_entities(response, possible_ents):
    print("extract_entities - GOT LLM RESPONSE", response)
    match = re.search(r'\[([^\]]+)\]', response)
    if match:
        items_str = match.group(1)
        items = [item.strip().strip('"').strip("'") for item in items_str.split(',')]
        print("LENGHT")
        # fixme: Attenzione a questo
        if len(items) >= 3:
            return []
        return items
    else:
        return []


def get_entity_knowledge(entity, graph, graph_id):
    results = []

    # Find all matching nodes (nodes that are equal to or contain the entity string)
    matching_nodes = [
        node for node in graph._graph.nodes
        if entity in node
    ]

    for node in matching_nodes:
        # Traverse edges where this node is the source
        for src, sink in nx.dfs_edges(graph._graph, node, depth_limit=1):
            relation = graph._graph[src][sink]["relation"]
            results.append(f"{src} {relation} {sink}")
            update_edge_usage(graph_id, {"head": src, "tail": sink, "relation": relation})

        # Traverse predecessors of the node
        for src in graph._graph.predecessors(node):
            relation = graph._graph[src][node]["relation"]
            results.append(f"{src} {relation} {node}")
            update_edge_usage(graph_id, {"head": src, "tail": node, "relation": relation})

    return results
