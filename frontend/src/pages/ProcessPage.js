import React, { useState } from 'react';
import { 
  Typography, 
  Box, 
  Paper, 
  Button, 
  TextField, 
  CircularProgress,
  Tabs,
  Tab,
  Alert,
  Divider,
  Chip,
  Grid,
  Card,
  CardContent,
  Link
} from '@mui/material';
import AudioRecorder from '../components/AudioRecorder';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import MicIcon from '@mui/icons-material/Mic';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import DownloadIcon from '@mui/icons-material/Download';
import { processData } from '../services/api';

const ProcessPage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [audioFile, setAudioFile] = useState(null);
  const [text, setText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    // Reset state when changing tabs
    setAudioFile(null);
    setText('');
    setError('');
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.includes('audio')) {
        setAudioFile(file);
        setError('');
      } else {
        setError('Please upload an audio file (WAV, MP3, etc.)');
      }
    }
  };

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleAudioRecorded = (blob) => {
    // Create a File object from the Blob
    const file = new File([blob], "recorded_audio.wav", { type: "audio/wav" });
    setAudioFile(file);
    setAudioBlob(blob);
  };

  const handleProcess = async () => {
    setError('');
    setIsProcessing(true);
    
    try {
      let data = {};
      
      if (activeTab === 0 && audioFile) {
        data.audioFile = audioFile;
      } else if (activeTab === 1 && text) {
        data.text = text;
      } else {
        setError('Please provide either an audio file or text to process');
        setIsProcessing(false);
        return;
      }
      
      const response = await processData(data);
      setResult(response);
    } catch (error) {
      console.error('Error processing data:', error);
      setError('An error occurred while processing. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const renderEntityChips = (entities) => {
    if (!entities || entities.length === 0) {
      return <Typography>No entities found</Typography>;
    }
    
    return (
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {entities.map((entity, index) => (
          <Chip
            key={index}
            label={`${entity.term} (${entity.type})`}
            className={`entity-${entity.type}`}
            sx={{ m: 0.5 }}
          />
        ))}
      </Box>
    );
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Process Medical Conversation
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 3 }}>
          <Tab icon={<MicIcon />} label="Audio" />
          <Tab icon={<TextFieldsIcon />} label="Text" />
        </Tabs>
        
        {activeTab === 0 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Upload or Record Audio
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 3 }}>
              <Button
                variant="outlined"
                component="label"
                startIcon={<UploadFileIcon />}
              >
                Upload Audio
                <input
                  type="file"
                  hidden
                  accept="audio/*"
                  onChange={handleFileChange}
                />
              </Button>
              
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <AudioRecorder onRecordingComplete={handleAudioRecorded} />
              </Box>
            </Box>
            
            {audioFile && (
              <Alert severity="success" sx={{ mb: 2 }}>
                Audio file ready: {audioFile.name}
              </Alert>
            )}
          </Box>
        )}
        
        {activeTab === 1 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Enter Medical Conversation Text
            </Typography>
            
            <TextField
              fullWidth
              multiline
              rows={6}
              variant="outlined"
              placeholder="Enter the medical conversation text here..."
              value={text}
              onChange={handleTextChange}
              sx={{ mb: 3 }}
            />
          </Box>
        )}
        
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <Button
          variant="contained"
          color="primary"
          onClick={handleProcess}
          disabled={isProcessing || (activeTab === 0 && !audioFile) || (activeTab === 1 && !text)}
          startIcon={isProcessing ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {isProcessing ? 'Processing...' : 'Process'}
        </Button>
      </Paper>
      
      {result && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Results
          </Typography>
          
          <Grid container spacing={3}>
            {result.transcription && (
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Transcription
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {result.transcription}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            )}
            
            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Medical Entities
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  {renderEntityChips(result.entities)}
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Summary
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="body1">
                    {result.summary}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Clinical Report
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>
                    {result.report}
                  </Typography>
                  
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<DownloadIcon />}
                    component={Link}
                    href={`${process.env.REACT_APP_API_URL || ''}${result.report_url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download PDF Report
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};

export default ProcessPage; 