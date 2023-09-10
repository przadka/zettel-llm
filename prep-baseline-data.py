import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "./chroma.db"
COLLECTION_NAMES = ["zettelkasten", "notions"]
QUERY_RESULTS = 30
CSV_FILE_PATH = 'queries.csv'  # Replace with your CSV file path

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
        return None

def get_collections(client, embedding_function):
    """Retrieve both collections using a given ChromaDB client and embedding function.

    Args:
        client (chromadb.PersistentClient): ChromaDB client.
        embedding_function (EmbeddingFunction): Embedding function for the collections.

    Returns:
        dict: Dictionary with collections.
    """
    return {name: client.get_collection(name=name, embedding_function=embedding_function) for name in COLLECTION_NAMES}

def print_top_n_zettelkasten_results(results, n=2):
    """
    Prints up to the top n results from a given results dictionary.
    
    Parameters:
        results (dict): Dictionary containing the results.
        n (int): Number of top results to print. Default is 2.
    """
    print("Zettelkasten Results:")
    print("=" * 60)  # Heading separator
    for i in range(min(n, len(results['metadatas'][0]))):
        authors = results['metadatas'][0][i]['author(s)']
        title = results['metadatas'][0][i]['title of the source']
        notions = results['metadatas'][0][i]['notions']
        quote_start = len(authors) + len(title) + 2
        document = results['documents'][0][i]
        distance = results['distances'][0][i]

        quote = document[quote_start:300]

        print(f"Author(s): {authors}")
        print(f"Title: {title}")
        print(f"Quote: {quote}")
        print(f"Distance: {distance}")
        print(f"Notions: {notions}")
        print("="*50)  # print separator for better readability
    
    print("\n")  # Space for better readability

def get_notions_from_zettelkasten_results(results):
    """
    Returns all the notions from a given results dictionary. 
    Each notion is added to a list.
    
    Parameters:
        results (dict): Dictionary containing the results.

    Returns:
        list: List of all notions from the results.
    """
    
    notions_list = []

    for entry in results['metadatas'][0]:
        notions_str = entry['notions']
        notions_list.extend([notion.strip() for notion in notions_str.split(",") if notion.strip()])
    
    return notions_list


def print_top_n_notions_results(results, n=2):
    """
    Prints up to the top n results from the notions results dictionary.
    
    Parameters:
        results (dict): Dictionary containing the results.
        n (int): Number of top results to print. Default is 2.
    """
    print("Notions Results:")
    print("=" * 60)  # Heading separator
    
    for i in range(min(n, len(results['documents'][0]))):
        notion = results['documents'][0][i]
        distance = results['distances'][0][i]
        print(f"{notion}")
        print(f"Distance: {distance}")

    print("\n")  # Space for better readability

def get_notions_from_notions_results(results):
    """
    Returns all the notions from the provided results dictionary.
    
    Parameters:
        results (dict): Dictionary containing the results.

    Returns:
        list: List of all notions from the results.
    """
    notions_list = [document for document in results['documents'][0]]
    return notions_list

def get_merged_notions_for_query(query):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    chroma_client = get_chroma_client(DB_PATH)
    all_notions = []

    if chroma_client:
        collections = get_collections(chroma_client, openai_ef)
        for name, collection in collections.items():
            results = collection.query(query_texts=[query], n_results=QUERY_RESULTS)
            if name == "zettelkasten":
                notions_from_zettelkasten = get_notions_from_zettelkasten_results(results)
                all_notions.extend(notions_from_zettelkasten)
            elif name == "notions":
                notions_from_notions = get_notions_from_notions_results(results)
                all_notions.extend(notions_from_notions)

        unique_notions_ordered_by_relevance = []
        for notion in all_notions:
            if notion not in unique_notions_ordered_by_relevance:
                unique_notions_ordered_by_relevance.append(notion)

        return unique_notions_ordered_by_relevance
    return []

def main():
    df = pd.read_csv(CSV_FILE_PATH)
    # Assume that the queries are in the first column of the dataframe
    df["Merged Notions"] = df.iloc[:, 0].apply(get_merged_notions_for_query)
    # Write the dataframe back to the same CSV
    df.to_csv(CSV_FILE_PATH, index=False)

if __name__ == "__main__":
    main()