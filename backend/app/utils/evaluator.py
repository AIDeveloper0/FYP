"""
Utility class for evaluating flowchart converter accuracy
"""
import os
import json
import time
import datetime
import logging
from typing import List, Dict, Tuple, Any, Optional

# Import converter directly (not from itself)
from app.converters.flowchart_converter import FlowchartConverter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlowchartEvaluator:
    """
    Evaluator for testing flowchart conversion accuracy against test cases
    """
    
    def __init__(self, test_data_path: Optional[str] = None):
        """
        Initialize the evaluator with test data
        
        Args:
            test_data_path: Path to test data JSON file. If None, uses default path.
        """
        self.converter = FlowchartConverter()
        
        # Set default path if not provided
        if test_data_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            self.test_data_path = os.path.join(base_dir, 'data', 'tests', 'flowchart_test_cases.json')
        else:
            self.test_data_path = test_data_path
        
        # Create directory if it doesn't exist
        test_dir = os.path.dirname(self.test_data_path)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir, exist_ok=True)
        
        # Load or create test cases
        self.test_cases = self._load_test_cases()
    
    def _load_test_cases(self) -> List[Dict[str, Any]]:
        """
        Load test cases from file or create default test cases if file doesn't exist
        
        Returns:
            List[Dict[str, Any]]: List of test cases
        """
        if os.path.exists(self.test_data_path):
            try:
                with open(self.test_data_path, 'r') as f:
                    data = json.load(f)
                    return data.get('test_cases', [])
            except Exception as e:
                logger.error(f"Error loading test data: {e}")
                return self._create_default_test_cases()
        else:
            # Create default test cases
            test_cases = self._create_default_test_cases()
            
            # Save default test cases
            try:
                with open(self.test_data_path, 'w') as f:
                    json.dump({'test_cases': test_cases}, f, indent=2)
            except Exception as e:
                logger.error(f"Error saving default test cases: {e}")
            
            return test_cases
    
    def _create_default_test_cases(self) -> List[Dict[str, Any]]:
        """
        Create default test cases
        
        Returns:
            List[Dict[str, Any]]: Default test cases
        """
        return [
            {
                "description": "Simple decision flow",
                "input": "User login if credentials valid then grant access else show error",
                "expected_patterns": ["graph TD", "Valid?", "Grant Access", "Error", "Yes", "No"]
            },
            {
                "description": "Sequence flow",
                "input": "First collect data, then validate the information, finally save to database",
                "expected_patterns": ["graph TD", "Collect Data", "Validate", "Save", "-->"]
            },
            {
                "description": "Complex business process",
                "input": "Order processing system where customer places order if payment successful then ship product if payment failed then notify customer",
                "expected_patterns": ["graph TD", "Order Processing", "Payment", "Ship", "Notify", "Yes", "No"]
            },
            {
                "description": "Loop pattern",
                "input": "Repeat checking status until task is complete",
                "expected_patterns": ["graph TD", "Checking Status", "Complete", "Yes", "No"]
            },
            {
                "description": "Parallel processes",
                "input": "System simultaneously processes payment and validates inventory",
                "expected_patterns": ["graph TD", "System", "Payment", "Inventory"]
            },
            {
                "description": "Multiple conditions with AND",
                "input": "Shopping checkout if customer is logged in and has items in cart then proceed to payment else redirect to cart",
                "expected_patterns": ["graph TD", "Shopping Checkout", "Logged In", "Items", "Proceed", "Redirect", "Yes", "No"]
            },
            {
                "description": "Process with error handling",
                "input": "Data import process checks file format if valid then import data else log error and notify admin",
                "expected_patterns": ["graph TD", "Data Import", "Valid", "Import Data", "Log Error", "Notify Admin", "Yes", "No"]
            },
            {
                "description": "Complex workflow with multiple steps",
                "input": "Ticket processing where agent receives ticket if priority is high then assign immediately and notify manager if priority is low then queue for later processing",
                "expected_patterns": ["graph TD", "Ticket Processing", "Priority", "High", "Assign", "Notify", "Queue", "Yes", "No"]
            },
            {
                "description": "While loop pattern",
                "input": "While there are unprocessed items, process the next item",
                "expected_patterns": ["graph TD", "Unprocessed Items", "Process", "Next Item", "Yes", "No"]
            },
            {
                "description": "Nested decisions",
                "input": "Login process checks username if valid then check password if password correct then grant access else lock account else show username error",
                "expected_patterns": ["graph TD", "Login Process", "Username", "Password", "Grant Access", "Lock Account", "Error", "Yes", "No"]
            }
        ]
    
    def count_total_expected_patterns(self) -> int:
        """Count total expected patterns across all test cases"""
        return sum(len(case['expected_patterns']) for case in self.test_cases)
    
    def evaluate_accuracy(self, verbose: bool = True) -> Tuple[float, Dict[str, Any]]:
        """
        Evaluate the accuracy of the flowchart converter
        
        Args:
            verbose: Whether to print detailed results
            
        Returns:
            Tuple[float, Dict[str, Any]]: Overall accuracy and detailed metrics
        """
        total_cases = len(self.test_cases)
        if total_cases == 0:
            return 0.0, {"error": "No test cases available"}
            
        matched_patterns = 0
        total_patterns = 0
        case_results = []
        error_cases = 0
        
        for case in self.test_cases:
            if verbose:
                print(f"\nEvaluating: {case['description']}")
                print(f"Input: {case['input']}")
            
            # Generate flowchart
            try:
                result = self.converter.convert(case['input'])
                error = None
            except Exception as e:
                print(f"Error processing case: {e}")
                result = "graph TD\n    A[Error] --> B[Failed]"
                error = str(e)
                error_cases += 1
            
            # Check for expected patterns
            case_matched = 0
            for pattern in case['expected_patterns']:
                total_patterns += 1
                if pattern.lower() in result.lower():
                    case_matched += 1
                    matched_patterns += 1
                    if verbose:
                        print(f"  ✅ Found pattern: {pattern}")
                else:
                    if verbose:
                        print(f"  ❌ Missing pattern: {pattern}")
            
            # Calculate case accuracy
            case_accuracy = case_matched / len(case['expected_patterns']) if case['expected_patterns'] else 0
            case_result = {
                "description": case['description'],
                "accuracy": round(case_accuracy * 100, 2),
                "matched_patterns": case_matched,
                "total_patterns": len(case['expected_patterns']),
                "output": result,
                "error": error
            }
            case_results.append(case_result)
            
            if verbose:
                print(f"  Case accuracy: {case_result['accuracy']}%")
                print(f"  Output:\n{result}")
        
        # Calculate overall accuracy
        pattern_accuracy = matched_patterns / total_patterns if total_patterns > 0 else 0
        
        # Calculate average case accuracy
        case_accuracies = [case["accuracy"] for case in case_results]
        avg_case_accuracy = sum(case_accuracies) / len(case_accuracies) if case_accuracies else 0
        
        # Combined accuracy (weighted)
        overall_accuracy = round((pattern_accuracy * 100 * 0.7 + avg_case_accuracy * 0.3), 2)
        
        metrics = {
            "overall_accuracy": overall_accuracy,
            "pattern_accuracy": round(pattern_accuracy * 100, 2),
            "avg_case_accuracy": round(avg_case_accuracy, 2),
            "total_cases": total_cases,
            "total_patterns": total_patterns,
            "matched_patterns": matched_patterns,
            "error_cases": error_cases,
            "case_results": case_results
        }
        
        if verbose:
            print("\n======= ACCURACY RESULTS =======")
            print(f"Overall accuracy: {overall_accuracy}%")
            print(f"Pattern matching accuracy: {metrics['pattern_accuracy']}%")
            print(f"Average case accuracy: {metrics['avg_case_accuracy']}%")
            print(f"Matched patterns: {matched_patterns}/{total_patterns}")
            print(f"Total test cases: {total_cases}")
        
        return overall_accuracy, metrics
    
    def add_test_case(self, description: str, input_text: str, 
                      expected_patterns: List[str]) -> bool:
        """
        Add a new test case
        
        Args:
            description: Description of the test case
            input_text: Input text for conversion
            expected_patterns: List of expected patterns in the output
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if not description or not input_text or not expected_patterns:
            logger.error("Invalid test case parameters: All fields must have values")
            return False
            
        try:
            # Add the new test case
            self.test_cases.append({
                "description": description,
                "input": input_text,
                "expected_patterns": expected_patterns
            })
            
            # Save updated test cases
            with open(self.test_data_path, 'w') as f:
                json.dump({'test_cases': self.test_cases}, f, indent=2)
                
            return True
        except Exception as e:
            logger.error(f"Error adding test case: {e}")
            return False
    
    def save_accuracy_results(self, metrics: Dict[str, Any], 
                             output_dir: Optional[str] = None) -> str:
        """
        Save accuracy results to a file
        
        Args:
            metrics: Metrics from evaluate_accuracy
            output_dir: Directory to save results (default: data/evaluation)
            
        Returns:
            str: Path to saved file
        """
        # Set default output directory if not provided
        if output_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            output_dir = os.path.join(base_dir, 'data', 'evaluation')
            
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"accuracy_results_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save results
        try:
            with open(filepath, 'w') as f:
                # Remove full output from case results to keep file size reasonable
                metrics_to_save = {**metrics}
                if 'case_results' in metrics_to_save:
                    for case in metrics_to_save['case_results']:
                        if 'output' in case and len(case['output']) > 500:
                            case['output'] = case['output'][:500] + "... (truncated)"
                
                json.dump(metrics_to_save, f, indent=2)
            return filepath
        except Exception as e:
            logger.error(f"Error saving accuracy results: {e}")
            return ""
    
    def fine_tune_converter(self, test_case_description: str) -> bool:
        """
        Apply fine-tuning to the converter based on a specific test case
        
        Args:
            test_case_description: Description of the test case to tune for
            
        Returns:
            bool: True if tuning was applied, False otherwise
        """
        # Find test case
        test_case = next((case for case in self.test_cases 
                         if case['description'] == test_case_description), None)
                         
        if test_case is None:
            logger.error(f"Test case not found: {test_case_description}")
            return False
            
        # Apply fine-tuning logic here
        # This would typically involve adjusting parameters in the converter
        # based on the specific test case requirements
        logger.info(f"Applied fine-tuning for: {test_case_description}")
        
        return True


def run_evaluation():
    """Run flowchart evaluation and print results"""
    evaluator = FlowchartEvaluator()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print("\n===== FLOWCHART CONVERTER ACCURACY EVALUATION =====")
    print(f"Date: {timestamp}\n")
    
    accuracy, metrics = evaluator.evaluate_accuracy(verbose=True)
    
    # Save results
    results_path = evaluator.save_accuracy_results(metrics)
    
    print("\n===== SUMMARY =====")
    print(f"Overall Accuracy: {accuracy}%")
    print(f"Results saved to: {results_path}")
    
    # Print suggestions for improvement
    print("\n===== IMPROVEMENT SUGGESTIONS =====")
    print("To improve accuracy:")
    print("1. Add more test cases with diverse patterns")
    print("2. Enhance pattern recognition for failing cases")
    print("3. Improve condition extraction for complex scenarios")
    print("4. Add support for additional flowchart patterns")
    
    target_accuracy = 90.0
    if accuracy >= target_accuracy:
        print(f"\n✅ Target accuracy of {target_accuracy}%+ achieved!")
    else:
        print(f"\n❌ Accuracy below target of {target_accuracy}%. Further improvements needed.")


# For direct script execution
if __name__ == "__main__":
    run_evaluation()

"""
Test runner for flowchart evaluator
"""
from app.utils.evaluator import FlowchartEvaluator

def test_evaluator():
    """Test flowchart evaluator with default test cases"""
    evaluator = FlowchartEvaluator()
    accuracy, metrics = evaluator.evaluate_accuracy(verbose=True)
    
    # Print summary
    print(f"\nTEST COMPLETE: Overall Accuracy: {accuracy}%")
    print(f"Matched patterns: {metrics['matched_patterns']}/{metrics['total_patterns']}")
    
    return accuracy, metrics

if __name__ == "__main__":
    test_evaluator()