import React from 'react';
import Box from '@mui/material/Box';

interface ImagePreviewProps {
    imageSrc: string;
}

const ImagePreview: React.FC<ImagePreviewProps> = ({ imageSrc }) => {
    return (
      <Box
        sx={{
            width: 200, // Set a fixed width
            height: 200, // Set a fixed height
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '8px 0',
            border: '1px solid #ccc', // Optional: Adds a border around the preview
        }}
      >
          <img
            src={imageSrc}
            alt="Preview"
            style={{ maxWidth: '100%', maxHeight: '100%' }} // Ensures the image fits within the container
          />
      </Box>
    );
};

export default ImagePreview;
