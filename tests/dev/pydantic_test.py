import requests
from langchain_core.language_models import LLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator


class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


joke_query = "Tell me a joke."

parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query in JSON format:\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


class OllamaProdLLM(LLM):
    @property
    def _llm_type(self):
        return "ollama"

    def _call(self, prompt, stop=None):
        url = "http://10.2.0.18:11434/v1/completions"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3.2:3b",
            "prompt": prompt
        }
        print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")


model = OllamaProdLLM()
chain = prompt | model | parser
print(chain.invoke({"query": joke_query}))
