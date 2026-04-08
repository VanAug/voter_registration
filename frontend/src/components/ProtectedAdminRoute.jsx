import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAdminLoggedIn } from '../api';

const ProtectedAdminRoute = ({ children }) => {
  if (!isAdminLoggedIn()) {
    return <Navigate to="/admin/login" replace />;
  }

  return children;
};

export default ProtectedAdminRoute;
