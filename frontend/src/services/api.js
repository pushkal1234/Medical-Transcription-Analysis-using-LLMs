import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Transcription API
export const transcribeAudio = async (audioFile) => {
  const formData = new FormData();
  formData.append('file', audioFile);
  
  try {
    const response = await api.post('/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error transcribing audio:', error);
    throw error;
  }
};

// Entity Extraction API
export const extractEntities = async (text) => {
  try {
    const response = await api.post('/extract_entities', { text });
    return response.data;
  } catch (error) {
    console.error('Error extracting entities:', error);
    throw error;
  }
};

// Summarization API
export const summarizeText = async (text) => {
  try {
    const response = await api.post('/summarize', { text });
    return response.data;
  } catch (error) {
    console.error('Error summarizing text:', error);
    throw error;
  }
};

// Report Generation API
export const generateReport = async (entities, summary) => {
  try {
    const response = await api.post('/generate_report', { entities, summary });
    return response.data;
  } catch (error) {
    console.error('Error generating report:', error);
    throw error;
  }
};

// Full Process API
export const processData = async (data) => {
  const formData = new FormData();
  
  if (data.audioFile) {
    formData.append('file', data.audioFile);
  } else if (data.text) {
    formData.append('text', data.text);
  }
  
  try {
    const response = await api.post('/process', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error processing data:', error);
    throw error;
  }
};

// Knowledge Base API
export const queryKnowledgeBase = async (query) => {
  try {
    const response = await api.post('/query_knowledge_base', null, {
      params: { query },
    });
    return response.data;
  } catch (error) {
    console.error('Error querying knowledge base:', error);
    throw error;
  }
};

// Explain Medical Terms API
export const explainMedicalTerms = async (terms) => {
  try {
    const response = await api.post('/explain_medical_terms', null, {
      params: { terms },
    });
    return response.data;
  } catch (error) {
    console.error('Error explaining medical terms:', error);
    throw error;
  }
};

export default {
  transcribeAudio,
  extractEntities,
  summarizeText,
  generateReport,
  processData,
  queryKnowledgeBase,
  explainMedicalTerms,
}; 