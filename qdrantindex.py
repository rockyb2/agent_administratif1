from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,StorageContext,Settings
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
    max_tokens=1024
)


qdrant_client = QdrantClient(
    url= os.getenv("QDRANT_URL"), 
    api_key= os.getenv("QDRANT_API_KEY"),
)

# creation of the collection
collection_name = "rag_agent1"
# qdrant_client.recreate_collection(
#     collection_name=collection_name,
#     vectors_config=VectorParams(size=384, distance =Distance.COSINE)
# )


# function for stocker les index dans une bdd vectoriel qdrant

def create_rag_index (directory: str):
    """
    Load the documents and create the index in Qdrant once and for all .
    """
    
    documents = SimpleDirectoryReader(directory).load_data()
    
    stores = QdrantVectorStore(
        client = qdrant_client,
        collection_name= collection_name
    )
    
    storage_context = StorageContext.from_defaults(vector_store=stores)
    
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )
    
    print("Index RAG créé et enregistré dans Qdrant !")
    return index

create_rag_index("bdc")


