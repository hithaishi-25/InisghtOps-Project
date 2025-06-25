import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { FolderIcon } from '@heroicons/react/24/outline';

function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await axios.get('http://127.0.0.1:8000/github/organization/DevOpsRealPage/projects/', {
          withCredentials: true,
        });
        setProjects(response.data); // Assuming the response is an array of projects
      } catch (err) {
        setError(err.message);
        console.error('Fetch projects error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">Projects</h1>
          <Link to="/GitOrgView" className="text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </div>

        {loading && <p className="text-center mt-8 text-gray-600">Loading Projects...</p>}
        {error && <p className="text-center mt-8 text-red-600">Error: {error}</p>}
        
        {!loading && !error && (
          <div className="bg-white rounded-lg shadow-md">
            <ul className="divide-y divide-gray-200">
              {projects.length > 0 ? (
                projects.map((project) => (
                  <li key={project.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                    <div className="flex items-center">
                      <FolderIcon className="h-6 w-6 text-gray-500 mr-4"/>
                      <div>
                        <p className="text-lg font-semibold text-gray-900">{project.name}</p>
                        <p className="text-sm text-gray-500">{project.description || 'No description'}</p>
                      </div>
                    </div>
                    {/* You could add a link to the project's external URL here */}
                    <a href={project.html_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                      View on GitHub
                    </a>
                  </li>
                ))
              ) : (
                <li className="p-4 text-center text-gray-500">No projects found.</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Projects;