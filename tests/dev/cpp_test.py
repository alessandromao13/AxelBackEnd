from langchain_core.language_models import LLM
import requests
from llama_cpp.llama import Llama, LlamaGrammar
import httpx
grammar_text = httpx.get("https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf").text

grammar = LlamaGrammar.from_string(grammar_text)

class OllamaProdLLM(LLM):
    @property
    def _llm_type(self):
        return "ollama"

    def _call(self, prompt, stop=None):
        # url = "http://10.2.0.15:11434/v1/completions"
        url = "http://10.2.0.18:11434/v1/completions"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3.2:3b",
            "prompt": prompt,
        }
        print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # print("+++ GOT LLM RES", response.json())
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")


llm = OllamaProdLLM()

response = llm(
    "Extract all entities from this text: 'Alberto and Angelo went for an Icecream'",
    grammar=grammar, max_tokens=-1
)

print("res", response)
