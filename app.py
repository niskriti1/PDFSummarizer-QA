import os
import time
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import qa_prompt_template
from summarizer import summarize
from qaSystem import initialize_retriver,get_context_data


load_dotenv(".env")
api_key = os.getenv("groq_api_key")

st.set_page_config(
    page_title="PDF Summarizer / QA",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

if not api_key:
    st.error("API key not found.")
    st.stop()

st.title("📄 PDF Summarizer / QA Tool")

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- pdf UPLOAD SECTION ----
if not st.session_state.pdf_uploaded:
    with st.container(border=True):
        st.subheader("📤 Upload Your pdf")
        st.markdown("Please upload your PDF to start the conversation.")
        uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

        if uploaded_file:
            with st.spinner("Uploading and processing your PDF..."):
                time.sleep(2)
                os.makedirs("uploaded_pdfs", exist_ok=True)
                file_path = os.path.join("uploaded_pdfs", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.session_state.pdf_uploaded = True
                st.session_state.pdf_path = file_path
            st.success("✅ PDF uploaded and saved successfully!")
            st.rerun()

# Task selection
if "task" not in st.session_state:
    st.session_state.task = None
if "proceed_clicked" not in st.session_state:
    st.session_state.proceed_clicked = False

task = st.radio("Choose what you want to do:", ["Summarize", "QA"], index=0 if st.session_state.task is None else ["Summarize", "QA"].index(st.session_state.task))
st.session_state.task = task

if st.button("Proceed"):
    st.session_state.proceed_clicked = True

if st.session_state.proceed_clicked:
    if st.session_state.pdf_uploaded:
        pdf_path = st.session_state.pdf_path

        # If summarize is chosen
        if task == "Summarize":
            st.subheader("📄 PDF Summarization")
            with st.spinner("Summarizing..."):
                result = summarize(api_key=api_key,pdf_path=pdf_path)
                
            success_placeholder = st.empty()
            success_placeholder.success("✅ Done!")
            st.write(result)
            time.sleep(2)
            success_placeholder.empty()
            
            

        # Else block for QA (you'll fill this)
        else:
            st.subheader("❓ Question Answering")
            try:
                retriever = initialize_retriver(api_key, pdf_path)
            except Exception as e:
                st.error(f"Error initializing retriever: {str(e)}")
                st.stop()
            
            # ---- RAG PIPELINE ----
            def rag_qa(question):
              llm = ChatGroq(
                model="llama3-70b-8192",
                temperature=0.2,
                api_key=api_key
              )
              
              context = get_context_data(retriever,question)
              
              
              prompt = qa_prompt_template.replace("{context}", context).replace("{question}", question)
              
              response = llm.invoke(prompt)
              return response.content

            # ---- CHAT DISPLAY ----
            st.markdown("### 💬 Chat about your pdf")
            # New Chat button
            if st.button("🔄 New Chat"):
                st.session_state.chat_history = []
                st.rerun()
              
            for chat in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.markdown(chat["user"])
                    st.caption(f"{chat['user_time']}")

                with st.chat_message("assistant"):
                    st.markdown(chat["bot"])
                    st.caption(f"{chat['bot_time']}")

            # Input and response generation
            if user_input := st.chat_input("Ask anything..."):
                user_time = datetime.now().strftime("%I:%M %p")
                with st.chat_message("user"):
                    st.markdown(user_input)
                    st.caption(f"{user_time}")

                with st.spinner("Thinking..."):
                    bot_response = rag_qa(user_input)
                    bot_time = datetime.now().strftime("%I:%M %p")

                with st.chat_message("assistant"):
                    st.markdown(bot_response)
                    st.caption(f"{bot_time}")

                # Save both timestamps in chat history
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": bot_response,
                    "user_time": user_time,
                    "bot_time": bot_time
                })
    else:
        st.warning("Please upload a PDF first.")
