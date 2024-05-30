from langchain.embeddings.openai import OpenAIEmbeddings

def get_embedding_function():
    # Replace with your OpenAI API key
    openai_api_key = ""

    embeddings = OpenAIEmbeddings(
        api_key=openai_api_key,
        model="gpt-3.5-turbo"  # Specify the OpenAI model to use for embeddings
    )
    return embeddings
