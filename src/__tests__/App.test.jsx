import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    // Render the component
    render(<App />);
    
    // You'll need to update this assertion based on what's actually in your App component
    // For example, if your App has a heading:
    expect(document.body.textContent).toBeDefined();
  });
});

describe('Flowchart Converter', () => {
    it('should convert a complex decision flow correctly', () => {
        const inputText = "E-commerce system where customer places order if payment successful and inventory available then process order and ship product if payment failed or inventory unavailable then notify customer and cancel order";
        const result = converter.convert(inputText);
        
        expect(result).toContain("graph TD");
        expect(result).toContain("{Successful?}");
        expect(result).toContain("{Payment Successful?}");
    });

    it('should convert a sequence flow correctly', () => {
        const inputText = "First collect user data, then validate input, finally save to database";
        const result = converter.convert(inputText);
        
        expect(result).toContain("graph TD");
        expect(result).toContain("[\"Collect User Data\"]");
    });

    it('should extract main action correctly', () => {
        const testCases = [
            { text: "system will process payment", expected: "Process Payment" },
            { text: "user must enter credentials", expected: "Enter Credentials" },
            { text: "to validate user input", expected: "Validate User Input" }
        ];

        testCases.forEach(({ text, expected }) => {
            const result = converter.extract_main_action(text);
            expect(result).not.toBeNull();
            expect(result.toLowerCase()).toContain(expected.toLowerCase());
        });
    });
});

import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        include: ['**/*.{test,spec}.{js,jsx,mjs,cjs}'],
        exclude: ['node_modules', 'dist', 'cypress', '.idea', '.git', 'cache', 'output', 'temp']
    }
});