// src/utils/flowchartParser.js

// Parse input and generate a flowchart
export const parseFlowchartInput = async (input) => {
  console.log("🔄 Starting diagram generation for:", input.substring(0, 50) + "...");

  try {
    console.log("🤖 Attempting flowchart generation...");
    
    // Extract key phrases from input to use in a fallback diagram
    const phrases = input
      .split(/[,.;:]/)
      .map(p => p.trim())
      .filter(p => p.length > 0)
      .slice(0, 5);
    
    try {
      // Try to get diagram from API
      const result = await generateFlowchartFromAPI(input);
      
      // Validate the result is proper Mermaid syntax
      if (result && (result.trim().startsWith("flowchart") || result.trim().startsWith("graph"))) {
        console.log("✅ Flowchart generation succeeded!");
        return result;
      } else {
        throw new Error("API returned invalid flowchart syntax");
      }
    } catch (apiError) {
      console.error("API Error:", apiError);
      
      // Generate a simple flowchart using the extracted phrases
      const fallbackFlowchart = generateFallbackFlowchart(phrases);
      console.log("⚠️ Using fallback flowchart generator");
      return fallbackFlowchart;
    }
  } catch (error) {
    console.error("❌ Flowchart generation failed:", error.message);
    
    // Return a simple, valid flowchart on error
    return `flowchart TD
    A[Start] 
    B["Error: ${error.message.replace(/"/g, "'")}"]
    C[End]
    A --> B
    B --> C`;
  }
};

// API client function
async function generateFlowchartFromAPI(prompt) {
    try {
        console.log('🔧 Calling FIXED API with prompt:', prompt);
        
        const response = await fetch('http://localhost:8000/generate-flowchart', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        });

        console.log('🔍 RAW RESPONSE STATUS:', response.status);
        
        const data = await response.json();
        console.log('🔍 RAW API RESPONSE:', data);
        console.log('🔍 FLOWCHART FIELD:', JSON.stringify(data.flowchart));
        
        // VALIDATE FIXES - Updated for multiline format
        const flowchart = data.flowchart || '';
        const lines = flowchart.split('\n');
        
        const validations = {
            'Proper graph TD syntax': flowchart.startsWith('graph TD'),
            'No flowchart TD': !flowchart.includes('flowchart TD'),
            'No truncation dots': !flowchart.includes('...'),
            'Has decision nodes': flowchart.includes('{') && flowchart.includes('}'),
            'Has connections': flowchart.includes('-->'),
            'Has square brackets': flowchart.includes('[') && flowchart.includes(']'),
            'Multiline format': lines.length > 1,
            'Proper indentation': lines.slice(1).every(line => !line.trim() || line.startsWith('    '))
        };
        
        console.log('✅ VALIDATION RESULTS:', validations);
        const allPassed = Object.values(validations).every(v => v);
        console.log('🎯 ALL VALIDATIONS PASSED:', allPassed);
        
        // Log the actual multiline format
        console.log('📝 MULTILINE MERMAID:');
        console.log(flowchart);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        if (data.flowchart) {
            console.log('✅ Fixed API returned valid multiline flowchart');
            return data.flowchart;
        } else {
            console.error('❌ No flowchart in API response');
            throw new Error('Invalid flowchart format received from API');
        }
        
    } catch (error) {
        console.error('❌ API call failed:', error);
        throw error;
    }
}

// Generate a simple flowchart from key phrases
function generateFallbackFlowchart(phrases) {
  let flowchart = "flowchart TD\n";
  
  // Add nodes
  phrases.forEach((phrase, i) => {
    const nodeId = String.fromCharCode(65 + i); // A, B, C, etc.
    flowchart += `    ${nodeId}[${sanitizeForMermaid(phrase)}]\n`;
  });
  
  // Add connections
  for (let i = 0; i < phrases.length - 1; i++) {
    const currentNodeId = String.fromCharCode(65 + i);
    const nextNodeId = String.fromCharCode(65 + i + 1);
    flowchart += `    ${currentNodeId} --> ${nextNodeId}\n`;
  }
  
  return flowchart;
}

// Sanitize text for Mermaid
function sanitizeForMermaid(text) {
  return text.replace(/"/g, "'").substring(0, 30);
}

// Convert a simple flowchart to a complex one with decision points
function convertToComplexFlowchart(simpleFlowchart) {
  // If we already have a complex flowchart with decisions, return it
  if (simpleFlowchart.includes("{") && 
      (simpleFlowchart.includes("|Yes|") || simpleFlowchart.includes("|No|"))) {
    return simpleFlowchart;
  }
  
  // Convert from flowchart TD to graph TD
  let result = simpleFlowchart.replace("flowchart TD", "graph TD");
  
  // Extract nodes and look for conditional statements
  const lines = result.split('\n');
  const newLines = [];
  const connections = [];
  const nodes = {};
  
  // First pass: collect nodes
  lines.forEach(line => {
    if (line.trim() === "" || line.trim() === "graph TD") {
      newLines.push(line);
      return;
    }
    
    // Check if this is a node definition
    const nodeMatch = line.match(/\s*([A-Z])\["([^"]+)"\]/);
    if (nodeMatch) {
      const [_, id, text] = nodeMatch;
      nodes[id] = text;
      
      // Check if this contains conditional text
      if (text.toLowerCase().includes("if ") || 
          text.toLowerCase().includes("condition") ||
          text.toLowerCase().includes("acceptable")) {
        // Convert to decision diamond
        const parts = text.split("if ");
        if (parts.length > 1) {
          const condition = parts[1].split(",")[0];
          newLines.push(`    ${id}{${condition}?}`);
        } else {
          newLines.push(line);
        }
      } else {
        newLines.push(line);
      }
    }
    // Check if this is a connection
    else if (line.includes("-->")) {
      connections.push(line);
    } else {
      newLines.push(line);
    }
  });
  
  // Add connections
  newLines.push(...connections);
  
  return newLines.join('\n');
}