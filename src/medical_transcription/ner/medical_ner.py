import logging
from transformers import pipeline
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MedicalNER:
    """
    A class to handle medical named entity recognition using pre-trained models.
    """
    
    def __init__(self, model_name="Jean-Baptiste/roberta-large-ner-english"):
        """
        Initialize the MedicalNER with a specific model.
        
        Args:
            model_name (str): Name of the pre-trained model to use.
        """
        logger.info(f"Initializing MedicalNER with model: {model_name}")
        self.model_name = model_name
        self.ner_model = None
        
    def load_model(self):
        """
        Load the NER model if not already loaded.
        """
        if self.ner_model is None:
            logger.info(f"Loading NER model: {self.model_name}")
            try:
                self.ner_model = pipeline("ner", model=self.model_name)
                logger.info("NER model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading NER model: {str(e)}")
                raise
    
    def extract_entities(self, text):
        """
        Extract named entities from the given text.
        
        Args:
            text (str): The text to extract entities from
            
        Returns:
            list: List of extracted entities with their types, scores, and positions
        """
        try:
            # Load model if not already loaded
            self.load_model()
            
            logger.info("Extracting entities from text")
            entities = self.ner_model(text)
            logger.info(f"Extracted {len(entities)} entities")
            
            return entities
        except Exception as e:
            logger.error(f"Error during entity extraction: {str(e)}")
            raise
    
    def filter_medical_entities(self, entities, threshold=0.7):
        """
        Filter entities to keep only those likely to be medical terms.
        
        Args:
            entities (list): List of entities from the NER model
            threshold (float): Confidence threshold for entities
            
        Returns:
            list: Filtered list of medical entities
        """
        medical_entities = []
        
        for entity in entities:
            # Keep entities with high confidence
            if entity['score'] >= threshold:
                # Check if entity is likely a medical term
                # This is a simple heuristic and can be improved
                if (entity['entity'] == 'MISC' or 
                    entity['entity'] == 'ORG' or 
                    entity['entity'] == 'I-MISC' or
                    entity['entity'] == 'B-MISC'):
                    
                    # Clean up the entity word
                    word = entity['word'].replace('Ġ', '')  # Remove special tokens
                    
                    if len(word) > 2:  # Ignore very short terms
                        medical_entities.append({
                            'term': word,
                            'type': entity['entity'],
                            'score': entity['score'],
                            'start': entity['start'],
                            'end': entity['end']
                        })
        
        return medical_entities
    
    def extract_medical_entities(self, text, threshold=0.7):
        """
        Extract and filter medical entities from text.
        
        Args:
            text (str): The text to extract medical entities from
            threshold (float): Confidence threshold for entities
            
        Returns:
            list: List of medical entities
        """
        all_entities = self.extract_entities(text)
        medical_entities = self.filter_medical_entities(all_entities, threshold)
        
        return medical_entities
    
    def format_entities_for_report(self, entities):
        """
        Format extracted entities for inclusion in a medical report.
        
        Args:
            entities (list): List of extracted medical entities
            
        Returns:
            str: Formatted string of medical entities
        """
        if not entities:
            return "No significant medical entities detected."
        
        # Group entities by type
        entity_groups = {}
        for entity in entities:
            entity_type = entity['type']
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(entity['term'])
        
        # Format the output
        formatted_output = []
        for entity_type, terms in entity_groups.items():
            # Remove duplicates while preserving order
            unique_terms = []
            for term in terms:
                if term not in unique_terms:
                    unique_terms.append(term)
            
            formatted_output.append(f"{entity_type}: {', '.join(unique_terms)}")
        
        return "\n".join(formatted_output)

# Example usage
if __name__ == "__main__":
    ner = MedicalNER()
    sample_text = "The patient has hypertension and diabetes. They are currently taking lisinopril and metformin."
    entities = ner.extract_medical_entities(sample_text)
    formatted = ner.format_entities_for_report(entities)
    print(formatted) 