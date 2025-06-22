import React, { useState, useEffect } from 'react';
import mermaid from 'mermaid';

// API function - we'll define it in this file for now
const createFlowchart = async (text) => {
  try {
    const response = await fetch('/api/diagrams/create-flowchart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating flowchart:', error);
    throw error;
  }
};

const DiagramCreator = () => {
  const [text, setText] = useState('');
  const [diagram, setDiagram] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCreateFlowchart = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await createFlowchart(text);
      
      if (result.success) {
        setDiagram(result.mermaid);
      }
    } catch (err) {
      setError('Failed to create flowchart. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    mermaid.initialize({ 
      startOnLoad: true,
      theme: 'default'
    });
  }, []);

  useEffect(() => {
    if (diagram) {
      mermaid.contentLoaded();
    }
  }, [diagram]);

  return (
    <div className="diagram-creator" style={{ padding: '20px' }}>
      <h2>Create Flowchart</h2>
      
      <div className="input-section">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter a description of your flowchart... (e.g., User login if credentials valid then grant access else show error)"
          rows={5}
          style={{
            width: '100%',
            padding: '12px',
            border: '1px solid #ddd',
            borderRadius: '8px',
            marginBottom: '15px',
            fontSize: '14px',
            fontFamily: 'Arial, sans-serif'
          }}
        />
        
        <button 
          onClick={handleCreateFlowchart} 
          disabled={loading || !text.trim()}
          style={{
            padding: '12px 24px',
            backgroundColor: loading || !text.trim() ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: loading || !text.trim() ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold'
          }}
        >
          {loading ? 'Creating...' : 'Create Flowchart'}
        </button>
      </div>
      
      {error && (
        <div style={{ 
          color: '#dc3545', 
          marginTop: '15px',
          padding: '10px',
          backgroundColor: '#f8d7da',
          border: '1px solid #f5c6cb',
          borderRadius: '4px'
        }}>
          {error}
        </div>
      )}
      
      {diagram && (
        <div className="diagram-output" style={{ marginTop: '30px' }}>
          <h3>Generated Flowchart Code</h3>
          <pre style={{
            backgroundColor: '#f8f9fa',
            padding: '20px',
            borderRadius: '8px',
            overflow: 'auto',
            border: '1px solid #dee2e6',
            fontSize: '14px',
            lineHeight: '1.4'
          }}>
            {diagram}
          </pre>
          
          <div style={{ marginTop: '20px' }}>
            <h3>Flowchart Preview</h3>
            <div 
              className="mermaid"
              style={{
                backgroundColor: 'white',
                padding: '20px',
                border: '1px solid #dee2e6',
                borderRadius: '8px',
                minHeight: '200px'
              }}
            >
              {diagram}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DiagramCreator;