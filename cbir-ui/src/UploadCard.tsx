import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';

interface UploadCardProps {
    onFileSelect: (file: File) => void;
}

const Input = styled('input')({
    display: 'none',
});

const UploadCard: React.FC<UploadCardProps> = ({ onFileSelect }) => {
    const [isDragOver, setIsDragOver] = useState(false);
    const [imagePreview, setImagePreview] = useState<string | null>(null);

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setIsDragOver(false);
        const file = event.dataTransfer.files[0];
        if (file) {
            onFileSelect(file);
            previewFile(file);
        }
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        const file = event.target.files && event.target.files[0];
        if (file) {
            onFileSelect(file);
            previewFile(file);
        }
    };

    const previewFile = (file: File) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            setImagePreview(reader.result as string);
        };
    };

    return (
      <Card
        variant="outlined"
        sx={{
            maxWidth: 345,
            margin: 'auto',
            border: isDragOver ? '2px dashed #1976d2' : '2px dashed #ccc',
            backgroundColor: isDragOver ? '#e3f2fd' : '',
            transition: 'border-color 0.3s ease-in-out, background-color 0.3s ease-in-out',
            position: 'relative',
            overflow: 'hidden',
            // boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
          <CardContent sx={{ textAlign: 'center' }}>
              {imagePreview ? (
                <img src={imagePreview} alt="Preview" style={{ maxWidth: '100%', marginBottom: 16 }} />
              ) : (
                <Typography variant="h6" component="h2" sx={{ marginBottom: 2 }}>
                    Drag an image here or click to upload
                </Typography>
              )}
              <Input
                accept="image/*"
                id="raised-button-file"
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="raised-button-file">
                  <Button
                    variant="contained"
                    component="span"
                    startIcon={<CloudUploadIcon />}
                    sx={{ marginTop: 2 }}
                  >
                      Upload
                  </Button>
              </label>
              {isDragOver && (
                <Typography variant="caption" display="block" sx={{ marginTop: 2 }}>
                    Drop to upload the image
                </Typography>
              )}
          </CardContent>
      </Card>
    );
};

export default UploadCard;
