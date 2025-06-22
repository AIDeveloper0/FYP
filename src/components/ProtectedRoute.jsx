import { Navigate, useLocation } from "react-router-dom";
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';

const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const isAuthenticated = !!localStorage.getItem("token");

  if (!isAuthenticated) {
    // Show login required message only once
    toast.warning('Please login to access this page', {
      position: "top-center",
      autoClose: 3000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      toastId: 'auth-warning' // Add a unique toastId to prevent duplicates
    });

    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  return children;
};

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired
};

export default ProtectedRoute;