'use client'

import React, { useState, useEffect } from 'react';

const ActionList = () => {
  const [actions, setActions] = useState([]);

  const fetchData = () => {
    fetch('https://webhook-repo-hsq1.onrender.com/events',{
      headers: {
        'Content-Type': 'application/json'
      }
    }) // Adjust the URL to match your backend endpoint
      .then(response => response.json())
      .then(data => setActions(data))
      .catch(error => console.error('Error fetching data:', error));
  };

  useEffect(() => {
    fetchData(); // Fetch data initially
    // const interval = setInterval(fetchData, 15000); // Fetch data every 15 seconds

    // return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Action List</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white shadow-md rounded-lg">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="py-2 px-4">ID</th>
              <th className="py-2 px-4">Action</th>
              <th className="py-2 px-4">Author</th>
              <th className="py-2 px-4">From Branch</th>
              <th className="py-2 px-4">Request ID</th>
              <th className="py-2 px-4">Timestamp</th>
              <th className="py-2 px-4">To Branch</th>
            </tr>
          </thead>
          <tbody>
            {actions.map(action => (
              <tr key={action._id} className="border-b text-black border-gray-200">
                <td className="py-2 px-4">{action._id}</td>
                <td className="py-2 px-4">{action.action}</td>
                <td className="py-2 px-4">{action.author}</td>
                <td className="py-2 px-4">{action.from_branch}</td> {/* Extract first line */}
                <td className="py-2 px-4">{action.request_id}</td>
                <td className="py-2 px-4">{new Date(action.timestamp).toLocaleString()}</td>
                <td className="py-2 px-4">{action.to_branch}</td> {/* Extract first line */}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ActionList;
