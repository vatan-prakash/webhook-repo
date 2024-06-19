'use client'
import React, { useState, useEffect } from 'react';

const ActionList = () => {
  const [actions, setActions] = useState([]);

  const fetchData = () => {
    fetch('https://webhook-repo-hsq1.onrender.com/events', {
      headers: {
        'Content-Type': 'application/json'
      }
    }) 
      .then(response => response.json())
      .then(data => setActions(data))
      .catch(error => console.error('Error fetching data:', error));
  };

  useEffect(() => {
    fetchData(); // Initial fetch
    const intervalId = setInterval(fetchData, 15000); // Fetch data every 15 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const day = date.getUTCDate();
    const month = date.toLocaleString('default', { month: 'long' });
    const year = date.getUTCFullYear();
    const hours = date.getUTCHours();
    const minutes = date.getUTCMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;

    return `${day}${getOrdinalSuffix(day)} ${month} ${year} - ${formattedHours}:${formattedMinutes} ${ampm} UTC`;
  };

  const getOrdinalSuffix = (day) => {
    if (day > 3 && day < 21) return 'th';
    switch (day % 10) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  };

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
                <td className="py-2 px-4">{action.from_branch}</td>
                <td className="py-2 px-4">{action.request_id}</td>
                <td className="py-2 px-4">{formatTimestamp(action.timestamp)}</td>
                <td className="py-2 px-4">{action.to_branch}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ActionList;
