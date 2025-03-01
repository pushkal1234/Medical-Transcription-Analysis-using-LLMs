import React, { useState } from 'react';
import { 
  Typography, 
  Box, 
  Paper, 
  TextField, 
  Button, 
  CircularProgress,
  Alert,
  Divider,
  Card,
  CardContent
} from '@mui/material';
import TranslateIcon from '@mui/icons-material/Translate';
import { explainMedicalTerms } from '../services/api';

const ExplainTermsPage = () => {
  const [terms, setTerms] = useState('');
  const [isExplaining, setIsExplaining] = useState(false);
  const [error, setError] = useState('');
  const [explanations, setExplanations] = useState(null);

  const handleTermsChange = (event) => {
    setTerms(event.target.value);
  };

  const handleExplain = async () => {
    if (!terms.trim()) {
      setError('Please enter medical terms to explain');
      return;
    }

    setError('');
    setIsExplaining(true);
    
    try {
      const response = await explainMedicalTerms(terms);
      setExplanations(response.explanations);
    } catch (error) {
      console.error('Error explaining medical terms:', error);
      setError('An error occurred while explaining terms. Please try again.');
    } finally {
      setIsExplaining(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleExplain();
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Explain Medical Terms
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Simplify Medical Terminology
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Enter medical terms or conditions to get simple, easy-to-understand explanations.
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="E.g., hypertension, myocardial infarction, tachycardia"
            value={terms}
            onChange={handleTermsChange}
            onKeyPress={handleKeyPress}
          />
          
          <Button
            variant="contained"
            color="primary"
            onClick={handleExplain}
            disabled={isExplaining || !terms.trim()}
            startIcon={isExplaining ? <CircularProgress size={20} color="inherit" /> : <TranslateIcon />}
          >
            {isExplaining ? 'Explaining...' : 'Explain'}
          </Button>
        </Box>
        
        {error && <Alert severity="error">{error}</Alert>}
      </Paper>
      
      {explanations && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Simplified Explanations
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
              {explanations}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default ExplainTermsPage; 