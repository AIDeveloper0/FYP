import React from "react";
import "../App.css";

export default function About() {
  return (
    <div className="about-page">
      <h2>About FlowMind AI</h2>
      <div className="about-blocks">
        {/* First block - full width */}
        <div className="about-block about-block-full">
          <h3>Our Mission</h3>
          <p>
            To make diagramming effortless and accessible for everyone. We empower
            users to create professional system diagrams with the help of AI.
          </p>
        </div>
        
        {/* Middle blocks - side by side */}
        <div className="about-block">
          <h3>What We Offer</h3>
          <ul>
            <li>
              AI-powered Flowcharts, Sequence, Class, Use Case, and DFD diagrams
            </li>
            <li>Easy-to-use interface for quick diagram creation</li>
            <li>Export and sharing options for your diagrams</li>
          </ul>
        </div>
        <div className="about-block">
          <h3>Who Can Use FlowMind AI?</h3>
          <p>
            Students, developers, analysts, and anyone who needs to visualize
            systems and processes efficiently.
          </p>
        </div>
        
        {/* Last block - full width */}
        <div className="about-block about-block-full">
          <h3>Contact & Support</h3>
          <p>
            Have questions or feedback?{" "}
            <a href="/contact" className="about-link">
              Contact us
            </a>{" "}
            any time!
          </p>
        </div>
      </div>
    </div>
  );
}