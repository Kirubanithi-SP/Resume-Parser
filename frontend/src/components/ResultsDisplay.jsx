import React from 'react';
import Spinner from './Spinner';

const ResultsDisplay = ({ result, error, isLoading }) => {
  if (isLoading) {
    return <Spinner />;
  }

  if (error) {
    return <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded max-w-lg mx-auto text-center">{error}</div>;
  }

  if (!result) {
    return null; // Don't render anything if there's no result yet
  }

  // Handle the case where the PDF wasn't identified as a resume
  if (result.message) {
    return <div className="mt-6 p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded max-w-lg mx-auto text-center">{result.message}</div>;
  }

  // Display ATS score and suggestions
  if (result.ats_score !== undefined && result.suggestions !== undefined) {
    return (
      <div className="mt-6 p-6 bg-white rounded shadow-md max-w-lg mx-auto space-y-4">
        <h3 className="text-xl font-semibold text-gray-800 text-center border-b pb-2">Parsing Results</h3>
        <div className="text-center">
          <p className="text-lg font-medium text-gray-700">ATS Compatibility Score:</p>
          <p className={`text-4xl font-bold ${result.ats_score >= 80 ? 'text-green-600' : result.ats_score >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
            {result.ats_score}%
          </p>
        </div>
        <div>
          <p className="text-lg font-medium text-gray-700">Suggestions:</p>
          <p className="text-gray-600 whitespace-pre-wrap bg-gray-50 p-3 rounded border">{result.suggestions || 'No specific suggestions provided.'}</p>
        </div>
      </div>
    );
  }

  // Fallback if the result format is unexpected
  return <div className="mt-6 p-4 bg-gray-100 border border-gray-300 text-gray-600 rounded max-w-lg mx-auto text-center">Received unexpected result format.</div>;
};

export default ResultsDisplay