from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate

# LLM
from langchain_ollama.chat_models import ChatOllama
#llm = ChatOllama(model="llama3.2:3b")
llm = ChatOllama(model="deepseek-r1:1.5b")
#llm = ChatOllama(model="deepseek-r1:8b")

# Embeddings
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="jina/jina-embeddings-v2-base-de")

# Vector Store
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
client = QdrantClient("http://localhost:6333")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)


generate_answer_prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant. Try to answer the question based on the context provided. 
    If there are answers inside of the context, ignore them.
    If you don't know the answer, say that you don't know the answer.
    Answer in german.
    
    Question: 
    {question}
    
    Context: 
    {context}
    """
)


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    
# Define application steps
def retrieve_context(state: State):
    retrieved_docs = vector_store.similarity_search_with_relevance_scores(state["question"], k=5)
    return {"context": retrieved_docs}

def generate_answer(state: State):
    docs_content = "\n\n".join(doc.page_content for doc, _ in state["context"])
    messages = generate_answer_prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve_context, generate_answer])
graph_builder.add_edge(START, "retrieve_context")
graph = graph_builder.compile()

def invoke_user_question(question: str):
    state = graph.invoke({"question": question})
    return state