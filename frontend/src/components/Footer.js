import React from 'react';
import { Box, Typography, Link, Container } from '@mui/material';

const Footer = () => {
  return (
    <Box component="footer" sx={{ bgcolor: '#f5f5f5', py: 3, mt: 'auto' }}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {'© '}
          {new Date().getFullYear()}
          {' '}
          <Link color="inherit" href="https://github.com/yourusername/Medical-Transcription-Analysis-using-LLMs">
            Medical Transcription Analysis
          </Link>
          {' - Powered by AI'}
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          This application is for demonstration purposes only and should not be used for medical diagnosis.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer; 