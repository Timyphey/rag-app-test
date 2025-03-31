from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate

# LLM
from langchain_ollama.chat_models import ChatOllama
llm = ChatOllama(model="llama3.2:3b")

# Embeddings
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Vector Store
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
client = QdrantClient("http://localhost:6333")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)


prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant. Answer the question based on the context provided.
    If the context does not contain the answer, say "I don't know".
    Answer in german.
    
    Question: {question}
    Context: {context}
    """
)


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    
# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

def invoke_user_question(question: str):
    state = graph.invoke({"question": question})
    return state