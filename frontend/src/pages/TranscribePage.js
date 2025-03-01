import React, { useState } from 'react';
import { 
  Typography, 
  Box, 
  Paper, 
  Button, 
  CircularProgress,
  Alert,
  Divider,
  Card,
  CardContent
} from '@mui/material';
import AudioRecorder from '../components/AudioRecorder';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { transcribeAudio } from '../services/api';

const TranscribePage = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);

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

  const handleAudioRecorded = (blob) => {
    // Create a File object from the Blob
    const file = new File([blob], "recorded_audio.wav", { type: "audio/wav" });
    setAudioFile(file);
    setAudioBlob(blob);
  };

  const handleTranscribe = async () => {
    if (!audioFile) {
      setError('Please upload or record an audio file');
      return;
    }

    setError('');
    setIsTranscribing(true);
    
    try {
      const response = await transcribeAudio(audioFile);
      setResult(response);
    } catch (error) {
      console.error('Error transcribing audio:', error);
      setError('An error occurred while transcribing. Please try again.');
    } finally {
      setIsTranscribing(false);
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Transcribe Medical Audio
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
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
        
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <Button
          variant="contained"
          color="primary"
          onClick={handleTranscribe}
          disabled={isTranscribing || !audioFile}
          startIcon={isTranscribing ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {isTranscribing ? 'Transcribing...' : 'Transcribe'}
        </Button>
      </Paper>
      
      {result && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Transcription Result
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
              {result.transcription}
            </Typography>
            
            {result.duration_seconds && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Processing time: {result.duration_seconds.toFixed(2)} seconds
              </Typography>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default TranscribePage; 