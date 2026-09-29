import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Define prompt
system_prompt = (
    "You are a helpful assistant answering questions based on a Node.js book. "
    "Use the following pieces of retrieved context to answer the user's question. "
    "If the answer is not in the context, just say that you don't know.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}"),
])

def process_query(query: str) -> str:
    print(f"Searching chunks for: {query}")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = QdrantVectorStore.from_existing_collection(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        collection_name=os.getenv("QDRANT_COLLECTION", "nodejs_book"),
        embedding=embeddings,
    )
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    chain = prompt | llm | StrOutputParser()

    # Retrieve similar chunks (top 4 by default)
    search_results = vector_store.similarity_search(query=query, k=4)

    # Format document contents into a single string
    context = "\n\n---\n\n".join(doc.page_content for doc in search_results)

    # Invoke the model chain with context and query
    response = chain.invoke({
        "context": context,
        "query": query,
    })

    return response


if __name__ == "__main__":
    answer = process_query("What is event-driven architecture?")
    print(answer)