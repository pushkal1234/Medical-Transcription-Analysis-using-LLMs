import os
import logging
import tempfile
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from datetime import datetime

# Import our modules
from ..transcription.whisper_transcriber import WhisperTranscriber
from ..ner.medical_ner import MedicalNER
from ..summarization.text_summarizer import TextSummarizer
from ..knowledge_base.vector_store import MedicalKnowledgeBase
from ..report_generation.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Transcription API",
    description="API for medical transcription, entity extraction, summarization, and report generation",
    version="1.0.0"
)

# Initialize components
transcriber = WhisperTranscriber()
ner = MedicalNER()
summarizer = TextSummarizer()
kb = MedicalKnowledgeBase()
report_generator = ReportGenerator()

# Create a directory for storing temporary files
os.makedirs("temp", exist_ok=True)

# Define request and response models
class TranscriptionRequest(BaseModel):
    audio_url: Optional[str] = None

class TranscriptionResponse(BaseModel):
    transcription: str
    duration_seconds: float

class EntityExtractionRequest(BaseModel):
    text: str

class EntityExtractionResponse(BaseModel):
    entities: List[Dict[str, Any]]

class SummarizationRequest(BaseModel):
    text: str

class SummarizationResponse(BaseModel):
    summary: str

class ReportGenerationRequest(BaseModel):
    entities: List[Dict[str, Any]]
    summary: str

class ReportGenerationResponse(BaseModel):
    report: str
    report_url: Optional[str] = None

class FullProcessRequest(BaseModel):
    audio_url: Optional[str] = None
    text: Optional[str] = None

class FullProcessResponse(BaseModel):
    transcription: Optional[str] = None
    entities: List[Dict[str, Any]]
    summary: str
    report: str
    report_url: str

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Transcription Analysis Application"}

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Transcribe an audio file to text.
    """
    try:
        # Save uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file_path = temp_file.name
        
        # Write the file content
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
        
        # Transcribe the audio
        start_time = datetime.now()
        transcription = transcriber.transcribe(temp_file_path)
        end_time = datetime.now()
        
        # Calculate duration
        duration_seconds = (end_time - start_time).total_seconds()
        
        # Schedule cleanup of temporary file
        background_tasks.add_task(os.unlink, temp_file_path)
        
        return {
            "transcription": transcription,
            "duration_seconds": duration_seconds
        }
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

@app.post("/extract_entities", response_model=EntityExtractionResponse)
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract medical entities from text.
    """
    try:
        entities = ner.extract_medical_entities(request.text)
        return {"entities": entities}
    except Exception as e:
        logger.error(f"Error during entity extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Entity extraction error: {str(e)}")

@app.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize medical text.
    """
    try:
        summary = summarizer.summarize_medical_conversation(request.text)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")

@app.post("/generate_report", response_model=ReportGenerationResponse)
async def generate_report(request: ReportGenerationRequest):
    """
    Generate a medical report from entities and summary.
    """
    try:
        report = report_generator.generate_report(request.entities, request.summary)
        
        # Generate a unique filename for the report
        report_id = str(uuid.uuid4())
        report_filename = f"temp/report_{report_id}.pdf"
        
        # Save the report as PDF
        report_generator.save_report_as_pdf(report, report_filename)
        
        return {
            "report": report,
            "report_url": f"/download_report/{report_id}"
        }
    except Exception as e:
        logger.error(f"Error during report generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation error: {str(e)}")

@app.get("/download_report/{report_id}")
async def download_report(report_id: str):
    """
    Download a generated report.
    """
    report_filename = f"temp/report_{report_id}.pdf"
    
    if not os.path.exists(report_filename):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=report_filename,
        filename="clinical_report.pdf",
        media_type="application/pdf"
    )

@app.post("/process", response_model=FullProcessResponse)
async def process_full(background_tasks: BackgroundTasks, 
                      file: Optional[UploadFile] = File(None),
                      text: Optional[str] = Form(None)):
    """
    Process audio or text through the entire pipeline.
    """
    try:
        # Step 1: Get transcription (either from audio or directly provided)
        transcription = None
        if file:
            # Save uploaded file to a temporary location
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file_path = temp_file.name
            
            # Write the file content
            with open(temp_file_path, "wb") as f:
                f.write(await file.read())
            
            # Transcribe the audio
            transcription = transcriber.transcribe(temp_file_path)
            
            # Schedule cleanup of temporary file
            background_tasks.add_task(os.unlink, temp_file_path)
        elif text:
            transcription = text
        else:
            raise HTTPException(status_code=400, detail="Either audio file or text must be provided")
        
        # Step 2: Extract entities
        entities = ner.extract_medical_entities(transcription)
        
        # Step 3: Summarize
        summary = summarizer.summarize_medical_conversation(transcription)
        
        # Step 4: Generate report
        report = report_generator.generate_report(entities, summary)
        
        # Step 5: Save report as PDF
        report_id = str(uuid.uuid4())
        report_filename = f"temp/report_{report_id}.pdf"
        report_generator.save_report_as_pdf(report, report_filename)
        
        # Step 6: Create knowledge base (in background)
        background_tasks.add_task(kb.create_index, transcription)
        
        return {
            "transcription": transcription,
            "entities": entities,
            "summary": summary,
            "report": report,
            "report_url": f"/download_report/{report_id}"
        }
    except Exception as e:
        logger.error(f"Error during full processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/query_knowledge_base")
async def query_kb(query: str):
    """
    Query the knowledge base with a question.
    """
    try:
        docs = kb.query(query)
        formatted_results = kb.format_query_results(docs)
        return {"results": formatted_results}
    except Exception as e:
        logger.error(f"Error querying knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Knowledge base query error: {str(e)}")

@app.post("/explain_medical_terms")
async def explain_terms(terms: str):
    """
    Explain medical terms in simple language.
    """
    try:
        explanations = report_generator.explain_medical_terms(terms)
        return {"explanations": explanations}
    except Exception as e:
        logger.error(f"Error explaining medical terms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Term explanation error: {str(e)}")

# Run the API server
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 