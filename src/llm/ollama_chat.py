import requests
from langchain.llms.base import LLM


class OllamaChatLLM(LLM):
    @property
    def _llm_type(self):
        return "ollama"

    def _call(self, prompt, stop=None):
        # url = "http://10.2.0.15:11434/v1/completions"
        url = "http://10.2.0.18:11434/v1/completions"
        data = {
            "model": "llama3.2:3b",
            # "model": "qwen2:1.5b",
            "prompt": prompt
        }

        headers = {
            "Content-Type": "application/json"
        }
        print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # print("+++ GOT LLM RES", response.json())
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")
