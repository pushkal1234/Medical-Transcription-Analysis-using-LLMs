import os
import librosa
import numpy as np
import whisper
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """
    A class to handle audio transcription using OpenAI's Whisper model.
    """
    
    def __init__(self, model_size="base"):
        """
        Initialize the WhisperTranscriber with a specific model size.
        
        Args:
            model_size (str): Size of the Whisper model to use. 
                             Options: "tiny", "base", "small", "medium", "large"
        """
        logger.info(f"Initializing WhisperTranscriber with model size: {model_size}")
        self.model = None
        self.model_size = model_size
        
    def load_model(self):
        """
        Load the Whisper model if not already loaded.
        """
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_size}")
            try:
                self.model = whisper.load_model(self.model_size)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading Whisper model: {str(e)}")
                raise
    
    def transcribe(self, audio_file, duration=2520):
        """
        Transcribe audio using Whisper model locally, without internet connection.
        Only processes the first 'duration' seconds.
        
        Args:
            audio_file (str): Path to the audio file
            duration (int): Duration in seconds to process (default: 2520 seconds = 42 minutes)
            
        Returns:
            str: Transcribed text
        """
        try:
            logger.info(f"Loading audio file: {audio_file}")
            
            # Check if file exists
            if not os.path.exists(audio_file):
                logger.error(f"Audio file not found: {audio_file}")
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
            # Load only the specified duration
            audio, sr = librosa.load(audio_file, sr=16000, duration=duration)
            
            duration_minutes = len(audio) / sr / 60
            logger.info(f"Loaded {duration_minutes:.2f} minutes of audio")
            
            # Load Whisper model if not already loaded
            self.load_model()
            
            logger.info("Starting transcription with Whisper...")
            result = self.model.transcribe(audio)
            logger.info("Transcription complete")
            
            return result["text"]
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    transcriber = WhisperTranscriber(model_size="base")
    audio_path = "path/to/your/audio.wav"
    if os.path.exists(audio_path):
        transcription = transcriber.transcribe(audio_path)
        print(transcription)
    else:
        print(f"Audio file not found: {audio_path}") 