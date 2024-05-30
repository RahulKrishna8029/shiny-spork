from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = ""

# Prompt template for summarization
SUMMARIZATION_TEMPLATE = """
Summarize the following text:

{text}
"""

# Prompt template for final answer generation
PROMPT_TEMPLATE = """
Answer the question based only on the following summarized context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Take the query text as input from the user
    query_text = input("Enter the query text: ")

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key="")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB for the relevant chunks.
    results = db.similarity_search_with_relevance_scores(query_text, k=10)
    if len(results) == 0:
        print("Unable to find matching results.")
        return

    # Summarize each chunk
    summarization_model = ChatOpenAI(openai_api_key="")
    summarized_chunks = []

    for doc, score in results:
        chunk_text = doc.page_content
        summarization_prompt_template = ChatPromptTemplate.from_template(SUMMARIZATION_TEMPLATE)
        summarization_prompt = summarization_prompt_template.format(text=chunk_text)
        summarized_chunk = summarization_model.predict(summarization_prompt)
        summarized_chunks.append(summarized_chunk)

    # Combine all summarized chunks into one context
    combined_summary = "\n\n---\n\n".join(summarized_chunks)

    # Generate the final response based on the combined summary
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=combined_summary, question=query_text)

    response_text = summarization_model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
