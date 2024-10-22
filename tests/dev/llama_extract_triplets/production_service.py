import ast
import json
import os

from langchain_core.prompts import PromptTemplate

from src.llm.ollama_prod import OllamaProdLLM
from src.persistence.mongoDB import save_partial_graph, save_failed_chunk, check_failed_chunk
from src.services.prompt_service import get_data_check_template_array
from tests.dev.llama_extract_triplets.llms import create_entity_chain, create_entity_relation_chain
from tests.dev.output_processing_service.response_processing_service import manage_llm_response, \
    parse_valid_python_dict_or_array


run_num = 1


# todo: evaluate what is the best chunk length
def chunk_text(text, max_length=1024):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# def generate_entities_from_chunk(text_chunk):
#     llm_res = []
#     entity_chain = create_entity_chain()
#     with open("../outputs/entity_llm_chunk_res.txt", "a") as file:
#         print(f"Processing chunk: {text_chunk}")
#         result = entity_chain.invoke({"input_text": text_chunk})
#         processed_result = manage_llm_response(result['text'])
#         llm_res.append(result)
#         file.write(f"Chunk: {text_chunk}\n")
#         file.write(f"Response: {processed_result}\n")
#         file.write("-" * 40 + "\n")
#     return processed_result
def generate_entities_from_chunk(text_chunk):
    llm_res = []
    entity_chain = create_entity_chain()
    output_dir = "../outputs"
    output_file = os.path.join(output_dir, "entity_llm_chunk_res.txt")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the file in append mode (creates the file if it doesn't exist)
    with open(output_file, "a") as file:
        print(f"Processing chunk: {text_chunk}")
        result = entity_chain.invoke({"input_text": text_chunk})
        # processed_result = test_data_extraction(result)
        processed_result = ast.literal_eval(result['text'])
        # processed_result = json.loads(result['text'])
        print("PROCESSED RESULT", processed_result)
        # processed_result = manage_llm_response(result['text'])
        llm_res.append(result)
        file.write(f"Chunk: {text_chunk}\n")
        file.write(f"Response: {processed_result}\n")
        file.write("-" * 40 + "\n")

    return processed_result


def generate_triplets_from_chunk_and_entities(got_entities, chunk, user_id):
    triplet_chain = create_entity_relation_chain()
    llm_res = []
    failed_extraction = None
    output_dir = "../outputs"
    output_file = os.path.join(output_dir, "triplets_llm_chunk_res.txt")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "a") as file:
        print(f"Chunk: {chunk}")
        # print(f"Entities: {got_entities}")
        result = triplet_chain.invoke({"detected_entities": got_entities, "input_text_chunk": chunk})
        print("+++ TRIPLETS ", result)
        # dict_result = parse_valid_python_dict_or_array(result['text'])
        dict_result = ast.literal_eval(result['text'])
        # dict_result = json.loads(result['text'])
        if dict_result:
            llm_res.append(result)
            file.write(f"Chunk: {chunk}\n")
            file.write(f"Entities: {got_entities}\n")
            file.write(f"Response: {result['text']}\n")
            # print("GOT DICT RES", dict_result)
            file.write(f"Loaded dict: {dict_result}\n")
            save_partial_graph(dict_result, run_num, chunk, user_id)
        else:
            file.write(f"FAILED \n")
            file.write(f"Chunk: {chunk}\n")
            file.write(f"Entities: {got_entities}\n")
            failed_extraction = {"chunk": chunk, "entities": got_entities}
        file.write("-" * 40 + "\n")
    return failed_extraction


def rerun_failed_extractions(failed_extraction, user_id):
    print("RERUNNING ..", failed_extraction)
    again_fails = rerun_generate_triplets_from_chunk_and_entities(failed_extraction['entities'], failed_extraction['chunk'], user_id)
    if len(again_fails) > 0:
        print("FAILED TWICE", again_fails)
        save_failed_chunk(again_fails, run_num)
    else:
        print("ALL GOOD")


def rerun_generate_triplets_from_chunk_and_entities(got_entities, chunk, user_id):
    triplet_chain = create_entity_relation_chain()
    failed_extractions_again = []
    output_dir = "../outputs"
    output_file = os.path.join(output_dir, "failed_triplets_llm_chunk_res.txt")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file, "a") as file:
        result = triplet_chain.invoke({"detected_entities": got_entities, "input_text_chunk": chunk})
        dict_result = parse_valid_python_dict_or_array(result['text'])
        if dict_result:
            file.write(f"Chunk: {chunk}\n")
            file.write(f"Entities: {got_entities}\n")
            file.write(f"Response: {result['text']}\n")
            file.write(f"Loaded dict: {dict_result}\n")
            save_partial_graph(dict_result, run_num, chunk, user_id)
        else:
            file.write(f"FAILED TWICE \n")
            file.write(f"Chunk: {chunk}\n")
            file.write(f"Entities: {got_entities}\n")
            failed_extractions_again.append({"chunk": chunk, "entities": got_entities})
        file.write("-" * 40 + "\n")
    return failed_extractions_again


# MAIN FUNCTION
def extract_triplets_from_text(input_text, user_id):
    """
    :param input_text:
    :return: None

    This function accepts a text input and:
    1. Divides it in chunks (sentences)
    For every chunk
    2. Extracts entities in the given chunk
    3. Given the text chunk and the entities found, generates some triplets to link the entities
        e.g. [{'src': 'ent1', 'dst': 'ent2', 'rel': 'the relation that links them'}]
    4. Runs again the process from .3 for every run that failed (probably due to poorly-formatted data)

    Notes:
    Every triplet successfully generated by one text chunk is saved in a temporary mongo collection
    as well as the chunks that where re-run (if they run successfully the second try)

    If some run fails twice, it is saved to a separated mongo collection,
    that is later used to notify the user and ask him if he needs to re-run again.

    When the whole process is over, all the triplets are joined together to generate e Knowledge Graph
    """
    failed_extr = []

    # Divides the text into sentences
    chunks = chunk_text(input_text)

    for chunk in chunks:
        # extract entities from the sentence
        got_entities = generate_entities_from_chunk(chunk)
        # generate triplets based on sentence and entities detected
        print("+++ GOT ENTITIES", got_entities)
        failed = generate_triplets_from_chunk_and_entities(got_entities, chunk, user_id)

        # save the failed runs
        if failed:
            failed_extr.append(failed)

    # check if any run failed
    if len(failed_extr) > 0:
        print("RERUNNING FAILED EXTRACTIONS: ", failed_extr)
        for fail in failed_extr:
            print("RUNNING THIS ONE THAT FAILED", fail)
            if fail is not [] and len(fail) > 0:
                # re-run the failed ones
                rerun_failed_extractions(fail, user_id)

    # Check if there's still some missing information's
    failed_twice = check_failed_chunk(run_num)
    if failed_twice:
        # Ask the user if he needs to run again (two more tries or make him integrate this manually)
        print(f"Troubles encountered when processing this piece {failed_twice}, do you with to try again?")
    return failed_twice


def test_data_extraction(data_to_check):
    template = get_data_check_template_array()
    prompt = PromptTemplate(
        template=template,
        input_variables=["got_data"],
    )
    model = OllamaProdLLM()
    chain = prompt | model
    response = chain.invoke({"got_data": data_to_check['text']})

    try:
        parsed_response = ast.literal_eval(response)
        if isinstance(parsed_response, list) and all(isinstance(i, str) for i in parsed_response):
            return parsed_response
        else:
            raise ValueError("Response is not a valid list of strings.")
    except (ValueError, SyntaxError) as e:
        print(f"Failed to parse response: {e}")
        return []
