# 🎯 Simple RAG + Vector Database Project

## 📁 Project Structure
```
simple-rag-system/
├── src/
│   ├── vector_db.py          # Vector database operations
│   ├── rag_system.py         # RAG implementation
│   ├── document_loader.py    # Document processing
│   ├── llm_client.py         # LLM integration (Groq)
│   └── main.py               # FastAPI app
├── ui/
│   └── streamlit_app.py      # Simple UI
├── data/
│   └── documents/            # Sample documents
├── requirements.txt
├── .env.example
├── docker-compose.yml
└── README.md
```

## 🚀 Step-by-Step Implementation

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone your-repo
cd simple-rag-system

# 2. Install dependencies
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
pip install uv
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env
# Add your GROQ_API_KEY
#Set up your Groq API Key
First, get your API key and update .env:

Go to https://console.groq.com/keys
Create account and get API key
Update .env file:

GROQ_API_KEY=your_actual_groq_api_key_here

# 4. Run API
python -m uvicorn src.main:app --reload

# 5. Run UI (in another terminal)
streamlit run ui/streamlit_app.py
```

## 🎯 Key Concepts Demonstrated

1. **Vector Database**: ChromaDB for storing embeddings
2. **Embeddings**: Sentence-transformers for text vectorization
3. **RAG Pipeline**: Retrieve → Generate workflow
4. **Document Processing**: PDF/TXT chunking with metadata
5. **LLM Integration**: Groq API for generation
6. **REST API**: FastAPI with proper endpoints
7. **UI**: Streamlit for user interaction

This simple implementation covers all RAG and vector database fundamentals while remaining easy to understand and extend!