from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from smolagents import Tool
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


def load_document(filename: str) -> Chroma:
    chroma_dir = "./chroma_db"
    if os.path.exists(chroma_dir):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)
        return vector_store
    docs_processed = []
    if filename.endswith(".json"):
        import json
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        source_docs = [
            Document(page_content=f"Title: {doc["title"]},\n Body: {doc["body"]}", metadata={"source": doc["url"]}) for
            doc in data]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        docs_processed = text_splitter.split_documents(source_docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(docs_processed, embeddings, persist_directory=chroma_dir)
    return vector_store


class RetrieverTool(Tool):
    name = "retriever"
    description = (
        "Uses semantic search to retrieve the parts of documentation that could be most relevant to answer your query."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, vector_store, **kwargs):
        super().__init__(**kwargs)
        self.vector_store = vector_store

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"
        docs = self.vector_store.similarity_search(query, k=5)
        return "\nRetrieved documents:\n" + "".join(
            [f'\n\n===== Document {i} =====\n content: {doc.page_content}'
             + (f',\n article: {doc.metadata["source"]}\n' if "source" in doc.metadata else "\n")
             for i, doc in enumerate(docs)])


rag_tool = RetrieverTool(load_document("dokai/hc_articles.json"))
