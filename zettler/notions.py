QUERY_RESULTS = 10

def get_notions_from_zettelkasten_results(results):
    """
    Returns all the notions from the results of a chromadb zettelkasten collection query. 
    Each notion is added to a list.
    
    Parameters:
        results (dict): Dictionary containing the results of a chromadb query of the zettelkasten collection.

    Returns:
        list: List of all notions from the results.
    """
    
    notions = []

    for entry in results['metadatas'][0]:
        notions_str = entry['notions']
        # Extend the main list with non-empty notions
        notions.extend([notion.strip() for notion in notions_str.split(",") if notion.strip()])

    return notions


def get_notions_from_notions_results(results):
    """
    Returns all the notions from the results of a chromadb notions collection query.
    
    Parameters:
        results (dict): Dictionary containing notions.

    Returns:
        list: List of all notions from the results.
    """
    notions = []

    for document in results['documents'][0]:
        notions.append(document)

    return notions

def get_notions_related_to(query, collections):
    merged_results = []

    for name, collection in collections.items():
        results = collection.query(query_texts=[query], n_results=QUERY_RESULTS)

        if name == "zettelkasten":
            notions_from_zettelkasten = get_notions_from_zettelkasten_results(results)
            merged_results.extend(notions_from_zettelkasten)
        elif name == "notions":
            notions_from_notions = get_notions_from_notions_results(results)
            merged_results.extend(notions_from_notions)

    # Remove duplicates and sort
    return sorted(list(set(merged_results)))

def get_closest_notions(q, notions_collection):
    query_results = notions_collection.query(query_texts=[q], n_results=3)
    return list(zip(query_results['documents'][0], query_results['distances'][0]))