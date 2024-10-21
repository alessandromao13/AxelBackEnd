import ast
import json
import re

from langchain_core.prompts import PromptTemplate

from src.llm.ollama_prod import OllamaProdLLM
from src.services.prompt_service import get_data_check_template_dict
from tests.dev.llama_extract_triplets.llms import create_summarization_chain
from tests.dev.output_processing_service.response_processing_service import process_llm_response


def produce_topic_and_summary(text):
    chain = create_summarization_chain()
    llm_result = chain.invoke({"text": text})
    # modified_text = llm_result['text'].replace("'", '"').replace('"', '\\"')
    # print("+++ GOT LLM RESULT", llm_result)
    # processed_res = process_llm_response(llm_result)
    # processed_res = test_data_extraction_dict(llm_result['text'])
    # processed_res = ast.literal_eval(llm_result['text'])
    print("LLM RES", llm_result)
    processed_res = json.loads(llm_result['text'])
    print("PROCESSED RESULT", processed_res)
    try:
        topic = processed_res['topic']
        summary = processed_res['summary']
        return topic, summary
    except KeyError as e:
        print(f"ERROR EXTRACTING TOPIC AND SUMMARY {e}")
        return None, None


def test_data_extraction_dict(data_to_check):
    template = get_data_check_template_dict()
    prompt = PromptTemplate(
        template=template,
        input_variables=["got_data"],
    )
    model = OllamaProdLLM()
    chain = prompt | model
    response = chain.invoke({"got_data": data_to_check})
    return json.loads(response)
