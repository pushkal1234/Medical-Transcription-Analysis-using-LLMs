import logging
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextSummarizer:
    """
    A class to handle text summarization using pre-trained models.
    """
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the TextSummarizer with a specific model.
        
        Args:
            model_name (str): Name of the pre-trained model to use.
        """
        logger.info(f"Initializing TextSummarizer with model: {model_name}")
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """
        Load the summarization model and tokenizer if not already loaded.
        """
        if self.model is None or self.tokenizer is None:
            logger.info(f"Loading summarization model and tokenizer: {self.model_name}")
            try:
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                logger.info("Summarization model and tokenizer loaded successfully")
            except Exception as e:
                logger.error(f"Error loading summarization model: {str(e)}")
                raise
    
    def summarize(self, text, max_length=1024, min_length=50, length_penalty=2.0, num_beams=4):
        """
        Summarize the given text.
        
        Args:
            text (str): The text to summarize
            max_length (int): Maximum length of the summary
            min_length (int): Minimum length of the summary
            length_penalty (float): Length penalty for generation
            num_beams (int): Number of beams for beam search
            
        Returns:
            str: Summarized text
        """
        try:
            # Load model if not already loaded
            self.load_model()
            
            logger.info("Summarizing text")
            
            # Truncate text if it's too long for the model
            truncated_text = text[:50000]  # Arbitrary limit to prevent tokenizer errors
            
            # Tokenize and generate summary
            inputs = self.tokenizer(truncated_text, return_tensors="pt", max_length=1024, truncation=True)
            
            # Generate summary
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                length_penalty=length_penalty,
                num_beams=num_beams,
                early_stopping=True
            )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            logger.info("Summarization complete")
            return summary
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise
    
    def summarize_medical_conversation(self, text):
        """
        Specialized method to summarize medical conversations.
        
        Args:
            text (str): The medical conversation text to summarize
            
        Returns:
            str: Summarized medical conversation
        """
        # Add a prefix to guide the model to focus on medical aspects
        prefix = "Summarize the following medical conversation, focusing on symptoms, diagnoses, and treatments: "
        
        # Combine prefix and text
        prefixed_text = prefix + text
        
        # Generate summary with medical focus
        return self.summarize(
            prefixed_text,
            max_length=200,  # Shorter summary for medical conversations
            min_length=30,
            length_penalty=1.5,  # Less penalty for length
            num_beams=4
        )

# Example usage
if __name__ == "__main__":
    summarizer = TextSummarizer()
    sample_text = """
    Doctor: What brings you in today?
    Patient: I've been having severe headaches for the past week, and they're getting worse.
    Doctor: Can you describe the pain?
    Patient: It's a throbbing pain on the right side of my head. Light makes it worse.
    Doctor: Any nausea or vomiting?
    Patient: Yes, I've vomited twice today.
    Doctor: Based on your symptoms, you may be experiencing migraines. Let's discuss treatment options.
    """
    summary = summarizer.summarize_medical_conversation(sample_text)
    print(summary) 