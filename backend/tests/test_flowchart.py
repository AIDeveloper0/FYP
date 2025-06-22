"""
Tests for the flowchart converter
"""
import pytest
import re
from app.converters.flowchart_converter import FlowchartConverter


class TestFlowchartConverter:
    """Test suite for the FlowchartConverter class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.converter = FlowchartConverter()
    
    def test_simple_flow(self):
        """Test a simple process flow"""
        input_text = "Process user registration"
        result = self.converter.convert(input_text)
        
        assert "graph TD" in result
        assert "[\"Process User Registration\"]" in result
        assert "-->" in result
    
    def test_decision_flow(self):
        """Test a decision process flow"""
        input_text = "User login if credentials valid then grant access else show error message"
        result = self.converter.convert(input_text)
        
        assert "graph TD" in result
        assert "{Valid?}" in result
        assert "|Yes|" in result
        assert "|No|" in result
        assert "[\"Grant Access\"]" in result
        assert "[\"Show Error Message\"]" in result
    
    def test_complex_decision_flow(self):
        """Test a complex decision process flow"""
        input_text = "E-commerce system where customer places order if payment successful and inventory available then process order and ship product if payment failed or inventory unavailable then notify customer and cancel order"
        result = self.converter.convert(input_text)
        
        assert "graph TD" in result
        assert "{Successful?}" in result or "{Payment Successful?}" in result
        assert "|Yes|" in result
        assert "|No|" in result
        assert "[\"Process Order\"]" in result or "[\"Ship Product\"]" in result
        assert "[\"Notify Customer\"]" in result or "[\"Cancel Order\"]" in result
    
    def test_sequence_flow(self):
        """Test a sequence flow"""
        input_text = "First collect user data, then validate input, finally save to database"
        result = self.converter.convert(input_text)
        
        assert "graph TD" in result
        assert "[\"Collect User Data\"]" in result
        assert "[\"Validate Input\"]" in result
        assert "[\"Save To Database\"]" in result
    
    def test_extract_condition(self):
        """Test the condition extraction functionality"""
        conditions = [
            ("user credentials are valid", "Valid?"),
            ("payment is successful", "Successful?"),
            ("inventory is available", "Available?"),
            ("form data is complete", "Complete?"),
            ("user is authenticated and authorized", "Authenticated & Authorized?")
        ]
        
        for input_condition, expected in conditions:
            result = self.converter.extract_condition(input_condition)
            assert result == expected or expected in result
    
    def test_invalid_input_handling(self):
        """Test handling of invalid or problematic input"""
        inputs = [
            "",                           # Empty string
            "a",                          # Too short
            "x" * 2000,                   # Very long input
            "!@#$%^&*()",                 # Special characters only
            "1234567890"                  # Numbers only
        ]
        
        for input_text in inputs:
            # Should not raise exceptions but return a diagram
            result = self.converter.convert(input_text)
            assert "graph TD" in result
            assert "-->" in result
    
    def test_extract_main_action(self):
        """Test the action extraction functionality"""
        test_cases = [
            ("system will process payment", "Process Payment"),
            ("user must enter credentials", "Enter Credentials"),
            ("to validate user input", "Validate User Input")
        ]
        
        for text, expected in test_cases:
            result = self.converter.extract_main_action(text)
            assert result is not None
            # Should contain the key parts of the expected result
            assert expected.lower() in result.lower()
    
    def test_build_decision_flowchart(self):
        """Test building a decision flowchart"""
        components = {
            'type': 'decision',
            'process': 'User Login',
            'condition': 'Credentials Valid?',
            'success_action': 'Grant Access',
            'failure_action': 'Show Error'
        }
        
        result = self.converter.build_decision_flowchart(components)
        assert "graph TD" in result
        assert "[\"User Login\"]" in result
        assert "{Credentials Valid?}" in result
        assert "[\"Grant Access\"]" in result
        assert "[\"Show Error\"]" in result
        assert "-->|Yes|" in result
        assert "-->|No|" in result
    
    def test_mermaid_syntax_validity(self):
        """Test that generated Mermaid code has valid syntax"""
        test_inputs = [
            "User login if credentials valid then grant access else show error message",
            "Order processing system where customer submits order if payment successful then ship order if payment failed then cancel order",
            "First collect data, then validate input, finally save to database"
        ]
        
        for input_text in test_inputs:
            result = self.converter.convert(input_text)
            
            # Check syntax validity
            assert result.startswith("graph TD")
            assert "-->" in result
            assert "[" in result and "]" in result
            
            # Check for balanced brackets and quotes
            assert result.count("[") == result.count("]")
            assert result.count("{") == result.count("}")
            # Even number of quotes
            assert result.count("\"") % 2 == 0
            
            # Check node format
            node_pattern = r'[A-Z]\[[^\[\]]+\]'
            nodes = re.findall(node_pattern, result)
            assert len(nodes) > 0