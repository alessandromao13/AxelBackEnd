# import time
#
# from langchain.chains.llm import LLMChain
# from langchain_core.prompts import PromptTemplate
#
# from src.llm.ollama_prod import OllamaProdLLM
# from src.persistence.mongoDB import save_partial_graph, clear_coll, save_failed_chunk, check_failed_chunk
# from src.services.hf_triplets import chunk_text
# from src.services.prompt_service import get_triplet_production_template, get_entity_production_template, \
#     get_relation_production_template
# from tests.res_cleaning_service.general_res import manage_llm_response, parse_valid_python_dict_or_array
#
#
# def get_time(flag, start=None):
#     if flag == "START":
#         return time.time()
#     elif flag == "STOP":
#         end_time = time.time()
#         print(f"Execution took {end_time - start}")
#
#
# # fixme test
# def create_triplet_chain():
#     llm = OllamaProdLLM()
#     template = get_triplet_production_template()
#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["input_text"],
#     )
#     return LLMChain(llm=llm, prompt=prompt, verbose=True)
#
#
# def create_entity_chain():
#     llm = OllamaProdLLM()
#     template = get_entity_production_template()
#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["input_text"],
#     )
#     return LLMChain(llm=llm, prompt=prompt, verbose=True)
#
#
# def create_entity_relation_chain():
#     llm = OllamaProdLLM()
#     template = get_relation_production_template()
#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["detected_entities", "input_text_chunk"],
#     )
#     return LLMChain(llm=llm, prompt=prompt, verbose=True)
#
#
# def generate_entities_from_chunk(text_chunk):
#     llm_res = []
#     entity_chain = create_entity_chain()
#     with open("outputs/entity_llm_chunk_res.txt", "a") as file:
#         print(f"Processing chunk: {text_chunk}")
#         result = entity_chain.invoke({"input_text": text_chunk})
#         processed_result = manage_llm_response(result['text'])
#         llm_res.append(result)
#         file.write(f"Chunk: {text_chunk}\n")
#         file.write(f"Response: {processed_result}\n")
#         file.write("-" * 40 + "\n")
#     return processed_result
#
#
# def generate_triplets_from_chunk_and_entities(got_entities, chunk):
#     triplet_chain = create_entity_relation_chain()
#     llm_res = []
#     failed_extraction = None
#     with open("outputs/triplets_llm_chunk_res.txt", "a") as file:
#         print(f"Chunk: {chunk}")
#         print(f"Entities: {got_entities}")
#         result = triplet_chain.invoke({"detected_entities": got_entities, "input_text_chunk": chunk})
#         dict_result = parse_valid_python_dict_or_array(result['text'])
#         if dict_result:
#             llm_res.append(result)
#             file.write(f"Chunk: {chunk}\n")
#             file.write(f"Entities: {got_entities}\n")
#             file.write(f"Response: {result['text']}\n")
#             print("GOT DICT RES", dict_result)
#             file.write(f"Loaded dict: {dict_result}\n")
#             save_partial_graph(dict_result, run_num, chunk)
#         else:
#             file.write(f"FAILED \n")
#             file.write(f"Chunk: {chunk}\n")
#             file.write(f"Entities: {got_entities}\n")
#             failed_extraction = {"chunk": chunk, "entities": got_entities}
#         file.write("-" * 40 + "\n")
#     return failed_extraction
#
#
# def rerun_failed_extractions(failed_extraction):
#     print("RERUNNING ..", failed_extraction)
#     again_fails = rerun_generate_triplets_from_chunk_and_entities(failed_extraction['entities'], failed_extraction['chunk'])
#     if len(again_fails) > 0:
#         print("FAILED TWICE", again_fails)
#         save_failed_chunk(again_fails, run_num)
#     else:
#         print("ALL GOOD")
#
#
# def rerun_generate_triplets_from_chunk_and_entities(got_entities, chunk):
#     print("RERUN FUNCTION")
#     triplet_chain = create_entity_relation_chain()
#     failed_extractions_again = []
#     with open("outputs/failed_triplets_llm_chunk_res.txt", "a") as file:
#         print(f"Chunk: {chunk}")
#         print(f"Entities: {got_entities}")
#         result = triplet_chain.invoke({"detected_entities": got_entities, "input_text_chunk": chunk})
#         dict_result = parse_valid_python_dict_or_array(result['text'])
#         if dict_result:
#             llm_res.append(result)
#             file.write(f"Chunk: {chunk}\n")
#             file.write(f"Entities: {got_entities}\n")
#             file.write(f"Response: {result['text']}\n")
#             print("GOT DICT RES", dict_result)
#             file.write(f"Loaded dict: {dict_result}\n")
#             save_partial_graph(dict_result, run_num, chunk)
#         else:
#             file.write(f"FAILED AGAIN")
#             file.write(f"Chunk: {chunk}\n")
#             file.write(f"Entities: {got_entities}\n")
#             failed_extractions_again.append({"chunk": chunk, "entities": got_entities})
#         file.write("-" * 40 + "\n")
#     return failed_extractions_again
#
#
# #  fixme triplet generation test
# if __name__ == '__main__':
#     clear_coll()
#     run_num = 1
#
#     failed_extr = []
#
#     with open("../src/assets/Aliens_abstract.txt", "r") as file:
#         input_text = file.read()
#     print(input_text)
#
#     chunks = chunk_text(input_text)
#     llm_res = []
#     start_time = get_time("START")
#
#     for chunk in chunks:
#         got_entities = generate_entities_from_chunk(chunk)
#         failed = generate_triplets_from_chunk_and_entities(got_entities, chunk)
#         if failed:
#             failed_extr.append(failed)
#
#     if len(failed_extr) > 0:
#         print("RERUNNING FAILED EXTRACTIONS: ", failed_extr)
#         for fail in failed_extr:
#             print("RUNNING THIS ONE THAT FAILED", fail)
#             if fail is not [] and len(fail) > 0:
#                 rerun_failed_extractions(fail)
#
#     failed_result = check_failed_chunk(run_num)
#     if failed_result:
#         print(f"Trubbles encountered when processing this piece {failed_result}, do you with to try again?")
#
#     get_time("STOP", start_time)
#
