import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        // NOTE: This assumes a new backend endpoint at '/github/users/'
        const response = await axios.get('http://127.0.0.1:8000/github/organization/DevOpsRealPage/users/', {
          withCredentials: true,
        });
        setUsers(response.data); // Expecting an array of users
      } catch (err) {
        setError(err.message);
        console.error('Fetch users error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">Organization Members</h1>
          <Link to="/GitOrgView" className="text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </div>

        {loading && <p className="text-center mt-8 text-gray-600">Loading Users...</p>}
        {error && <p className="text-center mt-8 text-red-600">Error: {error}</p>}
        
        {!loading && !error && (
          <div className="bg-white rounded-lg shadow-md">
            <ul className="divide-y divide-gray-200">
              {users.length > 0 ? (
                users.map((user) => (
                  <li key={user.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                    <div className="flex items-center">
                      {/* Using the user's avatar makes the list much better! */}
                      <img src={user.avatar_url} alt={`${user.login}'s avatar`} className="h-12 w-12 rounded-full mr-4"/>
                      <div>
                        <p className="text-lg font-semibold text-gray-900">{user.login}</p>
                        {/* You could add more info here if your API provides it, e.g., user's name */}
                      </div>
                    </div>
                    <a href={user.html_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 text-sm">
                      View Profile
                    </a>
                  </li>
                ))
              ) : (
                <li className="p-4 text-center text-gray-500">No users found.</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Users;