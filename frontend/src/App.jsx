// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import AdminDashboard from './components/AdminDashboard';
import CheckStatus from './components/CheckStatus';
import './styles.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <Link to="/">Register</Link>
          <Link to="/check-status">Check Status</Link>
        </nav>
        <Routes>
          <Route path="/" element={<RegistrationForm />} />
          <Route path="/check-status" element={<CheckStatus />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;