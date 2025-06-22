from fixed_pattern_matching_converter import fixed_mermaid_generator

# Test with your exact problematic input
test_input = "E-commerce order processing system where customer places order if payment method validation successful and inventory stock level sufficient then process order payment and generate shipping label if payment validation fails or inventory stock unavailable then send customer notification email with alternative options and hold order for manual review"

print(f"\n🧪 TESTING E-COMMERCE INPUT:")
print(f"Input: {test_input}")

result = fixed_mermaid_generator(test_input)

print(f"\n🔧 FIXED OUTPUT:")
print(f"{result}")

# Validate the fix
expected_elements = [
    'graph TD',
    'A[',
    'B{',
    '-->',
    '|Yes|',
    '|No|',
    'C[',
    'D['
]

print(f"\n✅ VALIDATION:")
for element in expected_elements:
    present = element in result
    print(f"   {element}: {'✅' if present else '❌'}")

# Check if it's a proper decision flowchart (not simple)
is_decision = '{' in result and '|Yes|' in result and '|No|' in result
print(f"\n🎯 DECISION FLOWCHART: {'✅ YES' if is_decision else '❌ NO - STILL SIMPLE'}")

# Additional test cases
additional_tests = [
    "payment processing if successful confirm if failed retry",
    "user login if valid allow if invalid deny",
    "data validation if correct save if wrong show error"
]

print(f"\n🧪 ADDITIONAL TESTS:")
for i, test in enumerate(additional_tests, 1):
    result = fixed_mermaid_generator(test)
    is_decision = '{' in result and '|Yes|' in result
    print(f"{i}. {test}")
    print(f"   Result: {'✅ DECISION' if is_decision else '❌ SIMPLE'}")