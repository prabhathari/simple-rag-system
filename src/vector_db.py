# src/vector_db.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import uuid

class VectorDatabase:
    """Simple vector database using ChromaDB"""
    
    def __init__(self, collection_name: str = "documents"):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print(f"✅ Vector DB initialized with collection: {collection_name}")
    
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None):
        """Add documents to vector database"""
        if not texts:
            return
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Generate IDs
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas or [{}] * len(texts),
            ids=ids
        )
        
        print(f"✅ Added {len(texts)} documents to vector database")
        return ids
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # Format results
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': 1 - results['distances'][0][i],  # Convert distance to similarity
                'id': results['ids'][0][i]
            })
        
        return documents
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }