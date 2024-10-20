# import yaml
# from bson import ObjectId
# from src.persistence.mongoDB import get_graph_by_id
# from src.services.context_retriever import build_context
# # from src.services.general_service import generate_kg
#
# # fixme: THIS FILE IS ONLY INTENDED FOR LOCAL TESTING WITH NO UI - CHECK CONFIG.YAML FOR SETUP
#
#
# def load_config(file_path):
#     with open(file_path, 'r') as file:
#         config = yaml.safe_load(file)
#     return config
#
#
# def setup_and_run_chain():
#     config = load_config('../config.yaml')
#     # Esegui l'operazione di creazione grafo o dialogo con grafo esistente
#     print("CONFIG ", config)
#     if config['create'] is True:
#         text_document = config['create_graph']['requirements']['text_document']
#         with open(text_document, 'r') as file:
#             text = file.read()
#         run_chain(text=text, build_kg=True)
#     else:
#         graph_id = config['dialog_with_existing_graph']['requirements']['graph_id']
#         run_chain(graph_id=ObjectId(graph_id), build_kg=False)
#
#
# def simulate_chat(graph):
#     while True:
#         query = input("ENTER QUERY..")
#         got_context = build_context(graph, query)
#         print("GOT CONTEXT", got_context)
#
#
# def run_chain(text=None, graph_id=None, build_kg=True):
#     if build_kg:
#         graph = generate_kg(text)
#     else:
#         print(f"Using existing graph with ID: {graph_id}")
#         graph = get_graph_by_id(graph_id)
#     return simulate_chat(graph)
#
#
# def main():
#     setup_and_run_chain()
#
#
# if __name__ == "__main__":
#     main()
