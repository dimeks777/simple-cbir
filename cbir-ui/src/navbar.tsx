import React, { useState } from 'react';
import { AppBar, Button, IconButton, Modal, Paper, Toolbar, Typography, useTheme } from "@mui/material";
import InfoIcon from '@mui/icons-material/Info';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import ImageSearchIcon from '@mui/icons-material/ImageSearch';
import { ColorModeContext } from './App';


const MyAppBar: React.FC = () => {
    const [ aboutModalOpen, setAboutModalOpen ] = useState(false);
    const theme = useTheme();
    const colorMode = React.useContext(ColorModeContext);
    const handleAboutOpen = () => {
        setAboutModalOpen(true);
    };

    const handleAboutClose = () => {
        setAboutModalOpen(false);
    };

    return (
      <AppBar position="static">
          <Toolbar>
              <ImageSearchIcon sx={{ fontSize: 40, mr: 2 }}/> {/* Add the icon next to the title */}
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                  Simple CBIR
              </Typography>
              <IconButton color="inherit" onClick={handleAboutOpen}>
                  <InfoIcon/>
              </IconButton>
              <IconButton sx={{ ml: 1 }} onClick={colorMode.toggleColorMode} color="inherit">
                  {theme.palette.mode === 'dark' ? <Brightness7Icon/> : <Brightness4Icon/>}
              </IconButton>
              <Modal
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
                open={aboutModalOpen}
                onClose={handleAboutClose}
                aria-labelledby="about-modal-title"
                aria-describedby="about-modal-description"
              >
                  <Paper sx={{
                      backgroundColor: theme.palette.background.paper,
                      boxShadow: theme.shadows[5],
                      padding: theme.spacing(2, 4, 3),
                  }}>
                      <h2 id="about-modal-title">Інформація про автора</h2>
                      <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                          {`Міщенко Дмитро \nКН-Н922б`}
                      </Typography>
                      <Button sx={{ marginTop: '10px' }} variant="outlined" color="primary" onClick={handleAboutClose}>
                          Close
                      </Button>
                  </Paper>
              </Modal>
          </Toolbar>
      </AppBar>
    );
};

export default MyAppBar;
