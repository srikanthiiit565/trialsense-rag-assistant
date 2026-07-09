def validate_context(
        documents,
        minimum_documents=2
):


    if not documents:

        return False



    if len(documents) < minimum_documents:

        return False



    return True