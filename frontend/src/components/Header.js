import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  useMediaQuery,
  useTheme,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';

const Header = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [anchorEl, setAnchorEl] = React.useState(null);
  
  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Toolbar>
        <MedicalServicesIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component={RouterLink} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'white' }}>
          Medical Transcription Analysis
        </Typography>
        
        {isMobile ? (
          <>
            <IconButton
              edge="end"
              color="inherit"
              aria-label="menu"
              onClick={handleMenu}
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem component={RouterLink} to="/" onClick={handleClose}>Home</MenuItem>
              <MenuItem component={RouterLink} to="/transcribe" onClick={handleClose}>Transcribe</MenuItem>
              <MenuItem component={RouterLink} to="/process" onClick={handleClose}>Process</MenuItem>
              <MenuItem component={RouterLink} to="/knowledge-base" onClick={handleClose}>Knowledge Base</MenuItem>
              <MenuItem component={RouterLink} to="/explain-terms" onClick={handleClose}>Explain Terms</MenuItem>
            </Menu>
          </>
        ) : (
          <Box>
            <Button color="inherit" component={RouterLink} to="/">Home</Button>
            <Button color="inherit" component={RouterLink} to="/transcribe">Transcribe</Button>
            <Button color="inherit" component={RouterLink} to="/process">Process</Button>
            <Button color="inherit" component={RouterLink} to="/knowledge-base">Knowledge Base</Button>
            <Button color="inherit" component={RouterLink} to="/explain-terms">Explain Terms</Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header; 