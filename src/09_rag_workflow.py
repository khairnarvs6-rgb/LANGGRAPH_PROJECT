
import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langgraph.graph import StateGraph, START, END

# Explicitly load from project root and tests folder
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "tests" / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"


# 1. Load documents.
documents: list[Document] = []

for path in DATA_DIR.glob("*.txt"):
    documents.extend(
        TextLoader(
            str(path),
            encoding="utf-8",
        ).load()
    )

if not documents:
    raise ValueError("Add at least one .txt file to data/.")

# 2. Split documents into chunks.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
)
chunks = splitter.split_documents(documents)

# 3. Create local embeddings.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Create or load the local vector database.
if DB_DIR.exists() and any(DB_DIR.iterdir()):
    vector_store = Chroma(
        collection_name="langgraph_notes",
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )
else:
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="langgraph_notes",
        persist_directory=str(DB_DIR),
    )

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# 5. Configure the Groq model and prompt.
llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    ),
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Answer using the supplied context.
If the context does not contain the answer, say that
the available documents do not provide enough information.

Context:
{context}"""
    ),
    ("human", "{question}"),
])


class RAGState(TypedDict):
    question: str
    context: list[Document]
    answer: str


# 6. Retrieve relevant document chunks.
def retrieve(state: RAGState) -> dict:
    docs = retriever.invoke(state["question"])
    return {"context": docs}


# 7. Generate an answer from the retrieved context.
def generate(state: RAGState) -> dict:
    context_text = "\n\n".join(
        doc.page_content for doc in state["context"]
    )

    response = (prompt | llm).invoke({
        "question": state["question"],
        "context": context_text,
    })

    return {"answer": response.content}


# 8. Build the RAG graph.
builder = StateGraph(RAGState)

builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()


if __name__ == "__main__":
    question = input("Ask your documents: ")

    result = graph.invoke({
        "question": question,
        "context": [],
        "answer": "",
    })

    print("\nRetrieved context:")
    for doc in result["context"]:
        print("-", doc.page_content[:200])

    print("\nAnswer:")
    print(result["answer"])
