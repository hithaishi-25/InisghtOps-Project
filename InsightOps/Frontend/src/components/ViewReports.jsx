// src/components/ViewReport.js

import { useSearchParams } from 'react-router-dom';

const ViewReport = () => {

  
  // useSearchParams hook allows us to read the query parameters from the URL
  const [searchParams] = useSearchParams();

  // Get the specific parameters by name
  const startDate = searchParams.get('startDate');
  const endDate = searchParams.get('endDate');

  return (
    <div className="text-center p-8">
        
        <h1 className="text-3xl font-bold text-gray-800">
            Displaying the Reports
        </h1>
        
        {startDate && endDate ? (
        <div className="mt-6 p-6 bg-gray-100 rounded-lg inline-block">
            <h2 className="text-xl font-semibold text-gray-700">Date Range:</h2>
            <p className="mt-2 text-lg text-blue-600 font-mono">
                <strong>From:</strong> {startDate}
            </p>
            <p className="text-lg text-blue-600 font-mono">
                <strong>To:</strong> {endDate}
            </p>
            <div className="mt-4 text-left text-gray-600">
            {/* Now you can make an API call using orgName, startDate, and endDate */}
                <p>Report content for your org will be listed here...</p>
            </div>
        </div>
        ) : (
        <p className="mt-4 text-red-500">
            Date range not specified. Please go back and select a date range.
        </p>
        )}
    </div>
  );
};

export default ViewReport;