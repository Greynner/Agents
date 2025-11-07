import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, StateGraph

try:
    from langchain_text_splitters import CharacterTextSplitter
except ImportError:
    from langchain.text_splitter import CharacterTextSplitter


class QAState(TypedDict, total=False):
    question: str
    context: str
    answer: str


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


def build_graph(retriever, qa_chain):
    graph = StateGraph(QAState)

    def retrieve(state: QAState) -> dict:
        docs = retriever.invoke(state["question"])
        context = format_docs(docs) if docs else ""
        return {"context": context}

    def generate(state: QAState) -> dict:
        context = state.get("context", "")
        if not context.strip():
            return {"answer": "No se encontró información relevante en el contexto proporcionado."}
        answer = qa_chain.invoke(
            {"context": context, "question": state["question"]}
        )
        return {"answer": answer}

    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


def main() -> None:
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    loader = TextLoader("data/document.txt", encoding="utf-8")
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_template(
        """Eres un asistente experto en QA.
Usa el siguiente contexto para responder la pregunta del usuario de forma clara y breve.
Si no encuentras información relevante en el contexto, dilo claramente.

Contexto:
{context}

Pregunta:
{question}"""
    )

    qa_chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    graph = build_graph(retriever, qa_chain)

    question = "¿Qué hace el agente QA?"
    result = graph.invoke({"question": question})
    answer = result.get("answer", "No se pudo generar una respuesta.")

    print("\n=== RESPUESTA ===\n")
    print(answer)


if __name__ == "__main__":
    main()

