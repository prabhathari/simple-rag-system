# ui/streamlit_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Page config
st.set_page_config(
    page_title="Simple RAG System",
    page_icon="🤖",
    layout="wide"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🤖 Simple RAG System")
st.write("Upload documents and ask questions about them!")

# Sidebar for stats
with st.sidebar:
    st.header("📊 System Stats")
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            st.metric("Total Documents", stats.get('total_documents', 0))
        else:
            st.error("Could not load stats")
    except:
        st.error("API not available")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=['pdf', 'txt']
    )
    
    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing document..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        st.info(f"Created {result['chunk_count']} chunks")
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.error("Upload failed")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.header("❓ Ask Questions")
    
    question = st.text_input("Enter your question:")
    top_k = st.slider("Number of relevant documents", 1, 10, 3)
    
    if question and st.button("Get Answer"):
        with st.spinner("Searching and generating answer..."):
            try:
                payload = {"question": question, "top_k": top_k}
                response = requests.post(f"{API_URL}/query", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.subheader("🎯 Answer:")
                    st.write(result['answer'])
                    
                    st.subheader(f"📚 Sources (Confidence: {result['confidence']}):")
                    for i, source in enumerate(result['sources']):
                        with st.expander(f"Source {i+1} - Score: {source['score']}"):
                            st.write(f"**File:** {source['source']}")
                            st.write(source['content'])
                else:
                    st.error("Query failed")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sample questions
st.subheader("💡 Try these sample questions:")
st.write("- What is the main topic of the document?")
st.write("- Can you summarize the key points?")
st.write("- What are the important dates mentioned?")