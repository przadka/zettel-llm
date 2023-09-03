import os
from dotenv import load_dotenv, find_dotenv
import chromadb
from chromadb.utils import embedding_functions
import argparse

import chroma
import notions

# Load the OpenAI API key from .env
_ = load_dotenv(find_dotenv())

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

def main():
    """Main execution function."""
    args = parse_arguments()  # Parse the command line arguments
    
    collections = chroma.get_zettels_and_notions()

    unique_notions = notions.get_notions_related_to(args.query, collections)

    # Print merged results
    print("\nMerged Notions:")
    for notion in unique_notions:
        print(notion)

if __name__ == "__main__":
    main()