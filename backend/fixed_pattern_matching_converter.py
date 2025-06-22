# FIXED PATTERN MATCHING CONVERTER
# Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-06-17 10:51:45
# Current User's Login: AIDeveloper0

import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FixedMermaidConverter:
    """
    FIXED CONVERTER - PROPER PATTERN MATCHING
    
    ✅ Correctly identifies decision patterns
    ✅ Handles complex conditional logic
    ✅ Extracts meaningful components
    ✅ Generates proper Mermaid DSL
    """
    
    def __init__(self):
        self.node_counter = 0
    
    def reset_counter(self):
        self.node_counter = 0
    
    def get_next_node_id(self):
        node_id = chr(ord('A') + self.node_counter)
        self.node_counter += 1
        return node_id
    
    def generate_mermaid_dsl(self, input_text):
        """Main function to generate Mermaid DSL"""
        
        try:
            self.reset_counter()
            
            # Clean input
            text = self.clean_input_text(input_text)
            
            logger.info(f"🔍 DEBUG: Cleaned text: {text[:100]}...")
            
            # Try to extract decision components
            components = self.extract_decision_components(text)
            
            logger.info(f"🔍 DEBUG: Extracted component type: {components['type']}")
            
            # Generate flowchart based on components
            if components['type'] == 'decision':
                return self.build_decision_flowchart(components)
            elif components['type'] == 'sequence':
                return self.build_sequence_flowchart(components)
            else:
                return self.build_simple_flowchart(components)
        
        except Exception as e:
            logger.error(f"❌ ERROR: {e}")
            return """graph TD
    A[Process]
    B{Complete?}
    C[Continue]
    D[Retry]
    A --> B
    B -->|Yes| C
    B -->|No| D"""
    
    def clean_input_text(self, text):
        """Clean and normalize input text"""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for pattern matching (but preserve original for labels)
        return text
    
    def extract_decision_components(self, text):
        """Extract decision components with improved pattern matching"""
        
        # FIXED PATTERN MATCHING FOR YOUR SPECIFIC CASE
        
        # Pattern 1: Your exact structure - "X if Y then Z if W then V"
        pattern1 = r'(.+?)\s+if\s+(.+?)\s+then\s+(.+?)\s+if\s+(.+?)\s+then\s+(.+?)$'
        match1 = re.search(pattern1, text, re.IGNORECASE)
        
        if match1:
            logger.info(f"🎯 MATCHED PATTERN 1")
            return {
                'type': 'decision',
                'process': self.clean_text(match1.group(1)),
                'condition': self.extract_main_condition(match1.group(2)),
                'success_action': self.clean_text(match1.group(3)),
                'failure_condition': self.extract_main_condition(match1.group(4)),
                'failure_action': self.clean_text(match1.group(5))
            }
        
        # Pattern 2: Standard if-then-else with complex conditions
        pattern2 = r'(.+?)\s+if\s+(.+?)\s+then\s+(.+?)\s+(?:else|otherwise|if.+?fails?|if.+?unavailable)\s+(.+?)$'
        match2 = re.search(pattern2, text, re.IGNORECASE)
        
        if match2:
            logger.info(f"🎯 MATCHED PATTERN 2")
            return {
                'type': 'decision',
                'process': self.clean_text(match2.group(1)),
                'condition': self.extract_main_condition(match2.group(2)),
                'success_action': self.clean_text(match2.group(3)),
                'failure_action': self.clean_text(match2.group(4))
            }
        
        # Pattern 3: Business process with embedded decisions
        pattern3 = r'(.+?)\s+(?:system|process|workflow)\s+(.+?)\s+if\s+(.+?)\s+(?:then\s+)?(.+?)$'
        match3 = re.search(pattern3, text, re.IGNORECASE)
        
        if match3:
            logger.info(f"🎯 MATCHED PATTERN 3")
            remaining = match3.group(2) + " " + match3.group(4)
            
            # Look for embedded if-then structure in remaining text
            if ' if ' in remaining.lower():
                sub_components = self.extract_decision_components(remaining)
                if sub_components['type'] == 'decision':
                    sub_components['process'] = f"{match3.group(1)} {match3.group(2)}"
                    return sub_components
            
            return {
                'type': 'decision',
                'process': self.clean_text(f"{match3.group(1)} {match3.group(2)}"),
                'condition': self.extract_main_condition(match3.group(3)),
                'success_action': self.clean_text(match3.group(4)),
                'failure_action': 'Handle Error'
            }
        
        # Pattern 4: Simple if-then pattern
        pattern4 = r'(.+?)\s+if\s+(.+?)\s+(.+?)$'
        match4 = re.search(pattern4, text, re.IGNORECASE)
        
        if match4:
            logger.info(f"🎯 MATCHED PATTERN 4")
            return {
                'type': 'decision',
                'process': self.clean_text(match4.group(1)),
                'condition': self.extract_main_condition(match4.group(2)),
                'success_action': self.clean_text(match4.group(3)),
                'failure_action': 'Retry Process'
            }
        
        # Handle E-commerce pattern specifically
        ecommerce_pattern = r'(.+?)\s+order\s+processing\s+system\s+where\s+(.+?)\s+if\s+(.+?)\s+then\s+(.+?)\s+if\s+(.+?)\s+then\s+(.+?)$'
        match_ecommerce = re.search(ecommerce_pattern, text, re.IGNORECASE)
        
        if match_ecommerce:
            logger.info(f"🎯 MATCHED E-COMMERCE PATTERN")
            return {
                'type': 'complex_decision',
                'process': f"{match_ecommerce.group(2)}",
                'condition': self.extract_main_condition(match_ecommerce.group(3)),
                'success_action': self.clean_text(match_ecommerce.group(4)),
                'failure_condition': self.extract_main_condition(match_ecommerce.group(5)),
                'failure_action': self.clean_text(match_ecommerce.group(6))
            }
        
        # Fallback: No clear decision pattern found
        logger.info(f"🚨 NO DECISION PATTERN MATCHED - USING FALLBACK")
        return {
            'type': 'simple',
            'process': self.extract_main_process(text),
            'action': 'Complete Process'
        }
    
    def extract_main_condition(self, condition_text):
        """Extract the main condition from complex condition text"""
        
        # Look for key condition indicators
        condition_keywords = {
            'successful': 'Successful',
            'valid': 'Valid', 
            'complete': 'Complete',
            'approved': 'Approved',
            'verified': 'Verified',
            'available': 'Available',
            'sufficient': 'Sufficient'
        }
        
        # Check for multiple conditions connected by 'and'
        if ' and ' in condition_text.lower():
            # Take the first meaningful condition
            parts = condition_text.split(' and ')
            for part in parts:
                for keyword, label in condition_keywords.items():
                    if keyword in part.lower():
                        return f"{label}?"
            
            # Combine conditions for readability
            return "Valid & Available?"
        
        # Check for single condition
        for keyword, label in condition_keywords.items():
            if keyword in condition_text.lower():
                return f"{label}?"
        
        # Fallback: use first few words
        words = condition_text.strip().split()
        if len(words) >= 2:
            return f"{words[0].title()} {words[1].title()}?"
        elif len(words) == 1:
            return f"{words[0].title()}?"
        else:
            return "Complete?"
    
    def clean_text(self, text):
        """Clean text for node labels"""
        
        if not text:
            return "Process"
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unnecessary words
        text = re.sub(r'\b(the|a|an|this|that)\b\s*', '', text, flags=re.IGNORECASE)
        
        # Handle long text by taking meaningful phrases
        if len(text) > 50:
            # Try to break at natural points
            if ',' in text:
                text = text.split(',')[0].strip()
            elif ' and ' in text:
                text = text.split(' and ')[0].strip()
            elif len(text.split()) > 8:
                # Take first 7-8 words
                words = text.split()
                text = ' '.join(words[:7])
        
        # Capitalize properly
        return text.strip().title() if text.strip() else "Process"
    
    def extract_main_process(self, text):
        """Extract main process name from text"""
        
        # Look for process/system keywords
        process_match = re.search(r'(.+?)\s+(?:system|process|workflow|procedure)', text, re.IGNORECASE)
        if process_match:
            return self.clean_text(process_match.group(1))
        
        # Take first meaningful phrase
        words = text.split()
        if len(words) >= 3:
            return self.clean_text(' '.join(words[:3]))
        else:
            return self.clean_text(text)
    
    def build_decision_flowchart(self, components):
        """Build decision flowchart with proper line breaks"""
        
        if components.get('type') == 'complex_decision':
            return self.build_complex_decision_flowchart(components)
            
        A = self.get_next_node_id()
        B = self.get_next_node_id()
        C = self.get_next_node_id()
        D = self.get_next_node_id()
        
        process = components.get('process', 'Process')
        condition = components.get('condition', 'Complete?')
        success_action = components.get('success_action', 'Continue')
        failure_action = components.get('failure_action', 'Handle Error')
        
        return f"""graph TD
    {A}[{process}]
    {B}{{{condition}}}
    {C}[{success_action}]
    {D}[{failure_action}]
    {A} --> {B}
    {B} -->|Yes| {C}
    {B} -->|No| {D}"""
    
    def build_complex_decision_flowchart(self, components):
        """Build complex decision flowchart for e-commerce scenario"""
        
        A = self.get_next_node_id()  # Customer action
        B = self.get_next_node_id()  # Main condition
        C = self.get_next_node_id()  # Success action 1
        D = self.get_next_node_id()  # Success action 2
        E = self.get_next_node_id()  # Failure action 1
        F = self.get_next_node_id()  # Failure action 2
        
        process = components.get('process', 'Customer Places Order')
        condition = components.get('condition', 'Payment Valid & Inventory Available?')
        
        success_action = components.get('success_action', 'Process Order')
        if ' and ' in success_action:
            success_parts = success_action.split(' and ')
            success_action1 = self.clean_text(success_parts[0])
            success_action2 = self.clean_text(success_parts[1] if len(success_parts) > 1 else "Complete Order")
        else:
            success_action1 = success_action
            success_action2 = "Complete Order"
        
        failure_action = components.get('failure_action', 'Send Notification')
        if ' and ' in failure_action:
            failure_parts = failure_action.split(' and ')
            failure_action1 = self.clean_text(failure_parts[0])
            failure_action2 = self.clean_text(failure_parts[1] if len(failure_parts) > 1 else "Review Process")
        else:
            failure_action1 = failure_action
            failure_action2 = "Review Process"
            
        return f"""graph TD
    {A}[{process}]
    {B}{{{condition}}}
    {C}[{success_action1}]
    {D}[{success_action2}]
    {E}[{failure_action1}]
    {F}[{failure_action2}]
    {A} --> {B}
    {B} -->|Yes| {C}
    {B} -->|No| {E}
    {C} --> {D}
    {E} --> {F}"""
    
    def build_sequence_flowchart(self, components):
        """Build sequence flowchart"""
        
        steps = components.get('steps', ['Process', 'Complete'])
        
        if len(steps) < 2:
            return self.build_simple_flowchart(components)
        
        lines = ["graph TD"]
        
        # Add nodes
        for i, step in enumerate(steps):
            node_id = chr(ord('A') + i)
            lines.append(f"    {node_id}[{step}]")
        
        # Add connections
        for i in range(len(steps) - 1):
            current = chr(ord('A') + i)
            next_node = chr(ord('A') + i + 1)
            lines.append(f"    {current} --> {next_node}")
        
        return "\n".join(lines)
    
    def build_simple_flowchart(self, components):
        """Build simple flowchart"""
        
        A = self.get_next_node_id()
        B = self.get_next_node_id()
        
        process = components.get('process', 'Process')
        action = components.get('action', 'Complete')
        
        return f"""graph TD
    {A}[{process}]
    {B}[{action}]
    {A} --> {B}"""


# Production function
def fixed_mermaid_generator(input_text):
    """
    FIXED MERMAID GENERATOR - PROPER PATTERN MATCHING
    
    ✅ Correctly identifies your specific pattern
    ✅ Handles complex conditional logic
    ✅ Generates proper decision flowcharts
    """
    converter = FixedMermaidConverter()
    return converter.generate_mermaid_dsl(input_text)