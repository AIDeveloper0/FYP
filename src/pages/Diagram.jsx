import React, { useState, useRef } from "react";
import { toast } from "react-toastify";
import MermaidRenderer from "../components/MermaidRenderer";
import { parseFlowchartInput } from "../utils/flowchartParser";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import "./diagram.css";

const diagramTypes = [
  { name: "Flowchart" },
  { name: "Sequence" },
  { name: "Class" },
  { name: "Use Case" },
  { name: "DFD" },
];

// Enhanced API function for backend flowchart generation
const createFlowchartFromBackend = async (text) => {
  try {
    console.log('📡 Calling backend flowchart API...');
    const response = await fetch('http://127.0.0.1:5000/api/diagrams/create-flowchart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log('✅ Backend response:', result);

    if (result.data && result.data.mermaid) {
      return { mermaid: result.data.mermaid };
    } else {
      throw new Error('No Mermaid data in response');
    }
  } catch (error) {
    console.error('❌ Backend flowchart generation failed:', error);
    throw error;
  }
};

// Helper function to convert ReactFlow to Mermaid (if needed)
const convertReactFlowToMermaid = (reactflowData) => {
  if (!reactflowData || !reactflowData.nodes) {
    throw new Error('Invalid ReactFlow data');
  }

  let mermaid = "graph TD\n";
  
  // Add nodes
  reactflowData.nodes.forEach(node => {
    const label = node.data?.label || node.id;
    const cleanLabel = label.replace(/["\n]/g, ' ').trim();
    
    if (node.type === 'input') {
      mermaid += `  ${node.id}(["${cleanLabel}"])\n`;
    } else if (node.type === 'output') {
      mermaid += `  ${node.id}(["${cleanLabel}"])\n`;
    } else if (cleanLabel.includes('?') || cleanLabel.includes('decision')) {
      mermaid += `  ${node.id}{${cleanLabel}}\n`;
    } else {
      mermaid += `  ${node.id}["${cleanLabel}"]\n`;
    }
  });

  // Add edges
  if (reactflowData.edges) {
    reactflowData.edges.forEach(edge => {
      if (edge.label) {
        mermaid += `  ${edge.source} -->|${edge.label}| ${edge.target}\n`;
      } else {
        mermaid += `  ${edge.source} --> ${edge.target}\n`;
      }
    });
  }

  return mermaid;
};

// Add this helper function before the component
const validateMermaidSyntax = (mermaidCode) => {
  try {
    // Basic validation checks
    if (!mermaidCode || typeof mermaidCode !== 'string') {
      throw new Error('Invalid mermaid code type');
    }
    
    // Check for required structure
    if (!mermaidCode.includes('graph TD') && !mermaidCode.includes('graph LR')) {
      throw new Error('Missing graph declaration');
    }
    
    // Check for proper line structure
    const lines = mermaidCode.split('\n');
    let hasNodes = false;
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('graph') && !trimmed.startsWith('classDef')) {
        // Check for valid node or edge syntax
        if (trimmed.includes('[') || trimmed.includes('(') || trimmed.includes('{') || trimmed.includes('-->')) {
          hasNodes = true;
        }
      }
    }
    
    if (!hasNodes) {
      throw new Error('No valid nodes or edges found');
    }
    
    return true;
  } catch (error) {
    console.error('Mermaid validation failed:', error);
    return false;
  }
};

// Add this helper function to clean Mermaid code
const cleanMermaidCode = (mermaidCode) => {
  if (!mermaidCode || typeof mermaidCode !== 'string') {
    return null;
  }
  
  // Split into lines and process each
  const lines = mermaidCode.split('\n');
  const cleanedLines = [];
  
  for (let line of lines) {
    // Remove any problematic characters
    let cleaned = line
      .replace(/[🚀📝⚙️❓✅❌🏁🎉⏳💳📦🏷️📧🏭🔄⏸️👥]/g, '')
      .trim();
    
    // Skip empty lines except after graph declaration
    if (cleaned || (cleanedLines.length === 1 && cleanedLines[0].startsWith('graph'))) {
      cleanedLines.push(cleaned);
    }
  }
  
  // Ensure proper structure
  if (cleanedLines.length === 0 || !cleanedLines[0].startsWith('graph')) {
    return `graph TD
    A["Start"] --> B["Process"]
    B --> C["End"]
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px`;
  }
  
  return cleanedLines.join('\n');
};

const ErrorBoundary = ({ children, fallback }) => {
  const [hasError, setHasError] = React.useState(false);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    const handleError = (error) => {
      console.error('🛡️ Error Boundary caught:', error);
      setError(error);
      setHasError(true);
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleError);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleError);
    };
  }, []);

  if (hasError) {
    return fallback || (
      <div style={{ padding: '20px', background: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '4px' }}>
        <h4>⚠️ Something went wrong</h4>
        <p>The diagram couldn't be displayed, but the application is still working.</p>
        <button onClick={() => setHasError(false)} style={{ padding: '5px 10px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
          Try Again
        </button>
      </div>
    );
  }

  return children;
};

export default function DiagramPage() {
  const [selected, setSelected] = useState(null);
  const [input, setInput] = useState("");
  const [mermaidCode, setMermaidCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showDSL, setShowDSL] = useState(false);
  const [inputWarning, setInputWarning] = useState(null);
  const diagramRef = useRef(null);

  // Input analysis
  const analyzeInput = (text) => {
    const length = text.length;
    const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    
    if (length > 3000) {
      setInputWarning({
        level: 'severe',
        message: `Very long input (${length} chars, ${wordCount} words). Will be processed in chunks.`
      });
    } else if (length > 2000) {
      setInputWarning({
        level: 'warning',
        message: `Long input (${length} chars, ${wordCount} words). May be simplified for better processing.`
      });
    } else if (length > 1000) {
      setInputWarning({
        level: 'info',
        message: `Medium input (${length} chars, ${wordCount} words). Should process well.`
      });
    } else {
      setInputWarning(null);
    }
  };

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInput(newValue);
    
    // Analyze input for warnings (only for flowchart)
    if (selected === "Flowchart") {
      analyzeInput(newValue);
    } else {
      setInputWarning(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) {
      setError("Please enter a description");
      return;
    }

    setLoading(true);
    setError(null);
    setMermaidCode("");

    try {
      let generatedDiagram;

      if (selected === "Flowchart") {
        try {
          console.log('📡 Using backend...');
          const result = await createFlowchartFromBackend(input);
          generatedDiagram = result.mermaid;
        } catch (backendError) {
          console.warn('⚠️ Backend failed, using fallback...');
          generatedDiagram = await parseFlowchartInput(input);
          toast.warning("Used fallback processing");
        }
      } else {
        generatedDiagram = await parseFlowchartInput(input);
      }

      // Set the diagram code
      setMermaidCode(generatedDiagram || `graph TD
      A["Start"] --> B["${selected || 'Process'}"] --> C["End"]`);
    } catch (error) {
      console.error('❌ Diagram generation failed:', error);
      setError(`Failed to generate diagram: ${error.message}`);

      // Set a fallback diagram
      setMermaidCode(`graph TD
      A["Start"] --> B["${selected || 'Process'}"] --> C["End"]`);
    } finally {
      setLoading(false);
    }
  };

  const copyDSLCode = () => {
    if (mermaidCode) {
      navigator.clipboard.writeText(mermaidCode).then(() => {
        toast.success("DSL code copied to clipboard!");
      }).catch(() => {
        toast.error("Failed to copy DSL code");
      });
    }
  };

  const exportAsPNG = () => {
    if (!diagramRef.current) {
      toast.error("Diagram reference not available");
      return;
    }

    console.log("Attempting export, HTML:", diagramRef.current.innerHTML);

    // Allow more time for rendering to complete
    setTimeout(() => {
      const diagramElement = diagramRef.current.querySelector(".mermaid-container svg");

      if (!diagramElement) {
        toast.error("No diagram to export. Try refreshing the diagram first.");
        console.error("SVG element not found during export. Available elements:", 
          diagramRef.current.innerHTML);
        return;
      }

      toast.info("Exporting as PNG...");

      try {
        const svgRect = diagramElement.getBoundingClientRect();
        const svgClone = diagramElement.cloneNode(true);
        const svgData = new XMLSerializer().serializeToString(svgClone);

        const canvas = document.createElement('canvas');
        canvas.width = svgRect.width;
        canvas.height = svgRect.height;

        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
          try {
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            const link = document.createElement('a');
            link.download = `${selected || 'diagram'}-${Date.now()}.png`;
            link.href = canvas.toDataURL('image/png');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            toast.success("Diagram exported as PNG successfully!");
          } catch (drawErr) {
            console.error("Error during canvas operations:", drawErr);
            toast.error("Failed to generate PNG: " + drawErr.message);
          }
        };

        img.onerror = (err) => {
          console.error("Image loading error:", err);
          toast.error("Failed to load SVG into image");
        };

        // Handle SVG data more reliably
        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));

      } catch (err) {
        console.error("Export error:", err);
        toast.error("Failed to export: " + err.message);
      }
    }, 1000); // Increased timeout to 1000ms
  };

  const exportAsPDF = () => {
    if (!diagramRef.current) return;

    setTimeout(() => {
      const diagramElement = diagramRef.current.querySelector(".mermaid-container svg");

      if (!diagramElement) {
        toast.error("No diagram to export. Try refreshing the diagram first.");
        return;
      }

      toast.info("Exporting as PDF...");

      const svgRect = diagramElement.getBoundingClientRect();
      const svgClone = diagramElement.cloneNode(true);
      const svgData = new XMLSerializer().serializeToString(svgClone);

      const canvas = document.createElement('canvas');
      canvas.width = svgRect.width;
      canvas.height = svgRect.height;

      const img = new Image();
      img.onload = () => {
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);

        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF();
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (svgRect.height * pdfWidth) / svgRect.width;

        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save(`${selected}-diagram.pdf`);
        toast.success("Diagram exported as PDF successfully!");
      };

      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="diagram-page p-4">
        <nav className="diagram-menu">
          {diagramTypes.map((type) => (
            <button
              key={type.name}
              className={`diagram-menu-item${
                selected === type.name ? " active" : ""
              }`}
              onClick={() => setSelected(type.name)}
            >
              {type.name}
            </button>
          ))}
          
          {mermaidCode && (
            <div className="menu-export-controls">
              <button
                onClick={exportAsPNG}
                className="export-menu-button"
                disabled={!mermaidCode}
              >
                <span role="img" aria-label="Export">📥</span> PNG
              </button>
              <button
                onClick={exportAsPDF}
                className="export-menu-button"
                disabled={!mermaidCode}
              >
                <span role="img" aria-label="Export">📄</span> PDF
              </button>
            </div>
          )}
        </nav>
        {selected ? (
          <div className="diagram-interface">
            <div className="diagram-input">
              <form onSubmit={handleSubmit}>
                <label>
                  Enter {selected} description:
                  <textarea
                    value={input}
                    onChange={handleInputChange}
                    placeholder={
                      selected === "Flowchart" 
                        ? `Describe your ${selected.toLowerCase()} in natural language...\nExample: User login if credentials valid then grant access else show error\n\n💡 Tip: For complex processes, break into clear if-then-else statements.`
                        : `Describe your ${selected.toLowerCase()} here...\nExample: Start -> Process -> Decision\nIf yes -> End\nIf no -> Process`
                    }
                    required
                  />
                </label>
                
                {/* Input Analysis Display */}
                {selected === "Flowchart" && (
                  <div className="input-analysis">
                    <div className="input-stats">
                      <span>Characters: {input.length}</span>
                      <span>Words: {input.split(/\s+/).filter(w => w.length > 0).length}</span>
                      <span>Sentences: {input.split(/[.!?]+/).filter(s => s.trim().length > 0).length}</span>
                    </div>
                    
                    {inputWarning && (
                      <div className={`input-warning ${inputWarning.level}`}>
                        <strong>{inputWarning.level === 'severe' ? '⚠️' : inputWarning.level === 'warning' ? '📝' : 'ℹ️'}</strong>
                        {inputWarning.message}
                      </div>
                    )}
                  </div>
                )}
                
                <button type="submit" className="submit-button" disabled={loading}>
                  {loading ? `Generating ${selected} Diagram...` : `Generate ${selected} Diagram`}
                </button>
              </form>
              {error && <div className="error-message">{error}</div>}
              
              {/* DSL Code Display Box */}
              {mermaidCode && (
                <div className="dsl-code-section">
                  <div className="dsl-code-header">
                    <h4>Generated DSL Code ({selected} Diagram)</h4>
                    <div className="dsl-controls">
                      <button 
                        onClick={() => setShowDSL(!showDSL)}
                        className="toggle-dsl-button"
                      >
                        {showDSL ? "Hide Code" : "Show Code"}
                      </button>
                      {showDSL && (
                        <button 
                          onClick={copyDSLCode}
                          className="copy-dsl-button"
                          title="Copy DSL code to clipboard"
                        >
                          📋 Copy
                        </button>
                      )}
                    </div>
                  </div>
                  {showDSL && (
                    <div className="dsl-code-container">
                      <pre className="dsl-code-display">
                        <code>{mermaidCode}</code>
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="diagram-display" ref={diagramRef}>
              <ErrorBoundary>
                {mermaidCode ? (
                  <div className="diagram-container" style={{ height: '100%', width: '100%' }}>
                    <MermaidRenderer chart={mermaidCode} />
                  </div>
                ) : (
                  <div className="diagram-placeholder">
                    <h3>{selected} Diagram</h3>
                    <p>Diagram will be shown here based on your input.</p>
                    {loading && <div>🔄 Generating...</div>}
                  </div>
                )}
              </ErrorBoundary>
            </div>
          </div>
        ) : (
          <div className="diagram-content">
            <h2>Select a diagram type from the menu above.</h2>
          </div>
        )}
      </div>
    </div>
  );
}