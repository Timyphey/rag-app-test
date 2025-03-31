# Embeddings
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Vector Store
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from langchain_community.document_loaders import PyPDFLoader

client = QdrantClient("http://localhost:6333")
client.create_collection(
    collection_name="test",
    vectors_config={"size": 1024, "distance": "Cosine"}
)
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)

# embed pdfs from /pdf
# Load PDF files from the /pdf folder
pdf_folder = "./pdf"
pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

# Load and combine all PDF documents
documents = []
for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    documents.extend(loader.load())

# Split documents into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)
print(f"Total number of chunks: {len(split_docs)}")

# Embed the chunks into the QdrantVectorStore
vector_store.add_documents(split_docs)

# Retrieve documents using a query
query = "What is this project about??"
retrieved_docs = vector_store.similarity_search_with_relevance_scores(query, k=3)

# Print the found documents
for i, doc in enumerate(retrieved_docs, start=1):
    print(f"Document {i}:")
    print(doc)
    print("-" * 80)