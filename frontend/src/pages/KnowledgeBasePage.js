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
  CardContent,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { queryKnowledgeBase } from '../services/api';

const KnowledgeBasePage = () => {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setError('');
    setIsSearching(true);
    
    try {
      const response = await queryKnowledgeBase(query);
      setResults(response.results);
    } catch (error) {
      console.error('Error querying knowledge base:', error);
      setError('An error occurred while searching. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Medical Knowledge Base
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Search Medical Information
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Ask questions about medical conditions, symptoms, treatments, or any medical topic.
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="E.g., What are the complications of diabetes?"
            value={query}
            onChange={handleQueryChange}
            onKeyPress={handleKeyPress}
          />
          
          <Button
            variant="contained"
            color="primary"
            onClick={handleSearch}
            disabled={isSearching || !query.trim()}
            startIcon={isSearching ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
          >
            {isSearching ? 'Searching...' : 'Search'}
          </Button>
        </Box>
        
        {error && <Alert severity="error">{error}</Alert>}
      </Paper>
      
      {results && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Search Results
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {results.length > 0 ? (
              <List>
                {results.map((result, index) => (
                  <ListItem key={index} alignItems="flex-start" divider={index < results.length - 1}>
                    <ListItemText
                      primary={`Result ${index + 1}`}
                      secondary={
                        <React.Fragment>
                          <Typography
                            component="span"
                            variant="body2"
                            color="text.primary"
                            sx={{ display: 'inline', fontWeight: 'bold' }}
                          >
                            Relevance: {result.score.toFixed(2)}
                          </Typography>
                          <Typography component="div" variant="body2" sx={{ mt: 1 }}>
                            {result.content}
                          </Typography>
                        </React.Fragment>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Alert severity="info">
                No results found. Try a different query or check if the knowledge base has been populated.
              </Alert>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default KnowledgeBasePage; 