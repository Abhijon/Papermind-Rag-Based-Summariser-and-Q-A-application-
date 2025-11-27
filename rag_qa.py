"""
RAG-based Question Answering Module
This module handles PDF text vectorization and question answering using Gemini
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

class RAGQuestionAnswering:
    def __init__(self):
        """Initialize the RAG QA system"""
        self.vector_store = None
        self.qa_chain = None
        self.embeddings = None
        self.llm = None
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize Gemini LLM
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
            convert_system_message_to_human=True
        )
    
    def create_vector_store(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Create a vector store from the given text
        
        Args:
            text: The text to vectorize (PDF content or summary)
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        
        # Create vector store
        self.vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings
        )
        
        # Create QA chain with custom prompt
        prompt_template = """You are a helpful assistant that answers questions based on the provided context from a PDF document.

Context: {context}

Question: {question}

Instructions:
- Answer the question based ONLY on the information provided in the context
- If the answer cannot be found in the context, say "I cannot find this information in the provided document"
- Be concise but comprehensive
- Use bullet points when listing multiple items
- Cite specific parts of the context when relevant

Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        return len(chunks)
    
    def ask_question(self, question: str) -> dict:
        """
        Ask a question and get an answer based on the vectorized content
        
        Args:
            question: The question to ask
            
        Returns:
            dict with 'answer' and 'source_documents'
        """
        if not self.qa_chain:
            return {
                "answer": "Please upload a PDF first before asking questions.",
                "source_documents": []
            }
        
        try:
            result = self.qa_chain.invoke({"query": question})
            
            return {
                "answer": result["result"],
                "source_documents": [doc.page_content for doc in result.get("source_documents", [])]
            }
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "source_documents": []
            }
    
    def save_vector_store(self, path: str = "temp/vector_store"):
        """Save the vector store to disk"""
        if self.vector_store:
            self.vector_store.save_local(path)
    
    def load_vector_store(self, path: str = "temp/vector_store"):
        """Load a previously saved vector store"""
        try:
            self.vector_store = FAISS.load_local(
                path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Recreate QA chain
            prompt_template = """You are a helpful assistant that answers questions based on the provided context from a PDF document.

Context: {context}

Question: {question}

Instructions:
- Answer the question based ONLY on the information provided in the context
- If the answer cannot be found in the context, say "I cannot find this information in the provided document"
- Be concise but comprehensive
- Use bullet points when listing multiple items
- Cite specific parts of the context when relevant

Answer:"""

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": 4}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def clear_vector_store(self):
        """Clear the current vector store"""
        self.vector_store = None
        self.qa_chain = None


# Global instance
rag_qa = RAGQuestionAnswering()
