import React, { useState } from 'react';
import axios from 'axios';

const CheckStatus = () => {
  const [idNumber, setIdNumber] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!idNumber.trim()) {
      setError('Please enter an ID number.');
      return;
    }
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await axios.get(`https://voter-registration-gn1a.onrender.com/api/check-status/${idNumber.trim()}/`);
      if (response.data.found) {
        setResult(response.data.data);
      } else {
        setError(response.data.message);
      }
    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setError('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="status-container">
      <h2>Check Registration Status</h2>
      <form onSubmit={handleCheck}>
        <div className="form-group">
          <label>Enter your ID Number</label>
          <input
            type="text"
            value={idNumber}
            onChange={(e) => setIdNumber(e.target.value)}
            placeholder="e.g., 12345678"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Check Status'}
        </button>
      </form>

      {error && <div className="message error">{error}</div>}

      {result && (
        <div className="status-result">
          <h3>Registration Details</h3>
          <p><strong>Full Name:</strong> {result.full_name}</p>
          <p><strong>Phone:</strong> {result.phone_number}</p>
          <p><strong>County:</strong> {result.county}</p>
          <p><strong>Voter Status:</strong> {result.voter_status ? 'Registered to vote' : 'Not registered to vote'}</p>
          <p><strong>Channel:</strong> {result.registration_channel}</p>
          <p><strong>Date:</strong> {new Date(result.registered_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default CheckStatus;