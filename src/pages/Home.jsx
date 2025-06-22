import { Link } from 'react-router-dom';
    import '../App.css';

    function Home() {
      return (
        <div className="home-page">
          <section className="hero">
            <h2>Welcome to FlowMind AI</h2>
            <p>Automate system modeling diagrams like Flowcharts, Sequence diagram, Class Diagram, Use-case Diagram and DFD with ease.</p>
            <Link to="/diagram" className="cta-button">Create Your Diagram</Link>
          </section>

          <section className="features">
            <h3>Why Choose FlowMind AI?</h3>
            <div className="feature-list">
              <div className="feature-item">
                <h4>Easy Diagram Creation</h4>
                <p>Create flowcharts, UML diagrams, and more in minutes.</p>
              </div>
              <div className="feature-item">
                <h4>AI-Powered Automation</h4>
                <p>Let AI generate diagrams based on your input.</p>
              </div>
              <div className="feature-item">
                <h4>Export & Share</h4>
                <p>Export your diagrams as images or PDFs and share them easily.</p>
              </div>
            </div>
          </section>

          
        </div>
      );
    }

    export default Home;