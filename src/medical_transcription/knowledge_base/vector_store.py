import logging
import os
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MedicalKnowledgeBase:
    """
    A class to handle the medical knowledge base using vector embeddings and FAISS.
    """
    
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the MedicalKnowledgeBase with a specific embedding model.
        
        Args:
            embedding_model_name (str): Name of the embedding model to use.
        """
        logger.info(f"Initializing MedicalKnowledgeBase with embedding model: {embedding_model_name}")
        self.embedding_model_name = embedding_model_name
        self.embeddings = None
        self.faiss_index = None
        self.index_path = "faiss_index"
    
    def load_embeddings(self):
        """
        Load the embedding model if not already loaded.
        """
        if self.embeddings is None:
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            try:
                self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading embedding model: {str(e)}")
                raise
    
    def create_index(self, text, chunk_size=200, chunk_overlap=50):
        """
        Create a FAISS index from the given text.
        
        Args:
            text (str): The text to index
            chunk_size (int): Size of text chunks
            chunk_overlap (int): Overlap between chunks
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load embeddings if not already loaded
            self.load_embeddings()
            
            logger.info(f"Creating FAISS index with chunk size {chunk_size} and overlap {chunk_overlap}")
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )
            chunks = text_splitter.split_text(text)
            
            logger.info(f"Split text into {len(chunks)} chunks")
            
            # Create FAISS index
            self.faiss_index = FAISS.from_texts(chunks, self.embeddings)
            
            # Save index
            self.save_index()
            
            logger.info("FAISS index created and saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating FAISS index: {str(e)}")
            return False
    
    def save_index(self, path=None):
        """
        Save the FAISS index to disk.
        
        Args:
            path (str, optional): Path to save the index. Defaults to self.index_path.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.faiss_index is None:
            logger.error("No FAISS index to save")
            return False
        
        save_path = path or self.index_path
        
        try:
            self.faiss_index.save_local(save_path)
            logger.info(f"FAISS index saved to {save_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
            return False
    
    def load_index(self, path=None, allow_dangerous=True):
        """
        Load a FAISS index from disk.
        
        Args:
            path (str, optional): Path to load the index from. Defaults to self.index_path.
            allow_dangerous (bool): Whether to allow deserialization of the index.
            
        Returns:
            bool: True if successful, False otherwise
        """
        load_path = path or self.index_path
        
        if not os.path.exists(load_path):
            logger.error(f"FAISS index not found at {load_path}")
            return False
        
        try:
            # Load embeddings if not already loaded
            self.load_embeddings()
            
            # Load FAISS index
            self.faiss_index = FAISS.load_local(
                load_path, 
                self.embeddings, 
                allow_dangerous_deserialization=allow_dangerous
            )
            
            logger.info(f"FAISS index loaded from {load_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            return False
    
    def query(self, query_text, k=3):
        """
        Query the knowledge base with the given text.
        
        Args:
            query_text (str): The query text
            k (int): Number of results to return
            
        Returns:
            list: List of relevant documents
        """
        if self.faiss_index is None:
            success = self.load_index()
            if not success:
                logger.error("Failed to load FAISS index for query")
                return []
        
        try:
            logger.info(f"Querying knowledge base with: {query_text}")
            docs = self.faiss_index.similarity_search(query_text, k=k)
            
            logger.info(f"Found {len(docs)} relevant documents")
            return docs
        except Exception as e:
            logger.error(f"Error querying knowledge base: {str(e)}")
            return []
    
    def format_query_results(self, docs):
        """
        Format query results for display.
        
        Args:
            docs (list): List of documents from query
            
        Returns:
            str: Formatted query results
        """
        if not docs:
            return "No relevant information found in the knowledge base."
        
        formatted_results = []
        for i, doc in enumerate(docs):
            formatted_results.append(f"Result {i+1}:\n{doc.page_content}\n")
        
        return "\n".join(formatted_results)

# Example usage
if __name__ == "__main__":
    kb = MedicalKnowledgeBase()
    sample_text = """
    Hypertension, also known as high blood pressure, is a long-term medical condition in which the blood pressure in the arteries is persistently elevated. High blood pressure typically does not cause symptoms. Long-term high blood pressure, however, is a major risk factor for stroke, coronary artery disease, heart failure, atrial fibrillation, peripheral arterial disease, vision loss, chronic kidney disease, and dementia.
    
    Diabetes mellitus, commonly known as diabetes, is a group of metabolic disorders characterized by a high blood sugar level over a prolonged period of time. Symptoms often include frequent urination, increased thirst, and increased appetite. If left untreated, diabetes can cause many complications. Acute complications can include diabetic ketoacidosis, hyperosmolar hyperglycemic state, or death. Serious long-term complications include cardiovascular disease, stroke, chronic kidney disease, foot ulcers, damage to the nerves, damage to the eyes and cognitive impairment.
    """
    
    # Create and save index
    kb.create_index(sample_text)
    
    # Query the knowledge base
    query = "What are the complications of diabetes?"
    results = kb.query(query)
    formatted = kb.format_query_results(results)
    print(formatted) 