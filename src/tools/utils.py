import random
import operator


def generate_math_questions(level, op_types, num_questions=5):
    """
    Generate a list of math questions with their answers based on difficulty level and operation types.

    Parameters:
    level (int): Difficulty level from 1 to 5
    op_types (list): List of operation types to include ["add", "subtract", "multiply", "divide"]
    num_questions (int): Number of questions to generate

    Returns:
    list: List of dictionaries containing question, answer, and id
    """
    # Define operation functions and symbols
    operations = {
        "add": (operator.add, "+"),
        "subtract": (operator.sub, "-"),
        "multiply": (operator.mul, "×"),
        "divide": (operator.truediv, "÷"),
    }

    # Define number ranges based on level
    ranges = {
        1: (1, 10),  # 1st-2nd grade: single digits
        2: (1, 20),  # 3rd-4th grade: numbers up to 20
        3: (1, 50),  # 5th grade: numbers up to 50
        4: (1, 200),  # 6th-7th grade: numbers up to 200
        5: (1, 1000),  # 8th-9th grade: numbers up to 1000
    }

    # Adjust difficulty of operations based on level
    if level not in ranges:
        level = min(max(level, 1), 5)  # Ensure level is between 1-5

    min_num, max_num = ranges[level]

    questions = []

    for i in range(num_questions):
        # Randomly select an operation from requested types
        op_type = random.choice(op_types)
        op_func, op_symbol = operations[op_type]

        # Generate numbers based on level and operation
        if op_type == "divide":
            # For division, ensure we have a clean division (no remainder for easier levels)
            if level <= 3:
                # For easier levels, make sure division results in whole numbers
                b = random.randint(1, min(max_num // 2, 10))
                result = random.randint(1, min(max_num // b, 10))
                a = b * result
            else:
                # For harder levels, allow non-integer results
                a = random.randint(min_num, max_num)
                b = random.randint(
                    1, min(a, 20)
                )  # Limit divisor to avoid tiny fractions
                result = op_func(a, b)
                # Round to 2 decimal places for division
                result = round(result, 2)
        elif op_type == "multiply":
            # Adjust multiplication difficulty based on level
            if level <= 2:
                a = random.randint(1, 10)
                b = random.randint(1, 10)
            elif level <= 4:
                a = random.randint(2, 12)
                b = random.randint(2, min(max_num // a, 12))
            else:
                a = random.randint(5, 20)
                b = random.randint(5, min(max_num // a, 50))
            result = op_func(a, b)
        else:  # add or subtract
            a = random.randint(min_num, max_num)
            b = random.randint(min_num, max_num)

            # For subtraction, ensure a >= b for levels 1-3 (no negative results)
            if op_type == "subtract" and level <= 3 and a < b:
                a, b = b, a

            result = op_func(a, b)

        # Format the question
        question = f"{a} {op_symbol} {b}"

        # Add to questions list
        questions.append({"question": question, "answer": result, "id": i})

    return questions


# Example usage:
if __name__ == "__main__":
    # Examples for different levels
    print("Level 1 (1st-2nd grade):")
    print(generate_math_questions(level=1, op_types=["add", "subtract"]))

    print("\nLevel 3 (5th grade):")
    print(
        generate_math_questions(
            level=3, op_types=["add", "subtract", "multiply", "divide"]
        )
    )

    print("\nLevel 5 (8th-9th grade):")
    print(
        generate_math_questions(
            level=5, op_types=["add", "subtract", "multiply", "divide"]
        )
    )
