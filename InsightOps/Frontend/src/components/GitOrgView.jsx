import { useState, useEffect } from 'react';
import { BriefcaseIcon, FolderIcon, UsersIcon } from '@heroicons/react/24/solid';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';
import CardList from './CardList';
import { useNavigate } from 'react-router-dom';

function GitOrgView (){
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
        const fetchData = async () => {
            try {
            setLoading(true);
            setError(null);

            // Fetch data from Django API
            const response = await axios.get('http://127.0.0.1:8000/github/organization/DevOpsRealPage/', {
                withCredentials: true, // Include credentials if authentication is needed
            });
            const apiData = response.data;

            // Map the API response to card data
            const data = [
                { title: 'Projects', number: apiData.total_projects, icon: BriefcaseIcon, color: 'bg-red-500', path: '/projects' },
                { title: 'Repositories', number: apiData.total_repositories, icon: FolderIcon, color: 'bg-blue-500', path: '/repositories' },
                { title: 'Users', number: apiData.active_users_count, icon: UsersIcon, color: 'bg-red-500', path: '/users' },
            ];

            // Add unique IDs to each card
            const dataWithIds = data.map((card) => ({
                ...card,
                id: uuidv4(),
            }));

            setCardData(dataWithIds);
            } catch (err) {
            setError(err.message);
            console.error('Fetch error:', err);
            } finally {
            setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
    <>
        <div className="text-center p-4">
        <h1 className="text-3xl font-bold text-blue-600">Organization Dashboard</h1>
        {loading && <p className="mt-4 text-gray-600">Loading...</p>}
        {error && <p className="mt-4 text-red-600">Error: {error}</p>}
        {!loading && !error && (
            <CardList cards={cardData} onCardClick={handleCardClick} />
            )}
        </div>
    </>

);
    
} 

export default GitOrgView;