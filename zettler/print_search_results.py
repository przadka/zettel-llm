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
        notions = results['metadatas'][0][i]['notions']
        quote_start = len(authors) + len(title) + 2
        document = results['documents'][0][i]
        quote = document[quote_start:300]

        print(f"Author(s): {authors}")
        print(f"Title: {title}")
        print(f"Quote: {quote}")
        print(f"Notions: {notions}")
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

    print("\n")  # Newline for better readability