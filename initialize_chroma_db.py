import os
import time
import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

API_LIMIT_RATE = 100  # Adjust based on the allowed rate by the API (requests per second)

def initialize_db():
    """
    Initialize the database with data from a CSV file.
    Logs are printed to the standard output detailing the progress of the operation.
    """

    start_time = time.time()

    # Load data from CSV
    data = pd.read_csv('documents/data_Zettel.csv')

    # Create a new 'txt' column by joining specific columns.
    data['txt'] = data[['author(s)', 'title of the source', 'type of the source', 'quotation']].agg(' '.join, axis=1)

    # Extract 'txt' column values and their corresponding unique indices (as IDs).
    documents = data['txt'].tolist()
    ids = [str(x) for x in data.index.tolist()]

    # Setup the OpenAI embedding function.
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    db_path = "./chroma.db"
    chroma_client = chromadb.PersistentClient(path=db_path)

    if "zettelkasten" not in [collection.name for collection in chroma_client.list_collections()]:
        chroma_client.create_collection(name="zettelkasten", embedding_function=openai_ef)

    collection = chroma_client.get_collection(name="zettelkasten", embedding_function=openai_ef)

    total_documents = len(documents)
    chunk_size = API_LIMIT_RATE

    print(f"Starting initialization of {total_documents} documents...")

    for i in range(0, total_documents, chunk_size):
        chunked_docs = documents[i:i+chunk_size]
        chunked_ids = ids[i:i+chunk_size]
        collection.add(documents=chunked_docs, ids=chunked_ids)

        elapsed_time = time.time() - start_time
        remaining_docs = total_documents - (i + chunk_size)
        estimated_time_remaining = (elapsed_time / (i + chunk_size)) * remaining_docs

        print(f"Processed document {i+chunk_size} of {total_documents}. Elapsed Time: {elapsed_time:.2f} seconds. ETA: {estimated_time_remaining:.2f} seconds.")

        # Sleep for a second to respect the API's rate limit
        time.sleep(1)

    print(f"Initialization completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    initialize_db()
