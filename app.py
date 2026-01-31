import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Page Config ---
st.set_page_config(page_title="Real-Time AI Assistant", page_icon="🤖")
st.title("🤖 Real-Time Web RAG Assistant")

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("Settings")
    model_id = st.selectbox("Select Model", ["llama3:8b", "mistral"])
    st.write("This assistant searches the web in real-time to answer your questions.")

# --- Initialize Session State (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Initialize Tools & Model ---
# We cache resources to avoid reloading model on every interaction
@st.cache_resource
def get_engine():
    llm = Ollama(model="llama3:8b")
    search = DuckDuckGoSearchRun()
    return llm, search

llm, search = get_engine()

# --- Chains ---
# 1. Query Rewriter (History Aware)
rewrite_prompt = ChatPromptTemplate.from_template("""
Given the conversation history and a follow-up question, rephrase the
follow-up question to be a standalone search query.
History: {history}
Question: {question}
Standalone Query:
""")
rewrite_chain = rewrite_prompt | llm | StrOutputParser()

# 2. Answer Generator
answer_prompt = ChatPromptTemplate.from_template("""
Answer the question based *only* on the context below.
Context: {context}
Question: {question}
""")
answer_chain = answer_prompt | llm | StrOutputParser()

# --- Chat Interface ---
# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask me anything..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Process Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking & Searching...")

        try:
            # Build history string
            history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])

            # Generate Search Query
            search_query = rewrite_chain.invoke({"history": history_str, "question": prompt})

            # Perform Search
            search_results = search.run(search_query)

            # Generate Answer
            full_response = answer_chain.invoke({"context": search_results, "question": prompt})

            # Display Response
            message_placeholder.markdown(full_response)

            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            message_placeholder.markdown(f"Error: {e}")