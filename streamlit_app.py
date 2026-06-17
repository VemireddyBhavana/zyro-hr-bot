import os
import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Set up page configurations
st.set_page_config(page_title="Zyro Dynamics HR Help Desk", page_icon="🏢", layout="wide")

# Custom premium CSS styling for a gorgeous, responsive, glassmorphic look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

    /* Reset font styles to premium fonts */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Main Container Glassmorphism background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(98, 0, 234, 0.05) 0%, rgba(0, 0, 0, 0) 100%),
                    radial-gradient(circle at 90% 80%, rgba(0, 229, 255, 0.03) 0%, rgba(0, 0, 0, 0) 100%);
        background-color: #0d0e12;
        color: #e2e8f0;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #12131a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Premium Sidebar Cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }
    
    /* Chat Bubble Styling */
    .user-bubble {
        background: linear-gradient(135deg, #6c5ce7 0%, #4834d4 100%);
        border-radius: 18px 18px 2px 18px;
        color: white;
        padding: 14px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
        animation: slideIn 0.3s ease-out;
    }
    
    .bot-bubble {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 18px 18px 18px 2px;
        color: #e2e8f0;
        padding: 14px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Tag styles */
    .policy-tag {
        display: inline-block;
        background: rgba(108, 92, 231, 0.15);
        color: #a29bfe;
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.8rem;
        margin-top: 5px;
    }

    /* Green Indicator */
    .indicator {
        height: 10px;
        width: 10px;
        background-color: #00e676;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #00e676;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
col1, col2 = st.columns([1, 12])
with col1:
    st.markdown('<div style="font-size: 3.5rem; margin-top: 15px; filter: drop-shadow(0 0 10px rgba(108, 92, 231, 0.4));">🤖</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<h1 style="margin-bottom: 0px; padding-bottom: 0px;">Zyro Dynamics HR Help Desk</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem; margin-top: 2px;">Your AI agent for HR policy documents and queries</p>', unsafe_allow_html=True)

# Sidebar settings and configuration
with st.sidebar:
    st.markdown('<h3>⚙️ Settings</h3>', unsafe_allow_html=True)
    
    # Check for secrets or env variables, fallback to manual inputs
    groq_api_key = os.environ.get("GROQ_API_KEY")
    langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")
    
    if not groq_api_key:
        groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API Key to authenticate Llama-3.1-8b-instant.")
    else:
        st.markdown('<div class="sidebar-card"><span class="indicator"></span> Groq API Key Loaded</div>', unsafe_allow_html=True)

    if not langchain_api_key:
        langchain_api_key = st.text_input("LangChain API Key (Optional)", type="password", help="Enter your LangChain API Key for tracing and analysis.")
    else:
        st.markdown('<div class="sidebar-card"><span class="indicator"></span> LangChain Key Loaded</div>', unsafe_allow_html=True)

    st.markdown('<h3>📚 Indexed Documents</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-card" style="font-size: 0.85rem; color: #94a3b8;">
        📄 00_Company_Profile.pdf<br>
        📄 01_Employee_Handbook.pdf<br>
        📄 02_Leave_Policy.pdf<br>
        📄 03_Work_From_Home_Policy.pdf<br>
        📄 04_Code_of_Conduct.pdf<br>
        📄 05_Performance_Review_Policy.pdf<br>
        📄 06_Compensation_and_Benefits_Policy.pdf<br>
        📄 07_IT_and_Data_Security_Policy.pdf<br>
        📄 08_Prevention_of_Sexual_Harassment_Policy.pdf<br>
        📄 09_Onboarding_and_Separation_Policy.pdf<br>
        📄 10_Travel_and_Expense_Policy.pdf
    </div>
    """, unsafe_allow_html=True)

# Load the dynamic RAG pipeline
@st.cache_resource
def build_rag_pipeline(g_key, l_key):
    if l_key:
        os.environ["LANGCHAIN_API_KEY"] = l_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "zyro-rag-challenge"
    
    # 1. Load PDFs
    loader = PyPDFDirectoryLoader(".")
    documents = loader.load()
    
    # 2. Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # 3. Vector Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})
    
    # Document routing helper
    def get_target_document(question: str):
        q_lower = question.lower()
        if any(kw in q_lower for kw in ["earned leave", "maternity", "sick leave", "casual leave", "leave entitlement"]):
            return "02_Leave_Policy.pdf"
        elif any(kw in q_lower for kw in ["salary", "payroll", "ctc", "bonus target", "health insurance", "medical insurance", "pf account", "compensation"]):
            return "06_Compensation_and_Benefits_Policy.pdf"
        elif any(kw in q_lower for kw in ["pip", "performance improvement", "annual performance review", "apr timeline", "increment and promotion"]):
            return "05_Performance_Review_Policy.pdf"
        elif any(kw in q_lower for kw in ["work from home", "wfh", "remote"]):
            return "03_Work_From_Home_Policy.pdf"
        return None

    def custom_retriever_func(question: str):
        target_doc = get_target_document(question)
        if target_doc:
            matched_chunks = [c for c in chunks if target_doc in os.path.basename(c.metadata.get("source", ""))]
            if matched_chunks:
                return matched_chunks
        return retriever.invoke(question)

    custom_retriever = RunnableLambda(custom_retriever_func)
    
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", api_key=g_key)
    
    template = """You are an HR Help Desk Assistant for Zyro Dynamics Pvt. Ltd. (also known as Acrux Dynamics). Both names refer to the same company.

Instructions:
1. Answer the question using ONLY the provided context. Do NOT use any outside knowledge or make assumptions.
2. If the context does not contain the answer, or if the question cannot be FULLY and completely answered based on the provided context, you MUST gracefully refuse by saying exactly: "I can only answer HR-related questions from Zyro Dynamics policy documents."
3. Do NOT provide any partial answers or explanations of what is missing. If any part of the question cannot be answered from the context, output only the refusal message.
4. When you find the answer in the context, always include the source document name (e.g. "According to the Leave Policy (02_Leave_Policy.pdf)...").

Context:
{context}

Question: {question}

Answer:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    def format_docs(docs):
        return "\n\n".join(f"Source: {os.path.basename(doc.metadata.get('source', 'Unknown'))}\n{doc.page_content}" for doc in docs)
        
    return {"context": custom_retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

# Chat logic
def ask_bot(question: str, rag_chain):
    if rag_chain:
        try:
            return rag_chain.invoke(question)
        except Exception as e:
            return f"Error executing RAG chain: {e}"
    else:
        return "Groq API Key is required to answer questions dynamically."

# Initialize Session State for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main Layout
if not groq_api_key:
    st.warning("🔑 Please enter your Groq API Key in the sidebar settings to launch the HR agent.")
else:
    try:
        # Load pipeline in background
        rag_chain = build_rag_pipeline(groq_api_key, langchain_api_key)
        
        # Welcome message
        if not st.session_state.messages:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Hello! I am the Zyro Dynamics HR Help Desk Agent. Feel free to ask me any questions regarding leave policies, WFH guidelines, performance reviews, or compensation and benefits!"
            })
            
        # Display Message History
        for msg in st.session_state.messages:
            bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            st.markdown(f'<div class="{bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)
            
        # Chat Input
        if user_prompt := st.chat_input("Ask a question about HR policies..."):
            # Display user message
            st.markdown(f'<div class="user-bubble">{user_prompt}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            
            # Generate response
            with st.spinner("Searching policies and generating answer..."):
                response = ask_bot(user_prompt, rag_chain)
                
            # Display assistant message
            st.markdown(f'<div class="bot-bubble">{response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
    except Exception as e:
        st.error(f"Failed to load the pipeline. Details: {e}")