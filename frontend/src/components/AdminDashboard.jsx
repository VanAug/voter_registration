// src/components/AdminDashboard.js
import React, { useEffect, useState } from 'react';
import { fetchApplicants } from '../api';
import axios from 'axios';

const AdminDashboard = () => {
  const [applicants, setApplicants] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [channelFilter, setChannelFilter] = useState('');
  const [deleting, setDeleting] = useState(null);

  const loadApplicants = async () => {
    try {
      const res = await fetchApplicants();
      setApplicants(res.data);
      setFiltered(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApplicants();
  }, []);

  useEffect(() => {
    let result = applicants;
    if (searchTerm) {
      result = result.filter(a =>
        a.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.id_number.includes(searchTerm) ||
        a.phone_number.includes(searchTerm)
      );
    }
    if (channelFilter) {
      result = result.filter(a => a.registration_channel === channelFilter);
    }
    setFiltered(result);
  }, [searchTerm, channelFilter, applicants]);

  const handleDelete = async (id, fullName) => {
    if (!window.confirm(`Are you sure you want to delete ${fullName}?`)) return;
    setDeleting(id);
    try {
      await axios.delete(`https://voter-registration-gn1a.onrender.com/api/applicants/${id}/`);
      // Refresh list
      setApplicants(prev => prev.filter(a => a.id !== id));
      alert('Deleted successfully');
    } catch (err) {
      console.error(err);
      alert('Delete failed. Please try again.');
    } finally {
      setDeleting(null);
    }
  };

  const exportToCSV = () => {
    // ... your existing export function ...
  };

  const totalSignups = applicants.length;
  const breakdown = {
    USSD: applicants.filter(a => a.registration_channel === 'USSD').length,
    WEBSITE: applicants.filter(a => a.registration_channel === 'WEBSITE').length,
    WHATSAPP: applicants.filter(a => a.registration_channel === 'WHATSAPP').length,
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h2>Admin Dashboard</h2>
      <div className="stats">
        <div className="stat-card">Total Sign-ups: {totalSignups}</div>
        <div className="stat-card">USSD: {breakdown.USSD}</div>
        <div className="stat-card">Website: {breakdown.WEBSITE}</div>
        <div className="stat-card">WhatsApp: {breakdown.WHATSAPP}</div>
      </div>

      <div className="filters">
        <input
          type="text"
          placeholder="Search by name, ID or phone"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select value={channelFilter} onChange={(e) => setChannelFilter(e.target.value)}>
          <option value="">All Channels</option>
          <option value="USSD">USSD</option>
          <option value="WEBSITE">Website</option>
          <option value="WHATSAPP">WhatsApp</option>
        </select>
        <button onClick={exportToCSV}>Export to CSV</button>
      </div>

      <div className="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Full Name</th><th>Phone</th><th>ID Number</th>
              <th>County</th><th>Voter</th><th>Channel</th><th>Date</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(a => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.full_name}</td>
                <td>{a.phone_number}</td>
                <td>{a.id_number}</td>
                <td>{a.county}</td>
                <td>{a.voter_status ? 'Yes' : 'No'}</td>
                <td>{a.registration_channel}</td>
                <td>{new Date(a.registered_at).toLocaleDateString()}</td>
                <td>
                  <button 
                    className="delete-btn" 
                    onClick={() => handleDelete(a.id, a.full_name)}
                    disabled={deleting === a.id}
                  >
                    {deleting === a.id ? '...' : 'Delete'}
                  </button>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr><td colSpan="9">No applicants found</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminDashboard;