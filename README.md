# 📄 PDF QA + Summarizer System (RAG-powered)

A Question Answering and Summarization system that enables users to **upload their pdf (PDF)** and then **either ask questions** or **generate a summary** of it. This application is powered by **Retrieval-Augmented Generation (RAG)** and a **language model** to provide intelligent, context-aware responses and summaries.

---

## 🚀 Features

- 🧠 Ask any question about your uploaded pdf
- ✨ Get an AI-generated summary of your pdf
- 📄 Supports PDF uploads
- 🔍 Embedding + Vector Store for fast information retrieval
- 🤖 Powered by a language model (Gemini 1.5 Flash)
- 💬 Interactive and easy-to-use **Streamlit UI**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **RAG Components**:
  - `LangChain`
  - `HuggingFaceEmbeddings`
  - `ChromaDB` (Vector Store)
  - `Gemini` (LLM)
- **PDF Parsing**: `PyMuPDF (fitz)`
- **Utilities**: `dotenv`, `os`, `datetime`, etc.

---

## 🧑‍💻 How It Works

1. **Upload PDF** (`.pdf`)
2. pdf text is **parsed** using llamaparse
3. Text is **split into chunks**
4. Each chunk is **embedded** using HuggingFace Embeddings
5. Chunks are stored in **ChromaDB vector store**
6. User selects:
   - **QA Mode**: Ask a question → relevant chunks are retrieved → Groq answers
   - **Summary Mode**: All chunks are summarized using Groq

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/niskriti1/PDFSummarizer-QA.git
```

# 2. (Optional) Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

# 3. Install dependencies

```
pip install -r requirements.txt
```

# 4. Run the app

```
streamlit run app.py
```
