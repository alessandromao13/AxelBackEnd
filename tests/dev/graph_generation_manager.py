from src.persistence.mongoDB import clear_coll
from tests.dev.generate_graph_from_triplets.generate_graph import generate_knowledge_graph, collect_triplet_chunks
from tests.dev.llama_extract_triplets.production_service import extract_triplets_from_text
from tests.dev.llama_generate_title_and_summary.generate_title_and_summary import produce_topic_and_summary


def run_graph_generation_system(text, user_id, document_title=None, document_summary=None):
    clear_coll()
    # print("++ RUNNING GRAPH GENERATION SYSTEM")
    if not document_title and not document_summary:
        document_title, document_summary = produce_topic_and_summary(text)
    # print("++ EXTRACTING TRIPLETS")
    failed_runs = extract_triplets_from_text(text, user_id)
    # TODO ==> implement a notification service \/
    print(f"+++ You should ask the user about this runs.. {failed_runs}")
    final_triplets = collect_triplet_chunks(user_id)
    kg = generate_knowledge_graph(text, final_triplets, document_title, document_summary, user_id)
    print("Generated Knowledge Graph", kg)


def clear_files():
    try:
        with open("../dev/outputs/triplets_llm_chunk_res.txt", 'w'):
            pass
        with open("../dev/outputs/failed_triplets_llm_chunk_res.txt", 'w'):
            pass
        with open("../dev/outputs/entity_llm_chunk_res.txt", 'w'):
            pass

    except Exception as e:
        print(f"An error occurred while clearing the file: {e}")


if __name__ == '__main__':
    clear_coll()
    clear_files()
    with open("../../src/assets/text/Aliens_abstract.txt", 'r') as file:
        text = file.read()
    print("TEXT IS", text)
    run_graph_generation_system(text, 10, None, None)
