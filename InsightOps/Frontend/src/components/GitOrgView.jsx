// src/components/GitOrgView.jsx

import { useState, useEffect } from 'react';
import { BriefcaseIcon, FolderIcon, UsersIcon } from '@heroicons/react/24/solid';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';
import CardList from './CardList';
import { useNavigate } from 'react-router-dom';
import GitFilter from './GitFilter';

function GitOrgView() {
  const [cardData, setCardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleCardClick = (path) => {
        if (path) {
            navigate(path);
        }
    };

  useEffect(() => {
    // 1. Create an AbortController for each effect run
    const controller = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await axios.get(`http://127.0.0.1:8000/github/organization/DevOpsRealPage/`, {
          withCredentials: true,
          // 2. Pass the controller's signal to the request
          signal: controller.signal, 
        });

        const apiData = response.data;
        const data = [
          { title: 'Projects', number: apiData.total_projects, icon: BriefcaseIcon, color: 'bg-[#7C3AED]', path: '/projects' },
          { title: 'Repositories', number: apiData.total_repositories, icon: FolderIcon, color: 'bg-[#7C3AED]', path: '/repositories' },
          { title: 'Users', number: apiData.active_users_count, icon: UsersIcon, color: 'bg-[#7C3AED]', path: '/users' },
        ];
        const dataWithIds = data.map((card) => ({ ...card, id: uuidv4() }));
        setCardData(dataWithIds);
      } catch (err) {
        setError(err.message);
        console.error('Fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [] );   

  return (
    <div className="p-4">
      <div className="flex justify-between items-start mb-4"> 
        {/* The heading is now also dynamic */}
        <h1 className="text-4xl font-bold text-[#111827]">Org Dashboard</h1>
        
        <GitFilter  />
      </div>
      
      <div className="text-center">
        {loading && <p className="mt-4 text-[#111827]">Loading...</p>}
        {error && <p className="mt-4 text-red-700">Error: {error}</p>}
        {!loading && !error && (
            <CardList cards={cardData} onCardClick={handleCardClick} />
            )}
      </div>
    </div>
  );
}

export default GitOrgView;