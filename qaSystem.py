import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import SelfQueryRetriever
from langchain_groq import ChatGroq
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.schema import Document
from parse import parse_s3_pdf_to_markdown_table



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
    documents.append(Document(
		page_content=data,
		metadata={
			"filename": "chapter-2.md",
			"folder": "output/",
			"page_no": 1 
			}
	))
    return documents
  
def chunk_data(docs):
  splitter = RecursiveCharacterTextSplitter(chunk_size = 2000,chunk_overlap = 100)
    
  return splitter.split_documents(docs)

def initialize_retriver(api_key,pdf_path):
  docs = process_doc(pdf_path)
  documents = chunk_data(docs)
  
  #embedding model
  embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
  
  #initialize llm model
  llm = ChatGroq(
		model="llama3-70b-8192",
		temperature=0.2,
		api_key=api_key
	)
  
  #initialize vectorstore
  vectorstore=Chroma.from_documents(
    documents=documents,
    embedding=embedding
  )
  
  #define metadata
  metadata_field_info = [
    AttributeInfo(
        name="filename",
        description="The name of the document PDF file",
        type="string"
    ),
    AttributeInfo(
        name="page_no",
        description="The page number where the chunk appears",
        type="integer"
    )]
  
  #retriever
  return SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    metadata_field_info=metadata_field_info,
    search_kwargs={'k':3},
    document_contents = "Content from PDFs"
  )
  
def get_context_data(retriever,question):
  docs=retriever.get_relevant_documents(question)
  
  if docs is None:
    return ""
  
  context = "\n".join(doc.page_content for doc in docs)
  return context