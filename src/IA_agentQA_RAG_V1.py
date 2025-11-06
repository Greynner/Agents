import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

try:
    from langchain_text_splitters import CharacterTextSplitter
except ImportError:
    from langchain.text_splitter import CharacterTextSplitter


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


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

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    question = "¿Qué hace el agente QA?"
    response = chain.invoke(question)

    print("\n=== RESPUESTA ===\n")
    print(response)


if __name__ == "__main__":
    main()