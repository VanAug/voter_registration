import React, { useState } from 'react';
import { registerViaWeb } from '../api';

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    id_number: '',
    county: '',
    voter_status: false,
  });
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const counties = [
  'Baringo', 'Bomet', 'Bungoma', 'Busia', 'Elgeyo Marakwet', 'Embu',
  'Garissa', 'Homa Bay', 'Isiolo', 'Kajiado', 'Kakamega', 'Kericho',
  'Kiambu', 'Kilifi', 'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui',
  'Kwale', 'Laikipia', 'Lamu', 'Machakos', 'Makueni', 'Mandera',
  'Marsabit', 'Meru', 'Migori', 'Mombasa', 'Murang\'a', 'Nairobi',
  'Nakuru', 'Nandi', 'Narok', 'Nyamira', 'Nyandarua', 'Nyeri',
  'Samburu', 'Siaya', 'Taita Taveta', 'Tana River', 'Tharaka-Nithi',
  'Trans Nzoia', 'Turkana', 'Uasin Gishu', 'Vihiga', 'Wajir', 'West Pokot'
 ];

  const normalizePhone = (phone) => {
    let cleaned = phone.trim();
    if (cleaned.startsWith('0')) cleaned = '+254' + cleaned.slice(1);
    else if (cleaned.startsWith('254') && !cleaned.startsWith('+')) cleaned = '+' + cleaned;
    else if (/^\d{9}$/.test(cleaned)) cleaned = '+254' + cleaned;
    return cleaned;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate fields before showing confirmation
    if (!formData.full_name || !formData.phone_number || !formData.id_number || !formData.county) {
      setMessage({ text: 'All fields are required.', type: 'error' });
      return;
    }
    if (!/^\d{5,8}$/.test(formData.id_number)) {
      setMessage({ text: 'ID number must be 5-8 digits.', type: 'error' });
      return;
    }
    const normalizedPhone = normalizePhone(formData.phone_number);
    if (!normalizedPhone.match(/^\+254[0-9]{9}$/)) {
      setMessage({ text: 'Phone number must be a valid Kenyan number (e.g., 0712345678 or +254712345678)', type: 'error' });
      return;
    }
    // Show confirmation modal
    setShowConfirm(true);
  };

  const confirmRegistration = async () => {
    setShowConfirm(false);
    setLoading(true);
    setMessage({ text: '', type: '' });

    const payload = {
      ...formData,
      phone_number: normalizePhone(formData.phone_number)
    };

    try {
      const response = await registerViaWeb(payload);
      setMessage({ text: `Registration successful! Welcome ${response.data.full_name}.`, type: 'success' });
      setFormData({ full_name: '', phone_number: '', id_number: '', county: '', voter_status: false });
    } catch (err) {
      const errorMsg = err.response?.data?.phone_number?.[0] ||
                       err.response?.data?.id_number?.[0] ||
                       err.response?.data?.detail ||
                       'Registration failed. Please check your details.';
      setMessage({ text: errorMsg, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const cancelRegistration = () => {
    setShowConfirm(false);
    setMessage({ text: 'Registration cancelled.', type: 'error' });
  };

  return (
    <div className="form-container">
      <h2>Voter Registration</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Phone Number</label>
          <input type="tel" name="phone_number" value={formData.phone_number} onChange={handleChange} placeholder="0712345678" required />
          <small>Kenyan number (07... or +254...)</small>
        </div>
        <div className="form-group">
          <label>ID Number</label>
          <input type="text" name="id_number" value={formData.id_number} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>County</label>
          <select name="county" value={formData.county} onChange={handleChange} required>
            <option value="">Select county</option>
            {counties.map(c => <option key={c}>{c}</option>)}
          </select>
        </div>
        <div className="checkbox-group">
          <input type="checkbox" name="voter_status" checked={formData.voter_status} onChange={handleChange} />
          <label>To register click the checkbox</label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
        {message.text && <div className={`message ${message.type}`}>{message.text}</div>}
      </form>

      {/* Confirmation Modal */}
      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Confirm Registration</h3>
            <p>Do you wish to be registered with these details?</p>
            <div className="modal-actions">
              <button onClick={confirmRegistration}>Yes, Register</button>
              <button onClick={cancelRegistration}>No, Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RegistrationForm;