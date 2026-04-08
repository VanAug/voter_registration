import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginAdmin, setAdminToken } from '../api';

const AdminLogin = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const onChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      const { data } = await loginAdmin(formData);
      setAdminToken(data.token);
      navigate('/admin');
    } catch (err) {
      setError(err?.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Admin Login</h2>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            value={formData.username}
            onChange={onChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={onChange}
            required
          />
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Signing in...' : 'Login'}
        </button>
      </form>

      {error && <p className="message error">{error}</p>}
    </div>
  );
};

export default AdminLogin;
