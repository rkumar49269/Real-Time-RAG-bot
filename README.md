# 🤖 Real-Time RAG Assistant (Local Llama 3)

A privacy-first, context-aware AI assistant that browses the live web to answer questions. Built with **LangChain**, **Ollama**, and **Streamlit**.

https://drive.google.com/file/d/1S-kRCFBTA_9QegOBSlZSIVPF0JS3H024/view

## 💡 The Problem & Solution
Standard LLMs (like Llama 3) have a knowledge cutoff—they don't know today's news. 
Standard RAG bots can search the web, but they often fail at **follow-up questions** (e.g., asking "Who is he?" after mentioning Elon Musk).

**My Solution:**
I engineered a **History-Aware RAG Pipeline** that acts as a cognitive bridge:
1.  **Intercepts** user questions.
2.  **Rewrites** them using conversation history (e.g., "Who is he?" $\rightarrow$ "Who is Elon Musk?").
3.  **Searches** the live web using DuckDuckGo.
4.  **Synthesizes** an answer using Llama 3.

## 🚀 Try It Now (Google Colab)
You can run this entire project in your browser using Google's free GPU.

1. Open Google Colab.
2. Clone this repo:
   ```python
   !git clone [https://github.com/rkumar49269/Real-Time-RAG-bot.git](https://github.com/rkumar49269/Real-Time-RAG-bot.git)
   %cd Real-Time-RAG-bot

   OR

   YOU CAN DIRECTLY DOWNLOAD THE COLAB(.ipynb) FILE AND RUN IT ON THE GOOGLE COLAB TO EXPERIENCE THE REAL TIME CHAT BOT.

   NOTE:- Use google colabs GPU instead of just CPU which took year to respond.