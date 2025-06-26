import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const [selectedOption, setSelectedOption] = useState('Git');
  const navigate = useNavigate();

  const handleOverviewClick = () => {
    if(selectedOption === 'Git'){
      navigate(`/GitOrgView`);
    } else if(selectedOption === 'Azure'){
      navigate('/AzureOrgView');
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#F9FAFB] p-4">
      <h1 className="text-3xl font-bold text-[#111827] mb-6">Select Data Source</h1>
      <div className="bg-[#F9FAFB] p-6 rounded-lg shadow-md flex flex-col items-center">
        <select
          value={selectedOption}
          onChange={(e) => setSelectedOption(e.target.value)}
          className="mb-4 p-2 border rounded-md text-lg"
        >
          <option value="Git">Git</option>
          <option value="Azure">Azure</option>
        </select>
        <button
          onClick={handleOverviewClick}
          className="bg-[#7C3AED] text-white px-4 py-2 rounded-md hover:bg-[#5B21B6] transition-colors"
        >
          Get Overview
        </button>
      </div>
    </div>
  );
}

export default HomePage;