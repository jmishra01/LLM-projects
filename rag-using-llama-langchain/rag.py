from IPython.display import Markdown, display

from operator import itemgetter

from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate

# Model
MODEL = "llama2"

chain = Ollama(model=MODEL) | StrOutputParser()
embeddings = OllamaEmbeddings()

# Load PDF file
filename = "Docker Deep Drive.pdf"
loader = PyPDFLoader(filename)
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
        "context": "The name I was given was Jitendra",
        "question": "What's my name?"
    }
))

from langchain_community.vectorstores import DocArrayInMemorySearch

vectorstores = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)

retriever = vectorstores.as_retriever()

from langchain_community.vectorstores import FAISS

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(loader.load())

faiss_db = FAISS.from_documents(texts, embedding=embeddings)

retriever = faiss_db.as_retriever()



chain_retriever = ({
    "context": itemgetter("question") | retriever,
    "question": itemgetter("question")
} | chain)

resp = chain_retriever.invoke({"question": "How many types of networking possible in the docker?"})

display(Markdown(resp))
