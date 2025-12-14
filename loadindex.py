from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, Settings
import os
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# configuration llamaindex
api_key = os.getenv("MISTRAL_API_KEY")

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

Settings.llm = MistralAI(
    model="mistral-large-latest",
    temperature=0.1,
    max_tokens=512
)


qdrant_client = QdrantClient(
    url= os.getenv("QDRANT_URL"), 
    api_key= os.getenv("QDRANT_API_KEY"),
)


def loadIndex():
    """
    Charge un index déjà existant dans Qdrant sans recréer les embeddings.
    """

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="rag_agent1"
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )

    return index
