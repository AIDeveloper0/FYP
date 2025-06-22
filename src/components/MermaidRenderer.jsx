// src/components/MermaidRenderer.jsx
import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

// Initialize once
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose'
});

const MermaidRenderer = ({ chart }) => {
  const containerRef = useRef(null);
  const [renderComplete, setRenderComplete] = useState(false);

  useEffect(() => {
    if (!chart) return;
    
    setRenderComplete(false); // Reset render state when chart changes
    
    // More aggressive line break normalization
    const normalizedChart = chart
      .replace(/\\n/g, '\n')             // Normalize escaped newlines
      .replace(/\\r/g, '')               // Remove carriage returns
      .replace(/\r\n?/g, '\n')           // Normalize CRLF to LF
      .replace(/\s*-->\s*\n\s*/g, ' --> ') // Fix arrows broken across lines
      .replace(/\n\s*\|([^|]+)\|\s*/g, '|$1|') // Fix label breaks
      .replace(/([^\n])(graph TD)/g, '$1\n$2') // Ensure graph declaration is on its own line
      .replace(/(\]|\})([\w])/g, '$1\n$2')     // Ensure proper breaks between node definitions
      .replace(/(-->)([^\n])/g, '$1 $2');      // Ensure proper spacing after arrows
    
    // Debug the normalized chart
    console.log("RENDERING CHART:", normalizedChart);
    
    const renderChart = async () => {
      try {
        const { svg } = await mermaid.render(`mermaid-${Date.now()}`, normalizedChart);
        if (containerRef.current) {
          containerRef.current.innerHTML = svg;
          setRenderComplete(true);
          
          // Add a data attribute to the SVG for easier selection
          const svgElement = containerRef.current.querySelector('svg');
          if (svgElement) {
            svgElement.setAttribute('data-export-ready', 'true');
          }
        }
      } catch (error) {
        console.error("Mermaid rendering error:", error);
        console.error("Problem chart:", normalizedChart);
        if (containerRef.current) {
          containerRef.current.innerHTML = 
            '<div style="padding:20px;border:1px solid #eee;color:#666;">'+
            'Error rendering diagram</div>';
        }
      }
    };
    
    renderChart();
  }, [chart]);

  return (
    <div 
      ref={containerRef} 
      className="mermaid-container" 
      data-render-complete={renderComplete}
      style={{ width: '100%', minHeight: '200px' }} 
    />
  );
};

export default MermaidRenderer;