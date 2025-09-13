# src/rag_system.py
from typing import List, Dict, Any
from .vector_db import VectorDatabase
from .document_loader import SimpleDocumentLoader
from .llm_client import LLMClient

class SimpleRAGSystem:
    """Simple RAG (Retrieval-Augmented Generation) system"""
    
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.doc_loader = SimpleDocumentLoader()
        self.llm_client = LLMClient()
        print("✅ RAG System initialized")
    
    def add_document(self, file_path: str) -> Dict[str, Any]:
        """Add a document to the knowledge base"""
        try:
            # Load and chunk document
            chunks_data = self.doc_loader.load_and_chunk(file_path)
            
            # Extract texts and metadata
            texts = [chunk['content'] for chunk in chunks_data]
            metadatas = [chunk['metadata'] for chunk in chunks_data]
            
            # Add to vector database
            doc_ids = self.vector_db.add_documents(texts, metadatas)
            
            return {
                'success': True,
                'message': f'Added document with {len(texts)} chunks',
                'chunk_count': len(texts),
                'document_ids': doc_ids
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error adding document: {str(e)}'
            }
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            # Step 1: Retrieve relevant documents
            relevant_docs = self.vector_db.search(question, top_k=top_k)
            
            if not relevant_docs:
                return {
                    'answer': "No relevant documents found in the knowledge base.",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # Step 2: Generate answer using LLM
            answer = self.llm_client.generate_answer(question, relevant_docs)
            
            # Step 3: Prepare sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    'content': doc['content'][:200] + "...",  # Truncate for display
                    'source': doc['metadata'].get('source', 'Unknown'),
                    'score': round(doc['score'], 3)
                })
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': round(relevant_docs[0]['score'], 3) if relevant_docs else 0.0
            }
            
        except Exception as e:
            return {
                'answer': f"Error processing query: {str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return self.vector_db.get_stats()