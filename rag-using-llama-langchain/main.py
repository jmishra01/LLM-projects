from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate

# Model
MODEL = "llama3"

chain = Ollama(model=MODEL) | StrOutputParser()
embeddings = OllamaEmbeddings()

# Load PDF file
loader = PyPDFLoader("lekl103.pdf")
pages = loader.load_and_split()


template = """
    Answer the question based on the context below.
    If you can't answer the question, reply "I don't know."

    Context: {context}

    Question: {question}
    """

prompt = PromptTemplate.from_template(template)

chain = prompt | chain

print(chain.invoke(
    {
        "context": "The name I was given was Santiago",
        "question": "What's my name?"
    }
))

from langchain_community.vectorstores import DocArrayInMemorySearch

vectorstores = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)

retriver = vectorstores.as_retriever()

print(dir(retriver))
