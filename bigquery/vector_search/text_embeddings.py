from openai import OpenAI
from vertexai.language_models import TextEmbeddingModel
import time


class TextEmbeddingClient:

    EMBEDDING_MODEL_OPENAI_SMALL = "text-embedding-3-small"
    EMBEDDING_MODEL_GECKO = "textembedding-gecko@001" #the higher models get throttled 

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

        if self.embedding_model == self.EMBEDDING_MODEL_OPENAI_SMALL:
            self.client = OpenAI()
        elif self.embedding_model == self.EMBEDDING_MODEL_GECKO:
            self.model = TextEmbeddingModel.from_pretrained(self.EMBEDDING_MODEL_GECKO) 
        else:
            raise Exception("Invalid embedding model")

    def get_embedding(self, text):
        if self.embedding_model == self.EMBEDDING_MODEL_OPENAI_SMALL:
            return self._get_openai_embedding(text)
        elif self.embedding_model == self.EMBEDDING_MODEL_GECKO:
            return self._get_google_vertexai_embedding(text)
        else:
            raise ValueError("Unsupported embedding model")
    
    def get_embedding_dim(self):
        if self.embedding_model == self.EMBEDDING_MODEL_OPENAI_SMALL:
            return 1536
        elif self.embedding_model == self.EMBEDDING_MODEL_GECKO:
            return 768
        else:
            raise ValueError("Unsupported embedding model")

    def _get_openai_embedding(self, texts: list):
        response = self.client.embeddings.create(
                        input=texts,
                        model=self.embedding_model
                    )
         
        return [data.embedding for data in response.data]

    def _get_google_vertexai_embedding(self, texts: list):
        embeddings = [embedding.values for embedding in self.model.get_embeddings(texts)]
        return embeddings
    
if __name__ == "__main__":
    
    # Example text for embedding
    texts = ["social media"]
    
    start = time.perf_counter()

    client = TextEmbeddingClient(TextEmbeddingClient.EMBEDDING_MODEL_OPENAI_SMALL)

    embeddings = client.get_embedding(texts)
    print(embeddings)
    with open('c:/tmp/embed.txt', 'w+') as f:
        f.write(str(embeddings))

    # print(embeddings)
    # print(len(embeddings))
    # print(len(embeddings[0]))
    # print(type(embeddings))
    # print(type(embeddings[0]))
    # print(type(embeddings[0][0]))

    # for i in range(10):
    #     start = time.perf_counter()
    #     embeddings = client.get_embedding(texts)
    #     print(f"text embedding: {time.perf_counter() - start} seconds ---")

    # client = TextEmbeddingClient(TextEmbeddingClient.EMBEDDING_MODEL_GECKO)
    # embeddings = client.get_embedding(texts)
    # print(embeddings)

    # print(f"text embedding: {time.perf_counter() - start} seconds ---")
