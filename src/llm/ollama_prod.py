import requests
from langchain.llms.base import LLM

# Available Models:
# mistral:7b-instruct-q2_K	1344ecf13c2e	3.1 GB	19 hours ago
# qwen2:1.5b              	f6daf2b25194	934 MB	3 days ago
# nomic-embed-text:latest 	0a109f422b47	274 MB	3 days ago
# llama2:7b               	78e26419b446	3.8 GB	3 days ago
# llama2:7b-json          	a73a226cd089	3.8 GB	3 days ago


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
            "temperature": 0
        }
        print("++ LLM Loading.. ++")

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # print("+++ GOT LLM RES", response.json())
            return response.json()['choices'][0]['text'].strip()
        else:
            raise Exception(f"Failed to call model: {response.text}")

