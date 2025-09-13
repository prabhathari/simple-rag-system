# src/llm_client.py
from groq import Groq
import os
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

class LLMClient:
    """Simple LLM client using Groq"""
    
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "llama-3.1-8b-instant" #,"llama-3.1-70b-versatile" 
    
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """Generate answer using query and context documents"""
        
        # Prepare context
        context = "\n".join([
            f"Document {i+1}: {doc['content']}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Create prompt
        prompt = f"""Based on the following context documents, answer the user's question.
If the answer is not in the context, say "I don't have enough information to answer that."

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_summary(self, text: str) -> str:
        """Generate summary of text"""
        prompt = f"Summarize the following text in 2-3 sentences:\n\n{text}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"