// src/components/GitFilter.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 1. Import useNavigate
import { FiCalendar } from 'react-icons/fi';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import { DateRange } from 'react-date-range';
import { addDays, format } from 'date-fns';

const GitFilter = ({ orgName }) => { // No longer needs onFilter prop
  const [showPicker, setShowPicker] = useState(false);
  const [selection, setSelection] = useState({
    startDate: new Date(),
    endDate: addDays(new Date(), 7),
    key: 'selection'
  });

  const navigate = useNavigate(); // 2. Initialize the navigate function

  const handleViewReports = () => {
    // 3. Format dates into a URL-friendly string (YYYY-MM-DD)
    const startDate = format(selection.startDate, 'yyyy-MM-dd');
    const endDate = format(selection.endDate, 'yyyy-MM-dd');
    
    // 4. Navigate to the new route with dates as query parameters
    navigate(`/view-report?startDate=${startDate}&endDate=${endDate}`);
    
    // 5. Close the picker after navigation
    setShowPicker(false);
  };

  return (
    <div className="relative">
      <button 
        onClick={() => setShowPicker(!showPicker)}
        className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors text-sm"
      >
        <FiCalendar className="text-gray-600" />
        <span>Date Range</span>
      </button>

      {showPicker && (
        <div className="absolute z-10 mt-1 right-0 bg-white shadow-lg rounded-md p-2 border border-gray-200">
          <DateRange
            ranges={[selection]}
            onChange={ranges => setSelection(ranges.selection)} // Just update local state now
            moveRangeOnFirstSelection={false}
            months={1}
            direction="horizontal"
          />
          {/* 6. Add the "View Reports" button */}
          <div className="p-2 text-right border-t border-gray-200 mt-2">
            <button
              onClick={handleViewReports}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              View Reports
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GitFilter;