import os
from sentence_transformers import SentenceTransformer
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class EmbeddingModel:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, sentences):
        print("EMBED DOCUMENTS")
        try:
            embeddings = self.model.encode(sentences)
            return embeddings
        except Exception as e:
            print(f"Error during encoding: {e}")
            return None

    def embed_query(self, query):
        # print("EMBED QUERY")
        try:
            embedding = self.model.encode([query])
            return embedding[0]
        except Exception as e:
            print(f"Error during query encoding: {e}")
            return None
