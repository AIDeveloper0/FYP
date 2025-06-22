import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';
import logo from '../assets/logo.png';

import '../App.css';

function Header() {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    toast.success('Logged out successfully');
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo-title">
          <img src={logo} alt="FlowMind AI" className="logo" />
          <span className="site-title">FlowMind AI</span>
        </div>
        
        <nav className="header-nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/about" className="nav-link">About</Link>
          <Link to="/diagram" className="nav-link">Diagram</Link>
          <Link to="/contact" className="nav-link">Contact</Link>
          
          {isAuthenticated ? (
            <div className="profile-section">
              <span className="username">{user.name}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="login-btn">Login</Link>
              <Link to="/signup" className="signup-btn">Sign Up</Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Header;
