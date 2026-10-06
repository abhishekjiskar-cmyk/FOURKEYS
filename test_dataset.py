"""
Test dataset for evaluating multi-agent system
"""

TEST_CASES = [
    # Medical Domain
    {
        "id": "med_001",
        "domain": "medical",
        "problem": "A 45-year-old patient presents with chest pain, shortness of breath, and sweating. Pain started 30 minutes ago and radiates to the left arm. What is the most likely diagnosis?",
        "ground_truth": "Myocardial infarction (heart attack)",
        "keywords": ["myocardial infarction", "heart attack", "acute coronary syndrome"],
        "difficulty": "medium"
    },
    {
        "id": "med_002",
        "domain": "medical",
        "problem": "What is the recommended first-line treatment for hypertension in a patient without comorbidities?",
        "ground_truth": "ACE inhibitors or thiazide diuretics",
        "keywords": ["ACE inhibitor", "thiazide", "diuretic"],
        "difficulty": "easy"
    },
    {
        "id": "med_003",
        "domain": "medical",
        "problem": "A child has a temperature of 39°C, severe sore throat, and white patches on tonsils. Rapid strep test is positive. What is the diagnosis and treatment?",
        "ground_truth": "Streptococcal pharyngitis (strep throat), treat with penicillin or amoxicillin",
        "keywords": ["strep throat", "streptococcal pharyngitis", "penicillin", "amoxicillin"],
        "difficulty": "easy"
    },

    # Code Review Domain
    {
        "id": "code_001",
        "domain": "code_review",
        "problem": """Review this Python code for bugs:
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```
What happens if an empty list is passed?""",
        "ground_truth": "Division by zero error - should check if list is empty before dividing",
        "keywords": ["division by zero", "ZeroDivisionError", "empty list"],
        "difficulty": "easy"
    },
    {
        "id": "code_002",
        "domain": "code_review",
        "problem": """Find the security vulnerability:
```python
username = request.form['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```""",
        "ground_truth": "SQL injection vulnerability - should use parameterized queries",
        "keywords": ["SQL injection", "parameterized", "prepared statement"],
        "difficulty": "medium"
    },
    {
        "id": "code_003",
        "domain": "code_review",
        "problem": """What's wrong with this code?
```python
def process_items(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result
```""",
        "ground_truth": "Unpythonic - should use list comprehension or enumerate. No actual bug but not idiomatic.",
        "keywords": ["list comprehension", "unpythonic", "optimization"],
        "difficulty": "easy"
    },

    # Math Domain
    {
        "id": "math_001",
        "domain": "math",
        "problem": "If a train travels at 60 km/h for 2.5 hours, how far does it travel?",
        "ground_truth": "150 km",
        "keywords": ["150"],
        "difficulty": "easy"
    },
    {
        "id": "math_002",
        "domain": "math",
        "problem": "What is the derivative of f(x) = 3x² + 2x - 5?",
        "ground_truth": "f'(x) = 6x + 2",
        "keywords": ["6x + 2", "6x+2"],
        "difficulty": "easy"
    },
    {
        "id": "math_003",
        "domain": "math",
        "problem": "A rectangle has a perimeter of 40 cm and a length of 12 cm. What is its area?",
        "ground_truth": "96 square cm (width = 8 cm, area = 12 × 8 = 96)",
        "keywords": ["96"],
        "difficulty": "medium"
    },

    # Fact Checking Domain
    {
        "id": "fact_001",
        "domain": "fact_checking",
        "problem": "Is it true that the Great Wall of China is visible from space with the naked eye?",
        "ground_truth": "False - this is a common myth. The Great Wall is not visible from space with the naked eye.",
        "keywords": ["false", "myth", "not visible"],
        "difficulty": "easy"
    },
    {
        "id": "fact_002",
        "domain": "fact_checking",
        "problem": "Does lightning never strike the same place twice?",
        "ground_truth": "False - lightning can and does strike the same place multiple times. Tall structures like skyscrapers are struck repeatedly.",
        "keywords": ["false", "myth", "can strike", "multiple times"],
        "difficulty": "easy"
    },
    {
        "id": "fact_003",
        "domain": "fact_checking",
        "problem": "Is it true that humans only use 10% of their brain?",
        "ground_truth": "False - this is a myth. Brain imaging shows all parts of the brain are active, and we use virtually all of it.",
        "keywords": ["false", "myth", "use entire brain"],
        "difficulty": "easy"
    },

    # Logic and Reasoning
    {
        "id": "logic_001",
        "domain": "logic",
        "problem": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?",
        "ground_truth": "No - this is a logical fallacy. We cannot conclude that some roses fade quickly just because some flowers do.",
        "keywords": ["no", "cannot conclude", "fallacy", "invalid"],
        "difficulty": "medium"
    },
    {
        "id": "logic_002",
        "domain": "logic",
        "problem": "You have 3 light switches outside a room. One controls a light bulb inside. You can flip switches but can only enter the room once. How do you determine which switch controls the bulb?",
        "ground_truth": "Turn on switch 1 for 5 minutes, turn it off. Turn on switch 2. Enter room. If bulb is on: switch 2. If off and warm: switch 1. If off and cold: switch 3.",
        "keywords": ["heat", "warm", "temperature", "timing"],
        "difficulty": "hard"
    },

    # Ambiguous/Tricky Cases
    {
        "id": "tricky_001",
        "domain": "ambiguous",
        "problem": "A doctor and a lawyer are both in a car. Who is driving?",
        "ground_truth": "Cannot be determined from the given information - could be either, or neither if someone else is driving.",
        "keywords": ["cannot determine", "insufficient information", "either", "ambiguous"],
        "difficulty": "easy"
    },
    {
        "id": "tricky_002",
        "domain": "ambiguous",
        "problem": "Is a tomato a fruit or a vegetable?",
        "ground_truth": "Both - botanically it's a fruit, but culinarily it's treated as a vegetable. Context matters.",
        "keywords": ["both", "botanically fruit", "culinary vegetable", "context"],
        "difficulty": "medium"
    },

    # Edge Cases Where Single Model Might Struggle
    {
        "id": "edge_001",
        "domain": "medical",
        "problem": "A patient has fever, headache, and a stiff neck. However, they also report these symptoms started after a long flight. What should be considered?",
        "ground_truth": "Meningitis should be considered (medical emergency) but also travel-related illnesses and dehydration. Multiple possibilities require urgent evaluation.",
        "keywords": ["meningitis", "multiple possibilities", "urgent", "differential diagnosis"],
        "difficulty": "hard"
    },
    {
        "id": "edge_002",
        "domain": "code_review",
        "problem": """Is this code thread-safe?
```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
```""",
        "ground_truth": "No - the increment operation is not atomic. In multi-threaded environment, race conditions can occur. Need locks or atomic operations.",
        "keywords": ["not thread-safe", "race condition", "lock", "atomic"],
        "difficulty": "hard"
    },
    {
        "id": "physics_001",
        "domain": "physics",
        "problem": "If a ball is dropped from a height of 100 meters (ignoring air resistance, g = 9.8 m/s^2), how long does it take to hit the ground?",
        "ground_truth": "Approximately 4.52 seconds (using d = 0.5 * g * t^2)",
        "keywords": ["4.5", "4.52", "seconds", "sqrt"],
        "difficulty": "medium"
    },
    {
        "id": "logic_003",
        "domain": "logic",
        "problem": "I am a paradox. 'This statement is false.' Is the statement true or false?",
        "ground_truth": "It is a paradox. If it's true, it's false. If it's false, it's true. It cannot be resolved to a single boolean value.",
        "keywords": ["paradox", "liar paradox", "neither", "unresolvable"],
        "difficulty": "hard"
    },
    {
        "id": "code_004",
        "domain": "code_review",
        "problem": "Can you spot the issue?\n```python\ndef append_to_list(val, my_list=[]):\n    my_list.append(val)\n    return my_list\n```",
        "ground_truth": "Mutable default argument. `my_list` is shared across all function calls that don't provide the second argument.",
        "keywords": ["mutable default", "shared", "None", "my_list=None"],
        "difficulty": "medium"
    }
]

def get_test_cases_by_domain(domain: str):
    """Get all test cases for a specific domain"""
    return [tc for tc in TEST_CASES if tc["domain"] == domain]

def get_test_cases_by_difficulty(difficulty: str):
    """Get all test cases of a specific difficulty"""
    return [tc for tc in TEST_CASES if tc["difficulty"] == difficulty]

def get_all_domains():
    """Get list of all unique domains"""
    return list(set(tc["domain"] for tc in TEST_CASES))
