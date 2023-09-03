import os
import time
import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

API_LIMIT_RATE = 250
start_time = time.time()

def embed_and_add_to_db(total_documents, documents, ids, metadatas, collection):
    chunk_size = API_LIMIT_RATE
    print(f"Starting initialization of {total_documents} documents...")

    for i in range(0, total_documents, chunk_size):
        chunked_docs = documents[i:i+chunk_size]
        chunked_ids = ids[i:i+chunk_size]
        chunked_metadatas = metadatas[i:i+chunk_size]

        collection.add(documents=chunked_docs, ids=chunked_ids, metadatas=chunked_metadatas,)

        elapsed_time = time.time() - start_time
        remaining_docs = total_documents - (i + chunk_size)
        estimated_time_remaining = (elapsed_time / (i + chunk_size)) * remaining_docs

        print(f"Processed document {i+chunk_size} of {total_documents}. Elapsed Time: {elapsed_time:.2f} seconds. ETA: {estimated_time_remaining:.2f} seconds.")
        time.sleep(1)

def initialize_db():
    """
    Initialize the database with data from CSV files.
    Logs are printed to the standard output detailing the progress of the operation.
    """

    # Setup the OpenAI embedding function.
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    db_path = "./chroma.db"
    chroma_client = chromadb.PersistentClient(path=db_path)

    # Check and create zettelkasten collection if not exists
    if "zettelkasten" not in [collection.name for collection in chroma_client.list_collections()]:
        chroma_client.create_collection(name="zettelkasten", embedding_function=openai_ef)
    zettelkasten_collection = chroma_client.get_collection(name="zettelkasten", embedding_function=openai_ef)

    # Check and create notions collection if not exists
    if "notions" not in [collection.name for collection in chroma_client.list_collections()]:
        chroma_client.create_collection(name="notions", embedding_function=openai_ef)
    notions_collection = chroma_client.get_collection(name="notions", embedding_function=openai_ef)

    # Load and embed notions
    data_notions = pd.read_csv('documents/notions.csv')
    data_notions['txt'] = data_notions['Notions']

    documents_notions = data_notions['txt'].tolist()
    ids_notions = ["N:" + str(idx) for idx in data_notions.index]
    metadatas_notions = [None for _ in range(len(documents_notions))]

    total_documents_notions = len(documents_notions)
    embed_and_add_to_db(total_documents_notions, documents_notions, ids_notions, metadatas_notions, notions_collection)

    # Load and embed quotes
    data_quotes = pd.read_csv('documents/train_data.csv')
    columns_to_include = ['author(s)', 'title of the source', 'type of the source', 'quotation'] 
    notion_columns = ['notion_{}'.format(i) for i in range(1, 9)]
    data_quotes[columns_to_include + notion_columns] = data_quotes[columns_to_include + notion_columns].fillna('').astype(str)
    data_quotes['txt'] = data_quotes[columns_to_include + notion_columns].agg(' '.join, axis=1)
    data_quotes['notions'] = data_quotes[['notion_{}'.format(i) for i in range(1, 9)]].agg(','.join, axis=1)
    
    documents_quotes = data_quotes['txt'].tolist()
    ids_quotes = ["Z:" + str(idx) for idx in data_quotes["ID"].astype(str)]

    # Extracting the values from notion_1 to notion_8 and joining them into a single string

    metadatas_quotes = data_quotes[["author(s)", "title of the source", "type of the source", "notions"]].to_dict(orient="records")

    total_documents_quotes = len(documents_quotes)
    embed_and_add_to_db(total_documents_quotes, documents_quotes, ids_quotes, metadatas_quotes, zettelkasten_collection)

    print(f"Initialization completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    initialize_db()
