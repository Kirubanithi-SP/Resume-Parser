import React, { useState, useRef } from 'react';
import apiClient from '../services/api'; // Use the configured axios instance
import Spinner from './Spinner';

// Accept onUploadComplete prop to pass results/errors back up
const UploadForm = ({ onUploadComplete }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null); // Ref to clear file input

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(''); // Clear previous errors
    } else {
      setSelectedFile(null);
      setError('Please select a PDF file.');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }

    setError('');
    setLoading(true);

    const formData = new FormData();
    formData.append('resume', selectedFile); // Match backend expected field name

    try {
      // Make the API call - interceptor will add the token
      // Explicitly set Content-Type for FormData
      const response = await apiClient.post('/api/upload', formData, {
         headers: {
           // Axios might set this automatically with FormData, but being explicit is safer
           'Content-Type': 'multipart/form-data',
         },
      });

      // Call the callback with the result data
      onUploadComplete(response.data, null);

      // Clear the file input after successful upload
      setSelectedFile(null);
      if(fileInputRef.current) {
          fileInputRef.current.value = "";
      }

    } catch (err) {
      console.error('Upload error:', err.response?.data || err.message);
      const errorMessage = err.response?.data?.message || 'File upload failed. Please try again.';
      setError(errorMessage);
      // Call the callback with null data and the error message
      onUploadComplete(null, errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded shadow-md max-w-lg mx-auto mt-8">
      <h3 className="text-xl font-semibold text-gray-700 mb-4 text-center">Upload Your Resume (PDF)</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <div>
          <label htmlFor="resume-upload" className="block text-sm font-medium text-gray-600 mb-1">
            Select PDF file:
          </label>
          <input
            id="resume-upload"
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            required
            className="block w-full text-sm text-gray-500
                       file:mr-4 file:py-2 file:px-4
                       file:rounded-full file:border-0
                       file:text-sm file:font-semibold
                       file:bg-blue-50 file:text-blue-700
                       hover:file:bg-blue-100"
            disabled={loading}
          />
          {selectedFile && <p className="text-xs text-gray-500 mt-1">Selected: {selectedFile.name}</p>}
        </div>
        <button
          type="submit"
          className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 flex justify-center items-center"
          disabled={!selectedFile || loading}
        >
          {loading ? <Spinner /> : 'Parse Resume'}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;