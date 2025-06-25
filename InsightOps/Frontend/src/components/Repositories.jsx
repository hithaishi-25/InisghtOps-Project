import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { CodeBracketIcon } from '@heroicons/react/24/outline'; // A nice icon for repos

function Repositories() {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRepositories = async () => {
      try {
        setLoading(true);
        setError(null);
        // NOTE: This assumes a new backend endpoint at '/github/repositories/'
        const response = await axios.get('http://127.0.0.1:8000/github/organization/DevOpsRealPage/repositories/', {
          withCredentials: true,
        });
        setRepositories(response.data); // Expecting an array of repositories
      } catch (err) {
        setError(err.message);
        console.error('Fetch repositories error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRepositories();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">Repositories</h1>
          <Link to="/GitOrgView" className="text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </div>

        {loading && <p className="text-center mt-8 text-gray-600">Loading Repositories...</p>}
        {error && <p className="text-center mt-8 text-red-600">Error: {error}</p>}
        
        {!loading && !error && (
          <div className="bg-white rounded-lg shadow-md">
            <ul className="divide-y divide-gray-200">
              {repositories.length > 0 ? (
                repositories.map((repo) => (
                  <li key={repo.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                    <div className="flex items-center">
                      <CodeBracketIcon className="h-6 w-6 text-gray-500 mr-4"/>
                      <div>
                        <p className="text-lg font-semibold text-gray-900">{repo.name}</p>
                        <p className="text-sm text-gray-500">{repo.description || 'No description'}</p>
                      </div>
                    </div>
                    <a href={repo.html_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 text-sm">
                      View on GitHub
                    </a>
                  </li>
                ))
              ) : (
                <li className="p-4 text-center text-gray-500">No repositories found.</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Repositories;