# backend/scripts/evaluate_flowchart.py
"""
Script to evaluate the accuracy of the flowchart converter
"""
import os
import sys
import json
from datetime import datetime

# Get the absolute path to the backend directory
backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(f"Backend directory: {backend_dir}")

# Add backend directory to Python path
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    print(f"Added {backend_dir} to Python path")

try:
    # Try importing with the full path
    from app.utils.evaluator import FlowchartEvaluator
    print("Successfully imported FlowchartEvaluator")
except ImportError as e:
    print(f"ERROR: Could not import FlowchartEvaluator: {e}")
    print("\nDebugging information:")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Check if the files exist
    utils_init = os.path.join(backend_dir, 'app', 'utils', '__init__.py')
    evaluator_path = os.path.join(backend_dir, 'app', 'utils', 'evaluator.py')
    
    print(f"\nChecking file existence:")
    print(f"app/__init__.py exists: {os.path.exists(os.path.join(backend_dir, 'app', '__init__.py'))}")
    print(f"app/utils/__init__.py exists: {os.path.exists(utils_init)}")
    print(f"app/utils/evaluator.py exists: {os.path.exists(evaluator_path)}")
    
    sys.exit(1)

def main():
    print("\n===== FLOWCHART CONVERTER ACCURACY EVALUATION =====")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create evaluator
    evaluator = FlowchartEvaluator()
    
    # Evaluate accuracy
    accuracy, metrics = evaluator.evaluate_accuracy(verbose=True)
    
    print("\n===== SUMMARY =====")
    print(f"Overall Accuracy: {accuracy}%")
    
    # Save results
    results_dir = os.path.join(backend_dir, 'data', 'evaluation')
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f"accuracy_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(results_file, 'w') as f:
        json.dump({
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "accuracy": accuracy,
            "metrics": metrics
        }, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    
    # Suggest improvements if accuracy is below target
    if accuracy < 90:
        print("\n===== IMPROVEMENT SUGGESTIONS =====")
        print("To improve accuracy:")
        print("1. Add more test cases with diverse patterns")
        print("2. Enhance pattern recognition for failing cases")
        print("3. Improve condition extraction for complex scenarios")
        print("4. Add support for additional flowchart patterns")
    else:
        print("\n✅ Target accuracy of 90%+ achieved!")

if __name__ == "__main__":
    main()