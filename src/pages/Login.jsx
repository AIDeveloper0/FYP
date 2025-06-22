import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";
import '../App.css'; 

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    if (!email || !password) {
      toast.error("Please fill in all fields");
      return;
    }

    setLoading(true);

    try {
      console.log('🔄 Attempting login to: /api/auth/login');
      
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      console.log('📡 Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('📊 Response data:', data);

      if (data.success) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        
        toast.success("Login successful!");
        navigate('/');
      } else {
        toast.error(data.message || "Invalid credentials");
      }
    } catch (error) {
      console.error('💥 Login error:', error);
      
      if (error.message.includes('Failed to fetch')) {
        toast.error("❌ Backend server not running! Start backend with: python app.py");
      } else if (error.message.includes('HTTP 404')) {
        toast.error("❌ Login endpoint not found. Check backend routes.");
      } else if (error.message.includes('HTTP 500')) {
        toast.error("❌ Server error. Check backend logs.");
      } else {
        toast.error(`❌ Connection error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container login-container-override">
        <h2 className="login-title">Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            required
            onChange={e => setEmail(e.target.value.trim())}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            required
            minLength={6}
            onChange={e => setPassword(e.target.value)}
            className="login-input"
          />
          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="auth-link">
          New user? <Link to="/signup" className="signup-link">Sign up first</Link>
        </div>
      </div>
    </div>
  );
}