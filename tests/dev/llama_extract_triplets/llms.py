from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from src.llm.ollama_prod import OllamaProdLLM
from src.services.prompt_service import get_entity_production_template, get_relation_production_template, \
    get_topic_and_summary_template


def create_entity_chain():
    llm = OllamaProdLLM()
    template = get_entity_production_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["input_text"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def create_entity_relation_chain():
    llm = OllamaProdLLM()
    template = get_relation_production_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["detected_entities", "input_text_chunk"],
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