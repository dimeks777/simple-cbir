import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';


const App2: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [similarImages, setSimilarImages] = useState<string[]>([]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleFormSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post<string[]>(
        'http://localhost:8008/upload-and-search',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setSimilarImages(response.data);
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Failed to upload and search for similar images.');
    }
  };

  return (
    <div className="App">
      <h1>CBIR System</h1>
      <form onSubmit={handleFormSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Search Similar Images</button>
      </form>

      <div className="similar-images">
        {similarImages.map((image, index) => (
          <img key={index} src={image} alt="Similar" />
        ))}
      </div>
    </div>
  );
};

export default App2;
