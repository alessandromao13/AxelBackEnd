from langchain.embeddings.base import Embeddings
import requests


# Create an embedding function class that extends the LangChain Embeddings class
class OllamaEmbeddings(Embeddings):
    def __init__(self, model_name="nomic-embed-text:latest", url="http://10.2.0.18:11434/api/embeddings"):
        self.model_name = model_name
        self.url = url

    # The method that will be used to generate embeddings
    def embed_query(self, text):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model_name,
            "prompt": text,  # text to embed
            "temperature": 0
        }

        print("++ Embedding query.. ++")

        response = requests.post(self.url, json=data, headers=headers)
        if response.status_code == 200:
            # Return the embeddings instead of text
            # print("RESPONSE", response.json())
            return response.json()['embedding']  # Make sure the API returns embeddings in this key
        else:
            raise Exception(f"Failed to call model: {response.text}")

    def embed_documents(self, texts):
        # To embed a list of documents
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_query(text))
        return embeddings