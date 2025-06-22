import React from 'react';
// If you put the CSS in a separate file like "Contact.css", you must import it.
// If you added it to your main global CSS file, you don't need this import here.
 import './Contact.css';

function Contact() {
  return (
    // 1. Main page wrapper
    <div className="contact-page">
      {/* 2. The centered "card" that holds the form */}
      <div className="contact-form-container">
        <h2>Contact Us</h2>
        <p>We'd love to hear from you! Please fill out the form below.</p>

        {/* 3. The form itself */}
        <form className="contact-form">
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input type="text" id="name" name="name" placeholder="Your name" required />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Your email" required />
          </div>

          <div className="form-group">
            <label htmlFor="message">Message:</label>
            <textarea id="message" name="message" rows="6" placeholder="Your message" required></textarea>
          </div>

          <button type="submit">Send Message</button>
        </form>
      </div>
    </div>
  );
}

export default Contact;