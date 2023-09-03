import chromadb
from chromadb.utils import embedding_functions
import os, sys

DB_PATH = "/Users/michalparkola/Documents/01 Projects/zettel-llm/zettler/chroma.db"
COLLECTION_NAMES = ["zettelkasten", "notions"]

def get_chroma_client(db_path):
    """Retrieve the ChromaDB client if both collections exist.

    Args:
        db_path (str): Path to the ChromaDB database file.

    Returns:
        chromadb.PersistentClient or None: ChromaDB client or None if a collection doesn't exist.
    """
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection_names = [collection.name for collection in chroma_client.list_collections()]

    if all(collection in collection_names for collection in COLLECTION_NAMES):
        print(f"Database and collections already exist, connecting to it...")
        return chroma_client
    else:
        print(f"Database or collections do not exist, please initialize first.")
        sys.exit()

def get_collections(chroma_client, ef):
    """Retrieve both collections using a given ChromaDB client and embedding function.

    Args:
        client (chromadb.PersistentClient): ChromaDB client.
        embedding_function (EmbeddingFunction): Embedding function for the collections.

    Returns:
        dict: Dictionary with collections.
    """
    return {name: chroma_client.get_collection(name=name, embedding_function=ef) for name in COLLECTION_NAMES}

def get_zettels_and_notions():
    chroma_client = get_chroma_client(DB_PATH)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    return get_collections(chroma_client, openai_ef)

def get_zettels():
    chroma_client = get_chroma_client(DB_PATH)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    return chroma_client.get_collection(name="zettelkasten", embedding_function=openai_ef)

def get_notions():
    chroma_client = get_chroma_client(DB_PATH)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    return chroma_client.get_collection(name="notions", embedding_function=openai_ef)