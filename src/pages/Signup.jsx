import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import '../App.css';

export default function Signup() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    organization: "",
    role: ""
  });

  const navigate = useNavigate();

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:5000/api/users/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form)
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Registration successful!');
        navigate('/login');
      } else {
        toast.error(data.msg || 'Registration failed');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Registration failed. Please try again.');
    }
  };

  return (
    <div className="signup-page" style={{ maxWidth: 400, margin: "2rem auto", background: "#fff", borderRadius: 8, padding: "2rem", boxShadow: "0 2px 8px rgba(44,62,80,0.08)" }}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit} className="signup-form" style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={form.name}
          required
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          required
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          required
          minLength={6}
          onChange={handleChange}
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={form.confirmPassword}
          required
          minLength={6}
          onChange={handleChange}
        />
        <input
          type="text"
          name="organization"
          placeholder="Organization (optional)"
          value={form.organization}
          onChange={handleChange}
        />
        <select
          name="role"
          value={form.role}
          onChange={handleChange}
          required
        >
          <option value="">Select Role</option>
          <option value="student">Student</option>
          <option value="developer">Developer</option>
          <option value="analyst">Analyst</option>
          <option value="other">Other</option>
        </select>
        <label style={{ fontSize: "0.95rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <input
            type="checkbox"
            name="agree"
            checked={form.agree}
            onChange={handleChange}
            required
          />
          I agree to the <a href="#" style={{ color: "#3498db" }}>terms and conditions</a>
        </label>
        <button type="submit" style={{ background: "#3498db", color: "#fff", border: "none", borderRadius: 5, padding: "0.7rem", fontWeight: "bold" }}>Sign Up</button>
      </form>
    </div>
  );
}