from tests.dev.llama_extract_triplets.llms import create_summarization_chain
from tests.dev.output_processing_service.response_processing_service import process_llm_response


def produce_topic_and_summary(text):
    chain = create_summarization_chain()
    llm_result = chain.invoke({"text": text})
    # print("+++ GOT LLM RESULT", llm_result)
    processed_res = process_llm_response(llm_result)
    try:
        topic = processed_res['topic']
        summary = processed_res['summary']
        return topic, summary
    except KeyError as e:
        print(f"ERROR EXTRACTING TOPIC AND SUMMARY {e}")
        return None, None