from langchain_core.prompts import PromptTemplate

from src.llm.ollama_prod import OllamaProdLLM
from src.services.prompt_service import get_data_check_template_array, get_data_check_template_dict


def test_data_extraction_array(data_to_check):
    template = get_data_check_template_array()
    prompt = PromptTemplate(
        template=template,
        input_variables=["got_data"],
    )
    model = OllamaProdLLM()
    chain = prompt | model
    response = chain.invoke({"got_data": data_to_check})
    return response


def test_data_extraction_dict(data_to_check):
    template = get_data_check_template_dict()
    prompt = PromptTemplate(
        template=template,
        input_variables=["got_data"],
    )
    model = OllamaProdLLM()
    chain = prompt | model
    response = chain.invoke({"got_data": data_to_check})
    return response


if __name__ == '__main__':
    data = """{'text': "{'topic': 'The Fall of the Zenthari Empire', 'summary': 'A complex interstellar power struggle ensues as the Zenthari Empire faces threats from within and outside forces, including a rising rebellion, a rival faction, and emerging genetically enhanced beings, all vying for control of resources and territories in the galaxy.}"}"""
    result = test_data_extraction_dict(data)
    print(result)
