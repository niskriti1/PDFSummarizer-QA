import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from parse import parse_s3_pdf_to_markdown_table
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

def process_doc(pdf_path):
  
    #check if pdf is already parsed
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  
    md_output_path = os.path.join("output", f"{pdf_name}.md")
    
    if os.path.exists(md_output_path):
      with open(md_output_path, "r", encoding="utf-8") as f:
          data = f.read()
    else:
      data = parse_s3_pdf_to_markdown_table(pdf_path)
    
    documents=[]
    documents.append(Document(page_content=data))
    return documents
  
def summarize(api_key,pdf_path):
  docs = process_doc(pdf_path)

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=100)
  chunks = text_splitter.split_documents(docs)

  llm = ChatGroq(
      model="llama3-70b-8192",
      temperature=0.2,
      api_key=api_key,
      max_tokens=4096
    )

  summarizer_chain = load_summarize_chain(
      llm=llm,
      chain_type="refine",
      verbose=False
  )

  return summarizer_chain.run(chunks)