export const createFlowchart = async (text) => {
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