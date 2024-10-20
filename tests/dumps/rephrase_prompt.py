from BE.src.llm.ollama_prompt import OllamaPromptLLM
from langchain.chains import GraphQAChain
from langchain_core.prompts import PromptTemplate
from BE.src.services.prompt_service import get_prompt_rephrase_template
from langchain.chains import LLMChain


def create_chain():
    llm = OllamaPromptLLM()
    template = get_prompt_rephrase_template()
    prompt = PromptTemplate(
        template=template,
        input_variables=["got_context", "user_query"],
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


if __name__ == '__main__':
    chain = create_chain()
    contesto = """
    Sara Rossi spouse Mario Neri
    Sara Rossi place of birth Ceva
    Sara Rossi date of birth 2009
    Sara Rossi employer University of London
    Gym inventor Sara Rossi
    Mario Neri spouse Sara Rossi
    """
    chain.invoke({"got_context": contesto, "user_query": "Who is Sara Rossi?"})
