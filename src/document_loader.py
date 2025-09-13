# src/document_loader.py
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
import re

class SimpleDocumentLoader:
    """Simple document loader for PDF and TXT files"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def load_pdf(self, file_path: str) -> str:
        """Load PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def load_txt(self, file_path: str) -> str:
        """Load text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        # Clean text
        text = re.sub(r'\s+', ' ', text.strip())
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find end position
            end = start + self.chunk_size
            
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Try to break at sentence or word boundary
            break_point = text.rfind('.', start, end)
            if break_point == -1:
                break_point = text.rfind(' ', start, end)
            if break_point == -1:
                break_point = end
            
            chunks.append(text[start:break_point])
            start = break_point - self.overlap
        
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def load_and_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """Load file and return chunks with metadata"""
        file_path = Path(file_path)
        
        # Load based on file extension
        if file_path.suffix.lower() == '.pdf':
            content = self.load_pdf(str(file_path))
        elif file_path.suffix.lower() == '.txt':
            content = self.load_txt(str(file_path))
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Create chunks
        chunks = self.chunk_text(content)
        
        # Add metadata
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                'content': chunk,
                'metadata': {
                    'source': str(file_path),
                    'chunk_id': i,
                    'total_chunks': len(chunks),
                    'file_type': file_path.suffix[1:]
                }
            })
        
        return result