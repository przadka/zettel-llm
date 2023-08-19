import os
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "./chroma.db"
COLLECTION_NAME = "zettelkasten"
QUERY_TEXT = ["artificial intelligence"]
N_RESULTS = 5


def get_chroma_client(db_path):
    """Retrieve the ChromaDB client if the 'zettelkasten' collection exists.

    Args:
        db_path (str): Path to the ChromaDB database file.

    Returns:
        chromadb.PersistentClient or None: ChromaDB client or None if the 'zettelkasten' collection doesn't exist.
    """
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection_names = [collection.name for collection in chroma_client.list_collections()]

    if COLLECTION_NAME in collection_names:
        print(f"Database and collection '{COLLECTION_NAME}' already exist, connecting to it...")
        return chroma_client
    else:
        print(f"Database and collection '{COLLECTION_NAME}' do not exist, please initialize first.")
        return None


def get_collection(client, embedding_function):
    """Retrieve a specific collection using a given ChromaDB client and embedding function.

    Args:
        client (chromadb.PersistentClient): ChromaDB client.
        embedding_function (EmbeddingFunction): Embedding function for the collection.

    Returns:
        Collection: The specified collection.
    """
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)


def main():
    """Main execution function."""
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    chroma_client = get_chroma_client(DB_PATH)

    if chroma_client:
        collection = get_collection(chroma_client, openai_ef)

        # Query the collection
        results = collection.query(query_texts=QUERY_TEXT, n_results=N_RESULTS)
        print(results)


if __name__ == "__main__":
    main()
