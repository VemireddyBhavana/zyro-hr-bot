import os
import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Zyro HR Help Desk", page_icon="🏢")
st.title("Zyro Dynamics HR Help Desk 🤖")

with st.sidebar:
    st.header("Settings")
    groq_key = st.text_input("Groq API Key", type="password")
    langchain_key = st.text_input("LangChain API Key", type="password")

if not groq_key:
    st.warning("Please enter your API Keys in the sidebar to continue.")
    st.stop()

os.environ["LANGCHAIN_API_KEY"] = langchain_key
os.environ["LANGCHAIN_TRACING_V2"] = "true" if langchain_key else "false"
os.environ["LANGCHAIN_PROJECT"] = "zyro-rag-challenge"

@st.cache_resource
def build_pipeline():
    loader = PyPDFDirectoryLoader("data") 
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", api_key=groq_key)
    prompt = PromptTemplate(
        template="""You are an HR Help Desk Assistant for Zyro Dynamics Pvt. Ltd.\n
        Answer the employee's question using the context below. \n
        If it cannot be answered from the context, gracefully refuse by saying exactly: "I can only answer HR-related questions from Zyro Dynamics policy documents."\n
        \n
        Context: {context}\n
        Question: {question}\n
        Answer:""",
        input_variables=["context", "question"]
    )
    
    def format_docs(docs):
        return "\n\n".join(f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in docs)
        
    return {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

try:
    with st.spinner("Loading HR Policies..."):
        rag_chain = build_pipeline()
except Exception as e:
    st.error(f"Please ensure your PDFs are in a 'data' folder! Error: {e}")
    st.stop()

if prompt := st.chat_input("Ask a question about Zyro Dynamics HR policies..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching policies..."):
            response = rag_chain.invoke(prompt)
            st.markdown(response)
