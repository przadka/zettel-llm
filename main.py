import os
import chromadb
from chromadb.utils import embedding_functions
import argparse

DB_PATH = "./chroma.db"
COLLECTION_NAMES = ["zettelkasten", "notions"]

QUERY_RESULTS = 20
PRINT_RESULTS = 20

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Query ChromaDB with given text.")
    parser.add_argument("query", type=str, nargs='?', default=None,
                        help="Text to query against the ChromaDB collection.")
    
    args = parser.parse_args()
    if args.query is None:
        print("Please provide a query text.")
        parser.print_help()
        exit(1)

    return args


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
    
    for i in range(min(n, len(results['metadatas'][0]))):
        authors = results['metadatas'][0][i]['author(s)']
        title = results['metadatas'][0][i]['title of the source']
        quote_start = len(authors) + len(title) + 2
        document = results['documents'][0][i]
        quote = document[quote_start:150] + " ... " + document[-300:]

        print(f"Author(s): {authors}")
        print(f"Title: {title}")
        print(f"Quote: {quote}")
        print("="*50)  # print separator for better readability

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
        print(f"{notion}")
        
    print("\n")  # Space for better readability

def main():
    """Main execution function."""
    args = parse_arguments()  # Parse the command line arguments

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002"
    )

    chroma_client = get_chroma_client(DB_PATH)

    if chroma_client:
        collections = get_collections(chroma_client, openai_ef)

        for name, collection in collections.items():
            print(f"Query results for {name}:")
            results = collection.query(query_texts=[args.query], n_results=QUERY_RESULTS)

            if name == "zettelkasten":
                print_top_n_zettelkasten_results(results, n=PRINT_RESULTS)
            elif name == "notions":
                print_top_n_notions_results(results, n=PRINT_RESULTS)

if __name__ == "__main__":
    main()