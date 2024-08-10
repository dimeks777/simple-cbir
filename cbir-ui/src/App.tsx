import React, { createContext, useMemo, useState } from 'react';
import Container from '@mui/material/Container';
import UploadCard from './UploadCard';
import ImageGrid from './ImageGrid';
import axios from 'axios';
import Box from '@mui/material/Box';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import "@fontsource/roboto";
import MyAppBar from './navbar';


interface ImageResponse {
    similar_images_uris: string[]
}

export const ColorModeContext = createContext({
    toggleColorMode: () => {
    }
});


const App: React.FC = () => {
    const [ images, setImages ] = useState<string[]>([]);

    const [ mode, setMode ] = useState<'light' | 'dark'>('dark');
    const colorMode = useMemo(
      () => ({
          toggleColorMode: () => {
              setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
          },
      }),
      [],
    );

    const theme = useMemo(
      () =>
        createTheme({
            palette: {
                mode,
                ...(mode === 'light'
                  ? {
                      // background: {
                      //   default: yellow[50],
                      //   paper: yellow[50],
                      // },
                      // palette values for light mode
                      // primary: amber,
                      // divider: amber[200],
                      // text: {
                      //   primary: grey[900],
                      //   secondary: grey[800],
                      // },
                  }
                  : {
                      // palette values for dark mode
                      // secondary: purple,
                      // divider: purple[300],
                      // background: {
                      //   default: deepOrange[900],
                      //   paper: deepOrange[900],
                      // },
                      // text: {
                      //   primary: '#fff',
                      //   secondary: grey[500],
                      // },
                  }),
            },
            // typography: {
            //     fontFamily: roboto.style.fontFamily,
            // },
            // components: {
            //   ...(mode === 'light'
            //     ? {} : {
            //       MuiButton: {
            //         variants: [
            //           {
            //             name: "contained",
            //             props: {
            //               color: 'primary',
            //               variant: 'contained',
            //             },
            //           },
            //         ],
            //       }
            //     }),
            //
            // }
        }),
      [ mode ],
    );

    const handleFileSelect = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post<ImageResponse>(
              'http://localhost:8008/upload-and-search',
              formData,
              {
                  headers: {
                      'Content-Type': 'multipart/form-data',
                  },
              },
            );
            setImages(response.data.similar_images_uris);
        } catch (error) {
            console.error('Error:', error);
            alert('Error uploading image.');
        }
    };

    return (
      <>
          <ColorModeContext.Provider value={colorMode}>
              <ThemeProvider theme={theme}>
                  <CssBaseline/>
                  <MyAppBar/>
                  <Container maxWidth="lg">
                      <Box sx={{ my: 4 }}>
                          <UploadCard onFileSelect={handleFileSelect}/>
                      </Box>
                      <Box sx={{ my: 4 }}>
                          <ImageGrid images={images}/>
                      </Box>
                  </Container>
              </ThemeProvider>
          </ColorModeContext.Provider>
      </>
    );
};

export default App;
