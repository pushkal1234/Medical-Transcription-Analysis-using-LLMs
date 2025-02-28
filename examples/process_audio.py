#!/usr/bin/env python3
"""
Example script demonstrating how to use the Medical Transcription Analysis library
to process an audio file and generate a clinical report.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_audio_file(audio_file_path, output_dir=None):
    """
    Process an audio file through the entire pipeline:
    1. Transcribe the audio
    2. Extract medical entities
    3. Generate a summary
    4. Create a clinical report
    5. Save the report as PDF
    
    Args:
        audio_file_path (str): Path to the audio file
        output_dir (str, optional): Directory to save the output files
    
    Returns:
        dict: Results of the processing pipeline
    """
    try:
        from medical_transcription.transcription.whisper_transcriber import WhisperTranscriber
        from medical_transcription.ner.medical_ner import MedicalNER
        from medical_transcription.summarization.text_summarizer import TextSummarizer
        from medical_transcription.report_generation.report_generator import ReportGenerator
        
        # Create output directory if it doesn't exist
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = "."
            
        # Step 1: Transcribe the audio
        logger.info(f"Transcribing audio file: {audio_file_path}")
        transcriber = WhisperTranscriber()
        transcription = transcriber.transcribe(audio_file_path)
        
        # Save transcription to file
        transcription_path = os.path.join(output_dir, "transcription.txt")
        with open(transcription_path, "w") as f:
            f.write(transcription)
        logger.info(f"Transcription saved to: {transcription_path}")
        
        # Step 2: Extract medical entities
        logger.info("Extracting medical entities")
        ner = MedicalNER()
        entities = ner.extract_medical_entities(transcription)
        formatted_entities = ner.format_entities_for_report(entities)
        
        # Step 3: Generate a summary
        logger.info("Generating summary")
        summarizer = TextSummarizer()
        summary = summarizer.summarize_medical_conversation(transcription)
        
        # Save summary to file
        summary_path = os.path.join(output_dir, "summary.txt")
        with open(summary_path, "w") as f:
            f.write(summary)
        logger.info(f"Summary saved to: {summary_path}")
        
        # Step 4: Generate a clinical report
        logger.info("Generating clinical report")
        report_generator = ReportGenerator()
        report = report_generator.generate_report(formatted_entities, summary)
        
        # Step 5: Save the report as PDF
        report_path = os.path.join(output_dir, "clinical_report.pdf")
        report_generator.save_report_as_pdf(report, report_path)
        logger.info(f"Clinical report saved to: {report_path}")
        
        return {
            "transcription": transcription,
            "entities": entities,
            "summary": summary,
            "report": report,
            "files": {
                "transcription": transcription_path,
                "summary": summary_path,
                "report": report_path
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise

def main():
    """Main entry point for the example script."""
    parser = argparse.ArgumentParser(description="Process a medical audio file")
    parser.add_argument("audio_file", help="Path to the audio file to process")
    parser.add_argument("--output-dir", help="Directory to save output files")
    args = parser.parse_args()
    
    try:
        results = process_audio_file(args.audio_file, args.output_dir)
        logger.info("Processing completed successfully")
        
        # Print a summary of the results
        print("\n" + "="*50)
        print("PROCESSING SUMMARY")
        print("="*50)
        print(f"Transcription length: {len(results['transcription'])} characters")
        print(f"Medical entities found: {len(results['entities'])}")
        print(f"Summary length: {len(results['summary'])} characters")
        print("\nOutput files:")
        for file_type, file_path in results['files'].items():
            print(f"- {file_type}: {file_path}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 