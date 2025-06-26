// src/components/GitOrgView.jsx

import { useState, useEffect } from 'react';
import { BriefcaseIcon, FolderIcon, UsersIcon } from '@heroicons/react/24/solid';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';
import CardList from './CardList';
import GitFilter from './GitFilter'; 

function GitOrgView() {
  const [cardData, setCardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
          { title: 'Projects', number: apiData.total_projects, icon: BriefcaseIcon, color: 'bg-red-500' },
          { title: 'Repos', number: apiData.total_repositories, icon: FolderIcon, color: 'bg-blue-500' },
          { title: 'Users', number: apiData.active_users_count, icon: UsersIcon, color: 'bg-red-500' },
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
        <h1 className="text-3xl font-bold text-blue-600">Org Dashboard</h1>
        
        <GitFilter  />
      </div>
      
      <div className="text-center">
        {loading && <p className="mt-4 text-gray-600">Loading...</p>}
        {error && <p className="mt-4 text-red-600">Error: {error}</p>}
        {!loading && !error && <CardList cards={cardData} />}
      </div>
    </div>
  );
}

export default GitOrgView;