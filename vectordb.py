# import chromadb
# from chromadb.utils import embedding_functions

# class ChromaDBWrapper:
#     def __init__(self, persist_path="db"):
#         self.client = chromadb.Client()
#         self.collection = self.client.create_collection("web_content")
#         self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

#     def add_document(self, doc_id: str, content: str):
#         embedding = self.embed_fn(content)
#         self.collection.add(
#             documents=[content],
#             ids=[doc_id],
#             embeddings=[embedding]
#         )

#     def retrieve(self, query: str, top_k=3):
#         embedding = self.embed_fn(query)
#         results = self.collection.query(
#             query_embeddings=[embedding],
#             n_results=top_k
#         )
#         docs = results["documents"][0]
#         return docs
