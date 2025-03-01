import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardActions, 
  Button,
  Paper
} from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import DescriptionIcon from '@mui/icons-material/Description';
import SearchIcon from '@mui/icons-material/Search';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import SettingsIcon from '@mui/icons-material/Settings';

const HomePage = () => {
  return (
    <Box sx={{ py: 4 }}>
      <Paper 
        elevation={0} 
        sx={{ 
          p: 4, 
          mb: 4, 
          textAlign: 'center',
          background: 'linear-gradient(45deg, #1976d2 30%, #21CBF3 90%)',
          color: 'white'
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Medical Transcription Analysis
        </Typography>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Transform medical conversations into structured clinical reports
        </Typography>
        <Button 
          variant="contained" 
          color="secondary" 
          size="large" 
          component={RouterLink} 
          to="/process"
          sx={{ mt: 2 }}
        >
          Get Started
        </Button>
      </Paper>

      <Typography variant="h4" component="h2" gutterBottom sx={{ mb: 3 }}>
        Features
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <MicIcon fontSize="large" color="primary" />
              </Box>
              <Typography gutterBottom variant="h5" component="h2" align="center">
                Transcription
              </Typography>
              <Typography>
                Convert medical audio recordings into accurate text using advanced speech recognition technology.
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary" component={RouterLink} to="/transcribe">
                Try Transcription
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <DescriptionIcon fontSize="large" color="primary" />
              </Box>
              <Typography gutterBottom variant="h5" component="h2" align="center">
                Report Generation
              </Typography>
              <Typography>
                Generate structured clinical reports from transcribed conversations with medical entity extraction.
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary" component={RouterLink} to="/process">
                Generate Reports
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <SearchIcon fontSize="large" color="primary" />
              </Box>
              <Typography gutterBottom variant="h5" component="h2" align="center">
                Knowledge Base
              </Typography>
              <Typography>
                Query medical information and get relevant answers based on the processed conversations.
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary" component={RouterLink} to="/knowledge-base">
                Search Knowledge
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <HelpOutlineIcon fontSize="large" color="primary" />
              </Box>
              <Typography gutterBottom variant="h5" component="h2" align="center">
                Medical Term Explanations
              </Typography>
              <Typography>
                Get simple explanations for complex medical terms to improve patient understanding.
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary" component={RouterLink} to="/explain-terms">
                Explain Terms
              </Button>
            </CardActions>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default HomePage; 