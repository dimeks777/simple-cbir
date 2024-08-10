import React from 'react';
import Masonry from 'react-masonry-css';
import './mansory.css';


interface ImageGridProps {
    images: string[];
}

const ImageGrid: React.FC<ImageGridProps> = ({ images }) => {
    // Define breakpoint columns for responsiveness
    const breakpointColumnsObj = {
        default: 4,
        1100: 3,
        700: 2,
        500: 1
    };

    return (
      <Masonry
        breakpointCols={breakpointColumnsObj}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
      >
          {images.map((image, index) => (
            <img key={index} src={image} alt={`Similar Image ${index}`} style={{ width: '100%', display: 'block' }} />
          ))}
      </Masonry>
    );
};

export default ImageGrid;