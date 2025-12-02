import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUpload.css';

function FileUpload({ onFileSelect, selectedFile }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    multiple: false
  });

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${selectedFile ? 'has-file' : ''}`}
      >
        <input {...getInputProps()} />
        {selectedFile ? (
          <div className="file-selected">
            <div className="file-icon">📄</div>
            <div className="file-info">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
            <button
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                onFileSelect(null);
              }}
            >
              ✕
            </button>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">☁️</div>
            <p className="upload-text">
              {isDragActive
                ? 'Drop your resume here'
                : 'Drag & drop your resume here'}
            </p>
            <p className="upload-subtext">or click to browse</p>
            <p className="file-types">Supports PDF and TXT files</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileUpload;
