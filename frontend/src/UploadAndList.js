import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Button, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import './UploadAndList.css';

const UploadAndList = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState({});
  const [transcribedFiles, setTranscribedFiles] = useState({});
  const [isTranscribingAll, setIsTranscribingAll] = useState(false);
  const [clickedFiles, setClickedFiles] = useState({});
  const fileRefs = useRef({});

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleClick = (filePath) => {
    setClickedFiles(prev => ({ ...prev, [filePath]: true }));
  };

  const fetchFiles = () => {
    axios.get('http://127.0.0.1:8000/speech/retrieve/')
      .then(response => {
        setFiles(response.data);
      })
      .catch(error => {
        console.error('Error fetching audio files:', error);
      });
  };

  const handleFileChange = (e) => {
    const selectedFiles = e.target.files;
    if (selectedFiles.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('files', selectedFiles[i]);
    }

    axios.post('http://127.0.0.1:8000/speech/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      console.log('Files uploaded successfully:', response.data);
      fetchFiles(); // Refresh the file list after upload
    })
    .catch(error => {
      console.error('Error uploading files:', error);
    });
  };

  const handleTranscribe = (filePath) => {
    console.log(`Transcribing file: ${filePath}`);
    setLoading(prev => ({ ...prev, [filePath]: true }));
  
    axios.get(`http://127.0.0.1:8000/speech/transcribe/${encodeURIComponent(filePath)}/`, { responseType: 'blob' })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        setTranscribedFiles(prev => ({ ...prev, [filePath]: url }));
      })
      .catch(error => {
        console.error(`Error transcribing audio file: ${filePath}`, error);
      })
      .finally(() => {
        setLoading(prev => ({ ...prev, [filePath]: false }));
      });
  };
  
  
  const handleTranscribeAll = () => {
    setIsTranscribingAll(true);
    const transcribePromises = files.map((filePath, index) =>
      new Promise((resolve) => {
        handleTranscribe(filePath);
        setTimeout(() => {
          const ref = fileRefs.current[filePath];
          if (ref) {
            ref.scrollIntoView({ behavior: 'smooth' });
          }
          resolve();
        }, 1000 * index);
      })
    );
  
    Promise.all(transcribePromises)
      .finally(() => {
        setIsTranscribingAll(false);
      });
  };
  

  return (
    <div>
      <h2>Upload and List Audio Files</h2>
      <Button
        component="label"
        variant="contained"
        startIcon={<CloudUploadIcon />}
      >
        Upload files
        <input
          type="file"
          multiple
          hidden
          onChange={handleFileChange}
        />
      </Button>
      <Button
        variant="contained"
        onClick={handleTranscribeAll}
        disabled={isTranscribingAll}
        style={{ backgroundColor: isTranscribingAll ? 'gray' : '#125570', marginLeft: '10px' }}
      >
        {isTranscribingAll ? 'Transcribing All...' : 'Transcribe All'}
      </Button>

      <h3>Uploaded Files</h3>
      <ul>
        {files.map(filePath => (
          <li key={filePath} ref={el => fileRefs.current[filePath] = el}>
            {filePath.split('/').pop()}
            <Button
              variant="contained"
              onClick={() => handleTranscribe(filePath)}
              disabled={loading[filePath]}
              style={{ backgroundColor: loading[filePath] ? 'gray' : '#2D607D' }}
            >
              {loading[filePath] ? 'Transcribing...' : 'Transcribe'}
            </Button>
            {loading[filePath] && <CircularProgress size={20} />}
            {transcribedFiles[filePath] && (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => handleClick(filePath)}
                style={{ backgroundColor: clickedFiles[filePath] ? '#7A972B' : '#FEBA1B' }}
                href={transcribedFiles[filePath]}
                download={`${filePath.split('/').pop()}.txt`}
              >
                Download
              </Button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UploadAndList;
