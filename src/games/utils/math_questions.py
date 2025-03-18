import operator
import random

OPS = {
    "add": ("+", operator.add),
    "subtract": ("-", operator.sub),
    "multiply": ("×", operator.mul),
    "divide": (
        "÷",
        lambda a, b: a // b if b != 0 and a % b == 0 else None,
    ),  # Ensure valid division
}


def get_num_operands(level):
    """
    Determines the number of operands based on the level.

    For level 1: Randomly selects between 2-5 operands
    For level 2+: Higher probability of 2 operands (70%) vs 3 operands (30%)
    As level increases, gradually shifts toward lower numbers

    Args:
        level (int): The current difficulty level (1-5)

    Returns:
        int: The number of operands to use
    """
    if level == 1:
        # For level 1, randomly select between 2-5 operands
        return random.randint(2, 5)
    else:
        # For levels 2-5, gradually increase the weight for 2 operands
        # Level 2: 70% chance of 2 operands, 30% chance of 3 operands
        # Level 5: 90% chance of 2 operands, 10% chance of 3 operands
        weight_for_two = 0.7 + (level - 2) * 0.05  # Increases from 0.7 to 0.85
        weight_for_three = 1 - weight_for_two

        return random.choices([2, 3], weights=[weight_for_two, weight_for_three])[0]


def generate_math_questions(level, op_types, num_questions=5):
    """Generates math questions with multi-step expressions and brackets."""
    questions = []
    attempts = 0
    max_attempts = num_questions * 10  # Prevent infinite loop

    while len(questions) < num_questions and attempts < max_attempts:
        attempts += 1

        num_operands = get_num_operands(level)
        numbers = []
        operators = []

        # Generate numbers based on difficulty level
        for _ in range(num_operands):
            if level == 1:  # 🟢 Easy (small numbers)
                numbers.append(random.randint(1, 10))
            elif level == 2:  # 🟡 Medium
                numbers.append(random.randint(10, 50))
            elif level == 3:  # 🟠 Hard
                numbers.append(random.randint(10, 100))
            elif level == 4:  # 🔴 Expert
                numbers.append(random.randint(20, 200))
            elif level == 5:  # 🟣 Master (Includes negatives)
                numbers.append(random.randint(-100, 100))

        # Select operators from allowed `op_types`
        for _ in range(num_operands - 1):
            op = random.choice(op_types)
            operators.append(op)

        # Construct the question string and calculate result
        question_parts = []

        # Determine bracket placement before constructing the expression
        has_brackets = level >= 1 and random.random() > 0.5
        bracket_start = -1
        bracket_end = -1

        if has_brackets:
            # Choose a position for brackets that ensures we're bracketing exactly two numbers and one operator
            bracket_start = random.randint(
                0, num_operands - 2
            )  # Start bracket at a number
            bracket_end = (
                bracket_start + 2
            )  # End bracket after the next number (enclosing 2 numbers and 1 operator)

        # Now build the expression
        for j in range(num_operands):
            # Add opening bracket if needed
            if has_brackets and j == bracket_start:
                question_parts.append("(")

            # Add the number
            question_parts.append(str(numbers[j]))

            # Add closing bracket if needed
            if has_brackets and j == bracket_end:
                question_parts.append(")")

            # Add operator if not the last number
            if j < num_operands - 1:
                op_symbol, _ = OPS[operators[j]]
                question_parts.append(op_symbol)

        question = " ".join(question_parts)

        # Calculate the correct result considering operator precedence and brackets
        try:
            # Replace × and ÷ with Python operators * and /
            calc_expr = question.replace("×", "*").replace("÷", "/")

            # Force integer division for division operations
            for j, op in enumerate(operators):
                if op == "divide":
                    # Find the division operation in the expression and ensure it's using //
                    calc_expr = calc_expr.replace("/", "//", 1)

            # Evaluate the expression
            result = eval(calc_expr)

            # Check if division is valid (no division by zero or fractional results)
            if "// 0" in calc_expr or (
                isinstance(result, float) and not result.is_integer()
            ):
                continue  # Skip this question
            if question.startswith("(") and question.endswith(")"):
                continue
            if level == 1 and result < 0:
                continue

            questions.append(
                {"id": len(questions), "question": question, "answer": int(result)}
            )

        except Exception:
            # Skip questions that can't be evaluated
            continue

    # If we couldn't generate enough questions, return what we have
    return questions


# Example usage:
if __name__ == "__main__":
    # Generate questions with progressive difficulty
    print("Sample questions with progressive difficulty:")
    questions = generate_math_questions(
        level=1, op_types=["add", "divide"], num_questions=5
    )
    for q in questions:
        print(f"Question {q['id']}: {q['question']} = {q['answer']}")
