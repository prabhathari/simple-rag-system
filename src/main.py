# src/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pathlib import Path

from .rag_system import SimpleRAGSystem
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Simple RAG System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = SimpleRAGSystem()

# Ensure uploads directory exists
Path("uploads").mkdir(exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@app.get("/")
def root():
    return {"message": "Simple RAG System API", "status": "running"}

@app.get("/health")
def health_check():
    stats = rag_system.get_stats()
    return {"status": "healthy", "stats": stats}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    
    # Check file type
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process document
    result = rag_system.add_document(file_path)
    
    # Clean up uploaded file
    os.remove(file_path)
    
    return result

@app.post("/query")
def query_documents(request: QueryRequest):
    """Query the document knowledge base"""
    return rag_system.query(request.question, request.top_k)

@app.get("/stats")
def get_system_stats():
    """Get system statistics"""
    return rag_system.get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)