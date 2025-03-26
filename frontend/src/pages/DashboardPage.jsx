import React, { useState } from 'react';
import UploadForm from '../components/UploadForm';
import ResultsDisplay from '../components/ResultsDisplay';
import { useAuth } from '../context/AuthContext'; // Optional: Get user info if needed

const DashboardPage = () => {
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  // const { user } = useAuth(); // Example if you stored user info

  const handleUploadComplete = (resultData, errorMsg) => {
    if (errorMsg) {
      setUploadError(errorMsg);
      setUploadResult(null); // Clear previous results on error
    } else {
      setUploadResult(resultData);
      setUploadError(null); // Clear previous errors on success
    }
     setIsUploading(false); // Make sure loading stops
  };

  // Callback for UploadForm to set loading state
  const handleUploadStart = () => {
    setIsUploading(true);
    setUploadError(null); // Clear previous errors/results on new upload
    setUploadResult(null);
  };


  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
         {/* Welcome, {user?.username || 'User'}! */} Welcome!
      </h1>
      <p className="text-center text-gray-600 mb-8">
        Upload your resume below to get an ATS compatibility score and suggestions.
      </p>

      {/* Pass handleUploadStart if needed, or manage loading within UploadForm */}
      <UploadForm onUploadComplete={handleUploadComplete} />

      {/* Pass the result, error, and loading state to ResultsDisplay */}
      <ResultsDisplay
         result={uploadResult}
         error={uploadError}
         isLoading={isUploading}
       />
    </div>
  );
};

export default DashboardPage;