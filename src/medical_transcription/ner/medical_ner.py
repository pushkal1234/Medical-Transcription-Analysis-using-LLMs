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
    
    def __init__(self, model_name="yikuan8/Clinical-Longformer-NER"):
        """
        Initialize the MedicalNER with a specific model.
        
        Args:
            model_name (str): Name of the pre-trained model to use.
                Default is a clinical NER model.
                Will fall back to general NER models if specified model fails.
        """
        logger.info(f"Initializing MedicalNER with model: {model_name}")
        self.model_name = model_name
        self.ner_model = None
        # List of fallback models in order of preference
        self.fallback_models = [
            "Jean-Baptiste/roberta-large-ner-english",  # General NER
            "dslim/bert-base-NER",                      # General NER
            "dbmdz/bert-large-cased-finetuned-conll03-english"  # General NER
        ]
        
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
                logger.error(f"Error loading NER model {self.model_name}: {str(e)}")
                
                # Try fallback models
                for fallback_model in self.fallback_models:
                    try:
                        logger.info(f"Attempting to load fallback model: {fallback_model}")
                        self.ner_model = pipeline("ner", model=fallback_model)
                        logger.info(f"Successfully loaded fallback model: {fallback_model}")
                        self.model_name = fallback_model  # Update model name to reflect what's loaded
                        return
                    except Exception as fallback_error:
                        logger.error(f"Error loading fallback model {fallback_model}: {str(fallback_error)}")
                
                # If we get here, all models failed
                raise ValueError("Failed to load any NER model. Please check your internet connection and model availability.")
    
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
            
            # Debug: Log the first few raw entities to understand what's being detected
            if entities:
                logger.info(f"Sample raw entities: {entities[:3]}")
                # Log the structure of the first entity to understand the format
                if len(entities) > 0:
                    logger.info(f"Entity structure: {entities[0].keys()}")
            
            return entities
        except Exception as e:
            logger.error(f"Error during entity extraction: {str(e)}")
            logger.error(f"Error details: {type(e).__name__}")
            raise
    
    def filter_medical_entities(self, entities, threshold=0.5):
        """
        Filter entities to keep only those likely to be medical terms.
        
        Args:
            entities (list): List of entities from the NER model
            threshold (float): Confidence threshold for entities (lowered to 0.5)
            
        Returns:
            list: Filtered list of medical entities
        """
        medical_entities = []
        
        # Debug: Log the entity types we're seeing
        entity_types = set()
        for entity in entities:
            if 'entity' in entity:
                entity_types.add(entity['entity'])
            elif 'entity_group' in entity:
                entity_types.add(entity['entity_group'])
        
        if entity_types:
            logger.info(f"Entity types found: {entity_types}")
        
        for entity in entities:
            # Get the score and entity type based on model output format
            score = entity.get('score', 0)
            entity_type = entity.get('entity', entity.get('entity_group', 'UNKNOWN'))
            word = entity.get('word', entity.get('word', ''))
            
            # Lower the confidence threshold to 0.5
            if score >= threshold:
                # Clean up the entity word
                if isinstance(word, str):
                    word = word.replace('Ġ', '')  # Remove special tokens
                
                if len(word) > 1:  # Allow shorter terms (changed from 2)
                    medical_entities.append({
                        'term': word,
                        'type': entity_type,
                        'score': score,
                        'start': entity.get('start', 0),
                        'end': entity.get('end', 0)
                    })
        
        # Debug: Log how many entities passed the filter
        logger.info(f"After filtering: {len(medical_entities)} entities remain")
        
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
        try:
            all_entities = self.extract_entities(text)
            medical_entities = self.filter_medical_entities(all_entities, threshold)
            
            # Convert any NumPy values to Python native types
            processed_entities = []
            for entity in medical_entities:
                processed_entity = {}
                for key, value in entity.items():
                    if hasattr(value, 'item') and callable(getattr(value, 'item')):
                        # Convert NumPy types to Python native types
                        processed_entity[key] = value.item()
                    else:
                        processed_entity[key] = value
                processed_entities.append(processed_entity)
            
            return processed_entities
        except Exception as e:
            logger.error(f"Error in extract_medical_entities: {str(e)}")
            logger.info("Attempting to use fallback general NER model")
            
            # Try with a general NER model as fallback
            try:
                # Save current model name
                original_model = self.model_name
                self.model_name = "Jean-Baptiste/roberta-large-ner-english"
                self.ner_model = None  # Force reload
                
                # Try extraction with fallback model
                all_entities = self.extract_entities(text)
                medical_entities = self.filter_medical_entities(all_entities, threshold)
                
                # Convert any NumPy values to Python native types
                processed_entities = []
                for entity in medical_entities:
                    processed_entity = {}
                    for key, value in entity.items():
                        if hasattr(value, 'item') and callable(getattr(value, 'item')):
                            processed_entity[key] = value.item()
                        else:
                            processed_entity[key] = value
                    processed_entities.append(processed_entity)
                
                # Restore original model name for future calls
                self.model_name = original_model
                self.ner_model = None
                
                return processed_entities
            except Exception as fallback_error:
                logger.error(f"Fallback model also failed: {str(fallback_error)}")
                return []  # Return empty list as last resort
    
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