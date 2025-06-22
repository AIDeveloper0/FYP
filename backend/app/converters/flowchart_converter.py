"""
Enhanced Flowchart Converter with Advanced NLP
Converts natural language descriptions into Mermaid flowchart diagrams
Uses spaCy for improved language understanding and pattern extraction
"""
import spacy
import re
import logging
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedFlowchartConverter:
    """
    Advanced NLP-based flowchart converter using spaCy for superior pattern recognition
    """
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model loaded successfully")
        except OSError:
            logger.error("❌ spaCy model not found - installing...")
            import subprocess
            try:
                subprocess.check_call(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("✅ spaCy model installed and loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to install spaCy model: {str(e)}")
                self.nlp = None
        
        # Dynamic patterns for different types of processes
        self.conditional_keywords = ['if', 'when', 'whenever', 'should', 'must', 'check', 'verify', 'validate']
        self.action_keywords = ['then', 'process', 'send', 'update', 'generate', 'create', 'notify', 'charge']
        self.alternative_keywords = ['else', 'otherwise', 'if not', 'unless', 'except', 'alternative']
        self.sequence_keywords = ['then', 'next', 'after', 'subsequently', 'following', 'and then']
        
        self.node_counter = 0
        self.edge_counter = 0
        self.error_occurred = False
        self.last_error = None
        
        logger.info("✅ EnhancedFlowchartConverter initialized")

    def convert(self, text_input: str) -> str:
        """
        Main public method to convert text to flowchart
        
        Args:
            text_input: The English text to convert
            
        Returns:
            str: Mermaid DSL code
        """
        try:
            self.error_occurred = False
            self.last_error = None
            
            logger.info(f"Processing flowchart text: {text_input}")
            
            # Clean and normalize input text
            text_input = text_input.strip()
            if not text_input:
                logger.warning("Empty input text provided")
                return self._create_simple_flowchart()
            
            # Process text to flowchart data
            flowchart_data = self.convert_text_to_flowchart(text_input)
            
            # Validate Mermaid syntax before returning
            mermaid_code = flowchart_data["mermaid"]
            if "None -->" in mermaid_code:
                logger.warning("Invalid 'None' node detected in Mermaid output, fixing...")
                mermaid_code = mermaid_code.replace("None -->", "start -->")
            
            # Additional validation to ensure proper line breaks between node definitions
            lines = mermaid_code.split('\n')
            fixed_lines = []
            
            # Ensure graph declaration is present
            if not any(line.strip() == "graph TD" for line in lines):
                fixed_lines.append("graph TD")
            
            for i, line in enumerate(lines):
                if line.strip() == "graph TD" and i > 0:
                    # Don't add duplicate graph declarations
                    continue
                    
                # Check for multiple node definitions in a single line
                if line.strip() and ']' in line and '[' in line.split(']', 1)[1]:
                    parts = re.findall(r'(\S+\[.*?\]|\S+\{.*?\})', line)
                    for part in parts:
                        fixed_lines.append(part)
                # Check for node and edge definition on the same line
                elif line.strip() and (']' in line or '}' in line) and '-->' in line:
                    node_part = line.split('-->', 1)[0].strip()
                    edge_part = '-->' + line.split('-->', 1)[1].strip()
                    fixed_lines.append(node_part)
                    fixed_lines.append(edge_part)
                else:
                    fixed_lines.append(line)
            
            # Reconstruct the mermaid code with proper line breaks
            mermaid_code = '\n'.join(fixed_lines)
            
            # Final format verification
            # Ensure all nodes and edges are on separate lines with proper indentation
            lines = mermaid_code.split('\n')
            final_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    final_lines.append("")
                elif line == "graph TD":
                    final_lines.append("graph TD")
                elif line.startswith("classDef"):
                    final_lines.append("    " + line)
                elif ("[" in line or "{" in line) and not "-->" in line:
                    # Node definition
                    final_lines.append("    " + line)
                elif "-->" in line:
                    # Edge definition
                    final_lines.append("    " + line)
                else:
                    # Other content
                    final_lines.append(line)
            
            mermaid_code = '\n'.join(final_lines)
            
            return mermaid_code

        except Exception as e:
            self.error_occurred = True
            self.last_error = str(e)
            logger.error(f"❌ Error in flowchart conversion: {str(e)}")
            
            # Return fallback flowchart
            return """graph TD
    A["Start"] --> B["Process"]
    B --> C["End"]
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px"""

    def _create_simple_flowchart(self) -> str:
        """Create a simple default flowchart for edge cases"""
        return """graph TD
    start["Start"] --> process["Process"]
    process --> end["End"]
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px"""

    def _extract_sentence_structure(self, text: str) -> Dict[str, Any]:
        """Dynamically extract sentence structure using spaCy NLP with improved sequence handling"""
        if not self.nlp:
            return self._fallback_structure_extraction(text)
        
        doc = self.nlp(text)
        
        structure = {
            'subjects': [],
            'verbs': [],
            'objects': [],
            'conditions': [],
            'actions': [],
            'entities': [],
            'sentences': []
        }
        
        # Extract sentences
        for sent in doc.sents:
            structure['sentences'].append(sent.text.strip())
        
        # Extract linguistic elements
        for token in doc:
            # Subjects (who/what is acting)
            if token.dep_ in ['nsubj', 'nsubjpass']:
                structure['subjects'].append(token.text.lower())
            
            # Verbs (actions)
            if token.pos_ == 'VERB' and not token.is_stop:
                structure['verbs'].append(token.lemma_.lower())
            
            # Objects (what's being acted upon)
            if token.dep_ in ['dobj', 'pobj', 'obj']:
                structure['objects'].append(token.text.lower())
        
        # Extract named entities
        for ent in doc.ents:
            structure['entities'].append({
                'text': ent.text,
                'label': ent.label_,
                'type': spacy.explain(ent.label_)
            })
        
        # Integrate sequential actions directly here
        sequential_actions = self._extract_sequential_actions_from_text(text)
        if sequential_actions:
            # Group actions by sentence to maintain proper sequence
            structure['sequences'] = [{'actions': [a['action'] for a in sequential_actions]}]
        else:
            # Fallback to empty sequences
            structure['sequences'] = []
        
        logger.info(f"🧠 Extracted structure: {len(structure['sentences'])} sentences, {len(structure['verbs'])} verbs")
        logger.info(f"🧠 Found {len(structure.get('sequences', [])[0]['actions']) if structure.get('sequences') else 0} sequential actions")
        
        return structure

    def _identify_process_patterns(self, text: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically identify different process patterns in the text"""
        
        patterns = {
            'conditionals': [],
            'sequences': [],
            'parallels': [],
            'loops': [],
            'decisions': []
        }
        
        text_lower = text.lower()
        sentences = structure['sentences']
        
        # Identify conditional patterns
        for i, sentence in enumerate(sentences):
            sent_lower = sentence.lower()
            
            # Find IF-THEN patterns
            if any(keyword in sent_lower for keyword in self.conditional_keywords):
                condition_match = self._extract_if_then_pattern(sentence)
                if condition_match:
                    patterns['conditionals'].append({
                        'sentence_index': i,
                        'condition': condition_match['condition'],
                        'then_action': condition_match['then_action'],
                        'else_action': condition_match.get('else_action'),
                        'original': sentence
                    })
            
            # Find sequential patterns
            if any(keyword in sent_lower for keyword in self.sequence_keywords):
                patterns['sequences'].append({
                    'sentence_index': i,
                    'sequence_type': self._identify_sequence_type(sentence),
                    'actions': self._extract_sequential_actions(sentence),
                    'original': sentence
                })
            
            # Find decision points
            if '?' in sentence or any(word in sent_lower for word in ['decide', 'choose', 'select', 'determine']):
                patterns['decisions'].append({
                    'sentence_index': i,
                    'decision': self._extract_decision_text(sentence),
                    'options': self._extract_decision_options(sentence),
                    'original': sentence
                })
        
        # Enhanced conditional detection for simple sentences
        sentences = structure['sentences']
        for i, sentence in enumerate(sentences):
            sent_lower = sentence.lower()
            
            # Check for very simple if/else structure not captured by keywords
            if sent_lower.startswith('if ') and ('otherwise' in sent_lower or 'else' in sent_lower):
                parts = re.split(r'otherwise|else', sent_lower, maxsplit=1)
                if len(parts) == 2:
                    if_part = parts[0].replace('if', '', 1).strip()
                    else_part = parts[1].strip()
                    
                    # Split the if part into condition and then-action
                    if ',' in if_part:
                        condition, then_action = if_part.split(',', 1)
                        patterns['conditionals'].append({
                            'sentence_index': i,
                            'condition': condition.strip(),
                            'then_action': then_action.strip(),
                            'else_action': else_part,
                            'original': sentence
                        })
        
        logger.info(f"🔍 Identified patterns: {len(patterns['conditionals'])} conditionals, {len(patterns['sequences'])} sequences, {len(patterns['decisions'])} decisions")
        return patterns

    def _extract_if_then_pattern(self, sentence: str) -> Optional[Dict[str, str]]:
        """Extract IF-THEN-ELSE pattern from a sentence"""
        
        patterns = [
            # Your existing patterns
            r'if\s+(.*?)\s+then\s+(.*?)(?:\s+(?:else|otherwise)\s+(.*?))?(?:\.|$)',
            r'when\s+(.*?),?\s*(.*?)(?:\s+(?:else|otherwise)\s+(.*?))?(?:\.|$)',
            r'should\s+(.*?),?\s*(.*?)(?:\s+(?:if not|unless)\s+(.*?))?(?:\.|$)',
            
            # Add this simple pattern that will match your specific example
            r'if\s+(.*?),\s+(.*?)\.?\s*(?:otherwise|else)[,\s]+(.*?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, sentence.lower(), re.IGNORECASE)
            if match:
                result = {
                    'condition': match.group(1).strip(),
                    'then_action': match.group(2).strip()
                }
                
                # Handle else action if present
                if len(match.groups()) >= 3 and match.group(3):
                    result['else_action'] = match.group(3).strip()
                
                # Log successful pattern match
                logger.info(f"✅ Extracted condition: '{result['condition']}', then: '{result['then_action']}', else: '{result.get('else_action', 'None')}'")
                return result
        
        logger.warning(f"❌ No conditional pattern found in: '{sentence}'")
        return None

    def _extract_sequential_actions(self, sentence: str) -> List[str]:
        """Extract sequential actions from a sentence"""
        
        # Split on common sequence separators
        separators = ['and then', 'then', 'next', 'after that', 'subsequently', 'and']
        
        actions = [sentence]
        for sep in separators:
            new_actions = []
            for action in actions:
                new_actions.extend([part.strip() for part in action.split(sep) if part.strip()])
            actions = new_actions
        
        # Clean up actions
        cleaned_actions = []
        for action in actions:
            action = re.sub(r'^(and\s+|then\s+|next\s+)', '', action.strip())
            if action and len(action) > 3:
                cleaned_actions.append(action)
        
        return cleaned_actions[:6]  # Limit to prevent overly complex diagrams

    def _identify_sequence_type(self, sentence: str) -> str:
        """Identify the type of sequence (linear, parallel, conditional)"""
        
        sent_lower = sentence.lower()
        
        if any(word in sent_lower for word in ['simultaneously', 'parallel', 'at the same time', 'concurrently']):
            return 'parallel'
        elif any(word in sent_lower for word in ['if', 'when', 'should', 'depending']):
            return 'conditional'
        else:
            return 'linear'

    def _extract_decision_text(self, sentence: str) -> str:
        """Extract decision text from a sentence"""
        
        # Remove question marks and clean up
        decision = sentence.replace('?', '').strip()
        
        # Extract the core decision
        if 'whether' in decision.lower():
            match = re.search(r'whether\s+(.*)', decision.lower())
            if match:
                decision = match.group(1).strip()
        
        return decision[:80]  # Limit length for diagram readability

    def _extract_decision_options(self, sentence: str) -> List[str]:
        """Extract decision options from a sentence"""
        
        # Look for explicit options
        options = []
        
        # Check for "or" patterns
        if ' or ' in sentence.lower():
            parts = sentence.split(' or ')
            options = [part.strip() for part in parts if part.strip()]
        
        # Default yes/no for questions
        if '?' in sentence and not options:
            options = ['Yes', 'No']
        
        return options[:4]  # Limit options for diagram clarity

    def _extract_process_steps(self, text: str) -> List[Dict[str, str]]:
        """Extract sequential process steps from text"""
        
        steps = []
        
        # Split into sentences
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        for i, sentence in enumerate(sentences):
            # Check for "When X, Y" pattern
            when_match = re.search(r'when\s+(.*?),\s+(.*)', sentence, re.IGNORECASE)
            if when_match:
                steps.append({
                    'type': 'event',
                    'trigger': when_match.group(1).strip(),
                    'action': when_match.group(2).strip()
                })
                continue
            
            # Check for "If X, Y; else Z" pattern
            if_match = re.search(r'if\s+(.*?),\s+(.*?)(?:;|$)\s*(?:else|otherwise),?\s*(.*?)(?:;|$)', 
                                sentence, re.IGNORECASE)
            if if_match:
                steps.append({
                    'type': 'condition',
                    'condition': if_match.group(1).strip(),
                    'then_action': if_match.group(2).strip(),
                    'else_action': if_match.group(3).strip() if if_match.group(3) else None
                })
                continue
        
        return steps

    def _extract_sequential_actions_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract sequences of actions from text using NLP and regex patterns"""
        if not self.nlp:
            return []
        
        sequential_actions = []
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # First extract sentence-level actions
        for sent_idx, sent in enumerate(doc.sents):
            # Skip sentences that are clearly conditional
            if any(keyword in sent.text.lower() for keyword in ['if ', 'when ', 'should ']):
                continue
                
            sent_text = sent.text.strip()
            
            # Add explicit pattern for "verb[s] noun" before commas
            comma_actions = re.findall(r'(\w+s(?:es)?\s+[^,;.]+)(?:,|;|and\s+)', sent_text, re.IGNORECASE)
            for action in comma_actions:
                if action.strip() and len(action.strip()) > 3:
                    sequential_actions.append({
                        'action': action.strip(),
                        'sentence_idx': sent_idx,
                        'source': 'comma_pattern'
                    })
            
            # Look for specific verb+object pairs using spaCy
            for token in sent:
                if token.pos_ == 'VERB' and not token.is_stop:
                    # Find direct objects of this verb
                    obj_text = ""
                    for child in token.children:
                        if child.dep_ in ['dobj', 'pobj']:
                            obj_text = child.text
                            # Include any adjectives modifying the object
                            for grandchild in child.children:
                                if grandchild.dep_ == 'amod':
                                    obj_text = f"{grandchild.text} {obj_text}"
                            break
                    
                    if obj_text:
                        action = f"{token.text} {obj_text}"
                        # Avoid duplicates
                        if not any(a['action'].lower() == action.lower() for a in sequential_actions):
                            sequential_actions.append({
                                'action': action,
                                'sentence_idx': sent_idx,
                                'source': 'spacy_verb_obj'
                            })
        
        return sequential_actions

    def _create_dynamic_flowchart(self, text: str, structure: Dict = None, patterns: Dict = None, sequential_actions: List = None) -> Dict[str, Any]:
        """Create flowchart with guaranteed sequence handling"""
        
        logger.info(f"🧠 Creating dynamic flowchart from text analysis...")
        
        # Use provided structure/patterns or create them if not provided
        if structure is None:
            structure = self._extract_sentence_structure(text)
        
        if patterns is None:
            patterns = self._identify_process_patterns(text, structure)
        
        # Build flowchart dynamically
        nodes = []
        edges = []
        
        # Create start node
        start_node = self._create_node('start', "Start", node_type='input')
        nodes.append(start_node)
        
        current_node_id = 'start'
        y_position = 150
        
        # CRITICAL FIX: Always check structure sequences first, then fall back to sequential_actions
        sequence_actions = []
        if structure.get('sequences') and structure['sequences'][0].get('actions'):
            sequence_actions = structure['sequences'][0]['actions']
        elif sequential_actions:
            sequence_actions = [a['action'] for a in sequential_actions]
        
        # Log that we're actually processing sequences
        logger.info(f"🔄 Processing {len(sequence_actions)} sequential actions in flowchart creation")
        
        # Process sequential actions first from structure.sequences
        if sequence_actions:
            logger.info(f"Processing {len(sequence_actions)} sequential actions")
            
            for i, action_text in enumerate(sequence_actions):
                action_id = f"action_{i+1}"
                
                # Capitalize first letter for better presentation
                if action_text and action_text[0].islower():
                    action_text = action_text[0].upper() + action_text[1:]
                
                action_node = self._create_node(
                    action_id,
                    action_text,
                    position={'x': 400, 'y': y_position}
                )
                nodes.append(action_node)
                
                # Connect to previous node
                edges.append(self._create_edge(current_node_id, action_id))
                
                # Update for next iteration
                current_node_id = action_id
                y_position += 100
    
        # Step 4: Process conditionals (existing logic)
        for i, conditional in enumerate(patterns.get('conditionals', [])):
            decision_id = f"decision_{i+1}"
            success_id = f"success_{i+1}"
            failure_id = f"failure_{i+1}"
            
            # Create decision node with better formatting
            condition_text = conditional['condition'].strip()
            if not condition_text.endswith('?'):
                condition_text += '?'
                
            decision_node = self._create_node(
                decision_id,
                f"Is {condition_text}",
                node_type='decision',
                position={'x': 400, 'y': y_position}
            )
            nodes.append(decision_node)
            
            # Create success path with better text formatting
            then_action = conditional['then_action'].strip()
            if then_action and then_action[0].islower():
                then_action = then_action[0].upper() + then_action[1:]
                
            success_node = self._create_node(
                success_id,
                then_action,
                position={'x': 200, 'y': y_position + 150}
            )
            nodes.append(success_node)
            
            # Connect previous node to the decision
            edges.append(self._create_edge(current_node_id, decision_id))
            
            # Connect decision to success path
            edges.append(self._create_edge(decision_id, success_id, label="YES"))
            
            # Create failure path if exists
            if conditional.get('else_action'):
                else_action = conditional['else_action'].strip()
                if else_action and else_action[0].islower():
                    else_action = else_action[0].upper() + else_action[1:]
                    
                failure_node = self._create_node(
                    failure_id,
                    else_action,
                    position={'x': 600, 'y': y_position + 150}
                )
                nodes.append(failure_node)
                
                # Add failure edge
                edges.append(self._create_edge(decision_id, failure_id, label="NO"))
                
                # Both paths continue to next step or end
                if i == len(patterns.get('conditionals', [])) - 1:
                    # If last conditional, connect both branches to end
                    edges.append(self._create_edge(success_id, 'end'))
                    edges.append(self._create_edge(failure_id, 'end')) 
                    # Don't update current_node_id as we're already connected to end
                else:
                    # Find a merge point - both branches connect to a new node
                    merge_id = f"merge_{i+1}"
                    merge_node = self._create_node(
                        merge_id,
                        "Continue",
                        position={'x': 400, 'y': y_position + 300}
                    )
                    nodes.append(merge_node)
                    edges.append(self._create_edge(success_id, merge_id))
                    edges.append(self._create_edge(failure_id, merge_id))
                    current_node_id = merge_id
            else:
                # No else path, just continue from the success path
                current_node_id = success_id
                
            y_position += 300
        
        # Add end node dynamically
        end_node = self._create_node(
            'end',
            "End",
            node_type='output',
            position={'x': 400, 'y': y_position}
        )
        nodes.append(end_node)
        
        # Connect the last node to the end if not already connected
        if not any(edge['target'] == 'end' for edge in edges):
            edges.append(self._create_edge(current_node_id, 'end'))
        
        logger.info(f"✅ Created dynamic flowchart with {len(nodes)} nodes and {len(edges)} edges")
        return {'nodes': nodes, 'edges': edges}

    def _create_node(self, node_id: str, label: str, node_type: str = 'default', position: Dict[str, int] = None) -> Dict[str, Any]:
        """Create a node with dynamic properties"""
        
        if position is None:
            position = {'x': 400, 'y': self.node_counter * 100 + 50}
        
        node = {
            'id': node_id,
            'data': {'label': label},
            'position': position
        }
        
        if node_type in ['input', 'output']:
            node['type'] = node_type
        
        self.node_counter += 1
        return node

    def _create_edge(self, source: str, target: str, label: str = None) -> Dict[str, Any]:
        """Create an edge with optional label"""
        
        edge = {
            'id': f"e_{self.edge_counter}",
            'source': source,
            'target': target
        }
        
        if label:
            edge['label'] = label
        
        self.edge_counter += 1
        return edge

    def _fallback_structure_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback structure extraction when spaCy is not available"""
        
        sentences = text.split('.')
        words = text.lower().split()
        
        return {
            'subjects': [w for w in words if w in ['user', 'customer', 'system', 'process', 'order']],
            'verbs': [w for w in words if w in ['process', 'validate', 'send', 'update', 'create', 'check']],
            'objects': [w for w in words if w in ['order', 'payment', 'email', 'data', 'information']],
            'sentences': [s.strip() for s in sentences if s.strip()],
            'entities': []
        }

    def _sanitize_node_id(self, node_id: str) -> str:
        """Sanitize node IDs to avoid Mermaid reserved keywords"""
        # List of Mermaid reserved keywords
        reserved_keywords = ['end', 'graph', 'subgraph', 'class', 'click', 'style', 'linkStyle']
        
        # If node_id is a reserved keyword, append "_node" to it
        if node_id.lower() in reserved_keywords:
            logger.warning(f"⚠️ Found reserved Mermaid keyword '{node_id}' as node ID, renaming to '{node_id}_node'")
            return f"{node_id}_node"
        return node_id

    def convert_to_mermaid(self, flowchart_data: Dict[str, Any]) -> str:
        """Convert to Mermaid with guaranteed correct syntax and better label handling"""
        try:
            # Start with proper graph declaration
            mermaid_parts = ["graph TD"]
            
            # Process all nodes with explicit newlines
            for node in flowchart_data.get('nodes', []):
                # Sanitize the node ID to avoid reserved keywords
                original_id = node['id']
                node_id = self._sanitize_node_id(original_id)
                
                label = node['data']['label']
                
                # Clean label thoroughly
                clean_label = str(label).replace('\n', ' ').replace('"', "'").strip()
                clean_label = re.sub(r'[^\w\s.,;:!?()\'"-]', '', clean_label)
                
                if not clean_label:
                    clean_label = f"Node_{node_id}"
                # Allow up to 40 characters for better readability (increased from original)
                elif len(clean_label) > 40:
                    clean_label = clean_label[:37] + "..."
                
                # Generate node with proper syntax - each node on its own line
                if node.get('type') == 'input' or 'start' in original_id.lower():
                    mermaid_parts.append(f"    {node_id}[\"{clean_label}\"]")
                elif node.get('type') == 'output' or 'end' in original_id.lower():
                    mermaid_parts.append(f"    {node_id}[\"{clean_label}\"]")
                elif 'decision' in original_id.lower() or node.get('type') == 'decision':
                    mermaid_parts.append(f"    {node_id}{{\"{clean_label}\"}}")
                else:
                    mermaid_parts.append(f"    {node_id}[\"{clean_label}\"]")
            
            # Store node ID mapping for edges
            id_mapping = {node['id']: self._sanitize_node_id(node['id']) 
                        for node in flowchart_data.get('nodes', [])}
            
            # Add blank line for clarity
            mermaid_parts.append("")
            
            # Process all edges with proper ID references
            for edge in flowchart_data.get('edges', []):
                source = id_mapping.get(edge['source'], edge['source'])
                target = id_mapping.get(edge['target'], edge['target'])
                
                # Skip edges with None as source or target
                if source is None or target is None or source == "None" or target == "None":
                    continue
                    
                label = edge.get('label', '')
                
                if label and label.strip():
                    clean_edge_label = str(label).replace('"', "'").strip()
                    mermaid_parts.append(f"    {source} -->|{clean_edge_label}| {target}")
                else:
                    mermaid_parts.append(f"    {source} --> {target}")
            
            # Add styling with proper spacing
            mermaid_parts.append("")
            mermaid_parts.append("    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px")
            mermaid_parts.append("    classDef startEnd fill:#e8f5e8,stroke:#4caf50,stroke-width:2px")
            
            # Join with explicit newlines
            mermaid_code = "\n".join(mermaid_parts)
            
            logger.info(f"✅ Generated Mermaid code with {len(mermaid_parts)} lines")
            return mermaid_code
        
        except Exception as e:
            logger.error(f"❌ Error in Mermaid conversion: {str(e)}")
            return """graph TD
    start["Start"] --> process["Process"]
    process --> finish["End"]
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px"""

    def convert_text_to_flowchart(self, text_input: str) -> Dict[str, Any]:
        """Single-pass, unit-based conversion with improved condition and structure handling"""
        import re
        logger.info(f"🚀 ENHANCED CONVERSION: {len(text_input)} chars")
        self.node_counter = 0
        self.edge_counter = 0

        def format_condition(cond):
            """Better format conditions without duplicating 'If' prefixes"""
            cond = cond.strip()
            # Remove 'if' from the beginning if present
            if cond.lower().startswith("if "):
                cond = cond[3:].strip()
            
            # Check if condition already has a verb
            has_verb = any(verb in cond.lower().split() for verb in 
                          ["is", "are", "was", "were", "has", "have", "can", "should", "would", "do", "does"])
            
            if not has_verb:
                return f"Are {cond}?"
            
            # Add question mark if missing
            return cond if cond.endswith("?") else f"{cond}?"

        def clean_action_text(text):
            """Clean and format action text for better readability"""
            if not text:
                return "Process"
                
            # Remove list markers (1., 2., etc)
            text = re.sub(r'^\s*\d+\.\s*', '', text.strip())
            
            # Remove leading "if" if present
            if text.lower().startswith("if "):
                parts = text.split(",", 1)
                if len(parts) > 1:
                    text = parts[1].strip()
                    
            # Capitalize first letter
            if text and text[0].islower():
                text = text[0].upper() + text[1:]
                
            # Truncate long text
            if len(text) > 40:
                text = text[:37] + "..."
                
            return text

        def make_node_id(prefix):
            self.node_counter += 1
            return f"{prefix}{self.node_counter}"

        def make_node(node_id, label, node_type=None, position=None):
            node = {'id': node_id, 'data': {'label': label}}
            if node_type:
                node['type'] = node_type
            if position:
                node['position'] = position
            return node

        def extract_if_else(unit):
            """Improved conditional extraction with better grammar handling"""
            # Check for "If not" alternative pattern first (related to previous condition)
            if_not_match = re.search(r'if\s+not\s*[,.]?\s*(.*?)(?:$|\.)', unit, re.IGNORECASE)
            if if_not_match:
                # This is an "if not" condition that relates to a previous condition
                return "not", if_not_match.group(1).strip(), ""
                
            # Match if X, Y pattern with flexible grammar
            if_match = re.search(r'if\s+(.*?)[,:]?\s*(.*?)(?:$|\.)', unit, re.IGNORECASE)
            if if_match:
                return if_match.group(1).strip(), if_match.group(2).strip(), ""
                
            # Complex pattern with explicit else
            complex_match = re.search(r'if\s+(.*?)[,:]?\s*(.*?)\s*(?:otherwise|else)[,\s]+(.*?)(?:\.|$)', 
                                     unit, re.IGNORECASE)
            if complex_match:
                return complex_match.group(1).strip(), complex_match.group(2).strip(), complex_match.group(3).strip()
                
            # Use existing pattern matcher as fallback
            if hasattr(self, '_extract_if_then_pattern'):
                cond_match = self._extract_if_then_pattern(unit)
                if cond_match:
                    return cond_match['condition'], cond_match['then_action'], cond_match.get('else_action', '')
                    
            return unit, '', ''

        def split_into_units(text):
            """Split text into logical units with improved handling of numbered lists and related clauses"""
            # First, normalize and remove numbered list markers
            text = re.sub(r'\s*\d+\.\s*', ' ', text)
            
            # Merge sentences with "if not" or "otherwise" with previous sentence
            sentences = []
            current = ""
            
            for sent in re.split(r'(?<=[.!?])\s+', text.strip()):
                sent = sent.strip()
                if not sent:
                    continue
                    
                # Check if this sentence continues from previous (alternatives, elaborations)
                if re.match(r'^(?:otherwise|else|if\s+not)\b', sent, re.IGNORECASE) and current:
                    current += " " + sent
                else:
                    # Store previous complete unit if exists
                    if current:
                        sentences.append(current)
                    current = sent
                    
            # Don't forget the last unit
            if current:
                sentences.append(current)
                
            # Group related sentences into logical units
            units = []
            i = 0
            while i < len(sentences):
                unit = sentences[i]
                
                # Check if next sentence is closely related (e.g., describes an alternative)
                if i + 1 < len(sentences):
                    next_sent = sentences[i+1]
                    # If next sentence starts with related keywords or is short
                    if (re.match(r'^(?:otherwise|else|if\s+not|however|but|when)\b', next_sent, re.IGNORECASE) or
                        len(next_sent.split()) <= 5):
                        unit += " " + next_sent
                        i += 1
                
                units.append(unit)
                i += 1
                
            return units

        def extract_sequential_actions(unit):
            """Extract sequential actions with improved verb-object recognition"""
            # Use spaCy if available, fallback to regex
            actions = []
            
            # Skip extraction if this is clearly a conditional
            if unit.lower().startswith("if "):
                return []
                
            if self.nlp:
                doc = self.nlp(unit)
                for sent in doc.sents:
                    # Skip conditionals within the sentence
                    if any(k in sent.text.lower() for k in ['if ', 'when ', 'else ', 'otherwise ']):
                        continue
                        
                    # Extract meaningful verb-object pairs using spaCy
                    for token in sent:
                        if token.pos_ == "VERB" and not token.is_stop:
                            obj = ""
                            for child in token.children:
                                if child.dep_ in ['dobj', 'pobj']:
                                    obj = child.text
                                    # Get any modifiers
                                    modifiers = []
                                    for grandchild in child.children:
                                        if grandchild.dep_ in ['amod', 'compound']:
                                            modifiers.append(grandchild.text)
                                    if modifiers:
                                        obj = f"{' '.join(modifiers)} {obj}"
                                    break
                                    
                            if obj:
                                action = f"{token.lemma_} {obj}".strip()
                                if not any(a.lower() == action.lower() for a in actions):
                                    actions.append(action)
                                
            # Enhanced regex fallback for verb-noun patterns
            if not actions:
                # Look for common action patterns
                action_patterns = [
                    r'\b(open|log\sin|enter|input|check|verify|display|show|redirect|grant|access|process)\s+[a-z\s]{3,30}\b',
                    r'\b(sends?|updates?|creates?|prompts?|displays?|redirects?)\s+[a-z\s]{3,30}\b'
                ]
                
                for pattern in action_patterns:
                    matches = re.findall(pattern, unit, re.IGNORECASE)
                    for match in matches:
                        full_match = re.search(f"{match}\\s+[a-z\\s]{{3,30}}\\b", unit, re.IGNORECASE)
                        if full_match:
                            actions.append(clean_action_text(full_match.group(0)))
                
                # Split by sentence boundaries and sequences if still no actions
                if not actions:
                    parts = re.split(r',|\sand\s|\sthen\s', unit)
                    meaningful_parts = []
                    for part in parts:
                        part = clean_action_text(part)
                        if len(part) > 10 and not part.lower().startswith("if "):
                            meaningful_parts.append(part)
                            
                    actions = meaningful_parts
                    
            return actions

        # --- Main conversion pipeline ---
        # Remove numbered list markers and clean the input
        text_input = re.sub(r'^\s*\d+\.\s*', '', text_input.strip())
        
        # Split text into logical units
        units = split_into_units(text_input)
        
        # Initialize flowchart components
        nodes, edges = [], []
        nodes.append(make_node("start", "Start", node_type='input'))
        prev = "start"
        last_decision = None
        branch_ends = []
        pending_connections = []
        
        # Process each unit of text
        for i, unit in enumerate(units):
            # Special handling for "If not" continuations
            is_continuation = False
            if unit.lower().startswith("if not") or unit.lower().startswith("otherwise"):
                if last_decision:
                    is_continuation = True
                    
            if is_continuation and last_decision:
                # This is a continuation of previous decision
                action_id = make_node_id("else")
                action_text = re.sub(r'^(?:if\s+not|otherwise)[,\s]+', '', unit, flags=re.IGNORECASE)
                action_text = clean_action_text(action_text)
                
                action_node = make_node(action_id, action_text)
                nodes.append(action_node)
                
                # Connect from last decision's "No" path
                edges.append((last_decision, action_id, "No"))
                branch_ends.append(action_id)
                
            # Regular conditional pattern
            elif unit.lower().startswith("if ") and not unit.lower().startswith("if not"):
                cond, then_act, else_act = extract_if_else(unit)
                
                # Create decision node with properly formatted condition
                decision_id = make_node_id("decision")
                decision_node = make_node(
                    decision_id, 
                    format_condition(cond),
                    node_type='decision'
                )
                nodes.append(decision_node)
                
                # Create success path node
                then_id = make_node_id("then")
                then_node = make_node(then_id, clean_action_text(then_act))
                nodes.append(then_node)
                
                # Connect from previous to decision
                if prev:
                    edges.append((prev, decision_id, None))
                    
                # Connect decision to success path
                edges.append((decision_id, then_id, "Yes"))
                
                # Create and connect else path if provided
                if else_act:
                    else_id = make_node_id("else")
                    else_node = make_node(else_id, clean_action_text(else_act))
                    nodes.append(else_node)
                    edges.append((decision_id, else_id, "No"))
                    branch_ends.append(else_id)
                else:
                    # Remember this decision to connect an else path later
                    last_decision = decision_id
                    
                # Update branches and previous pointer
                branch_ends.append(then_id)
                prev = None  # Reset prev since we're now tracking branch ends
                
            # Sequential steps
            else:
                actions = extract_sequential_actions(unit)
                
                # Handle extracted actions
                for act in actions:
                    step_id = make_node_id("step")
                    nodes.append(make_node(step_id, clean_action_text(act)))
                    
                    if prev:
                        edges.append((prev, step_id, None))
                    prev = step_id
                    
                # If this unit comes after a branch, connect all branch ends to this step
                if branch_ends and not prev and actions:
                    first_step = nodes[-len(actions)]['id']
                    for branch_end in branch_ends:
                        edges.append((branch_end, first_step, None))
                    branch_ends = []
                    prev = nodes[-1]['id']  # Last added step is new prev
    
        # Add end node
        end_id = "end"
        nodes.append(make_node(end_id, "End", node_type='output'))
        
        # Connect any hanging nodes to end
        endings_connected = False
        if branch_ends:
            for branch_end in branch_ends:
                edges.append((branch_end, end_id, None))
            endings_connected = True
            
        # If there's a prev node that hasn't been connected yet
        if prev:
            edges.append((prev, end_id, None))
            endings_connected = True
            
        # Connect the last decision's "No" path to end if not connected elsewhere
        if last_decision and not endings_connected:
            # Check if last_decision already has a "No" path
            if not any(edge[0] == last_decision and edge[2] == "No" for edge in edges):
                edges.append((last_decision, end_id, "No"))
        
        # Generate mermaid code
        mermaid = render_mermaid(nodes, edges)
        
        return {
            "mermaid": mermaid,
            "nodes": nodes,
            "edges": edges
        }

    def render_mermaid(nodes, edges):
        """Generate improved Mermaid diagram code with proper node types and connections"""
        mermaid_lines = ["graph TD"]
        
        # Process nodes with better formatting
        for node in nodes:
            nid = node['id']
            label = node['data']['label']
            
            # If node ID is 'end', rename it to avoid Mermaid reserved word conflicts
            if nid == 'end':
                nid = 'endNode'
            
            # Clean the label for better display
            clean_label = str(label).replace('"', "'").replace('\n', ' ').strip()
            clean_label = clean_label.strip("'").strip('"')
            
            # Remove "Is If" pattern if present
            clean_label = clean_label.replace("Is If ", "Is ")
            
            # Add each node definition with proper formatting
            if node.get('type') == 'decision' or 'decision' in nid:
                mermaid_lines.append(f'    {nid}{{"{clean_label}"}}')
            else:
                mermaid_lines.append(f'    {nid}["{clean_label}"]')
        
        # Process edges with proper connections
        for src, tgt, lbl in edges:
            # Skip invalid edges
            if src is None or tgt is None or src == "None" or tgt == "None":
                continue
            
            # Replace 'end' with 'endNode' in edges too
            if src == 'end':
                src = 'endNode'
            if tgt == 'end':
                tgt = 'endNode'
            
            if lbl:
                mermaid_lines.append(f"    {src} -->|{lbl}| {tgt}")
            else:
                mermaid_lines.append(f"    {src} --> {tgt}")
        
        # Add styling section
        mermaid_lines.append("")
        mermaid_lines.append("    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px")
        mermaid_lines.append("    classDef startEnd fill:#e8f5e8,stroke:#4caf50,stroke-width:2px")
        
        # Style both start and end nodes
        mermaid_lines.append("    class start,endNode startEnd")
        
        # Join with explicit newlines
        return "\n".join(mermaid_lines)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the conversion process
        
        Returns:
            Dict[str, Any]: Statistics about the conversion
        """
        return {
            "nodes_created": self.node_counter,
            "error_occurred": self.error_occurred,
            "error_message": self.last_error if self.error_occurred else None
        }

# Factory function to create instance
def create_flowchart_converter():
    """Create and return an enhanced flowchart converter instance"""
    return EnhancedFlowchartConverter()

# Create a backward-compatible alias for DynamicFlowchartConverter
class DynamicFlowchartConverter(EnhancedFlowchartConverter):
    """
    Backward compatibility class for existing code that expects DynamicFlowchartConverter
    This class inherits all functionality from EnhancedFlowchartConverter
    """
    def __init__(self):
        super().__init__()
        logger.info("✅ DynamicFlowchartConverter initialized (alias for EnhancedFlowchartConverter)")

def render_mermaid_simple(nodes, edges):
    """Generate a simpler, more compatible Mermaid diagram."""
    mermaid_lines = ["graph TD"]
    
    # Use simple node IDs to avoid conflicts
    id_map = {}
    for i, node in enumerate(nodes):
        simple_id = f"n{i}" 
        id_map[node['id']] = simple_id
        label = node['data']['label']
        clean_label = str(label).replace('"', "'").replace('\n', ' ').strip()
        
        if node.get('type') == 'decision' or 'decision' in node['id']:
            mermaid_lines.append(f'    {simple_id}{{"{clean_label}"}}')
        else:
            mermaid_lines.append(f'    {simple_id}["{clean_label}"]')
    
    # Simple edges
    for src, tgt, lbl in edges:
        if src is None or tgt is None or src == "None" or tgt == "None":
            continue
            
        src_id = id_map.get(src, src)
        tgt_id = id_map.get(tgt, tgt)
        
        if lbl:
            mermaid_lines.append(f"    {src_id} -->|{lbl}| {tgt_id}")
        else:
            mermaid_lines.append(f"    {src_id} --> {tgt_id}")
    
    return "\n".join(mermaid_lines)

def format_condition(cond):
    cond = cond.strip()
    has_verb = any(verb in cond.lower().split() for verb in ["is", "are", "was", "were", "has", "have"])
    if not has_verb:
        return f"Is {cond}?"
    # Add question mark if missing
    return cond if cond.endswith("?") else f"{cond}?"
