import requests
from langchain.llms.base import LLM


# Available Models:
# mistral:7b-instruct-q2_K	1344ecf13c2e	3.1 GB	19 hours ago
# qwen2:1.5b              	f6daf2b25194	934 MB	3 days ago
# nomic-embed-text:latest 	0a109f422b47	274 MB	3 days ago
# llama2:7b               	78e26419b446	3.8 GB	3 days ago
# llama2:7b-json          	a73a226cd089	3.8 GB	3 days ago


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

# FIXME: STUFF
#####
# print("+++ CREATING THE CHAIN")
# # Create the QA chain
# chain = GraphQAChain.from_llm(
#     llm=llm,
#     graph=graph,
#     verbose=True
# )
# get_execution_time()
# print("+++ NOW RUNNING CHAIN")
# while True:
#     # Run the QA chain with the question
#     question = input("Please enter your question: ")
#     response = chain.invoke(question)
#     # Print the response
#     print(response)
