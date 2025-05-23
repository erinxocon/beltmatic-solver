from functools import cache
from itertools import permutations
from collections import deque
from timeit import timeit
from primefac import primefac, isprime
import timeit


# Define the solver function
def solve_target(target, numbers, operators):
    """
    Solve for the shortest sequence to reach the target number using the given numbers and operators,
    with the addition of a heuristic factor tree using prime factorization.

    Args:
        target (int): The number to reach.
        numbers (list): List of available numbers.
        operators (list): List of available operators (e.g., ['+', '-', '*', '/']).

    Returns:
        list: The shortest pipeline as a list of operations, or None if no solution.
    """

    def apply_operator(a, b, op, /):
        """Apply an operator to two numbers."""
        try:
            if op == "+":
                return a + b
            elif op == "-":
                return a - b
            elif op == "*":
                return a * b
            elif op == "/":
                return a / b if b != 0 and a % b == 0 else None
        except ZeroDivisionError:
            return None

    # Get the prime factors of the target number to create a factor tree
    prime_factors = (
        factors if (factors := list(primefac(target))) and len(factors) > 1 else []
    )

    # Initialize the BFS queue
    queue = deque()
    visited = set(numbers)  # Keep track of visited results

    # Move any prime factors that are in 'numbers' to the front of the queue
    for factor in prime_factors:
        if factor in numbers:
            queue.append((factor, [factor]))  # Move to front

    # Add the base numbers to the queue as well
    for num in numbers:
        if num not in visited:  # Prevent duplicates
            queue.append((num, [num]))

    # If the target is prime and not in `numbers`, add it to enable operations
    if not prime_factors and target not in numbers:
        for num in numbers:
            queue.append((num, [num]))  # Start exploration with available numbers

    while queue:
        current_value, pipeline = queue.popleft()

        # Check if we reached the target
        if current_value == target and len(pipeline) > 1:
            return pipeline

        # Try all combinations of numbers and operators
        for num in numbers:
            for op in operators:
                result = apply_operator(current_value, num, op)

                # Skip invalid results
                if result is None or result in visited:
                    continue

                # Add new state to the queue
                visited.add(result)
                queue.append((result, pipeline + [op, num]))

    # Log a message if no solution is found
    print("No solution found for target:", target)
    return None


# look at 24, not the shortest provided the base numbers


# Example Usage
def test():
    target = 4795  # Prime target
    numbers = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        15,
        18,
        19,
        24,
        40,
        44,
        45,
        50,
        54,
        58,
        82,
        162,
        169,
        263,
        275,
        277,
        180,
        275,
        277,
        338,
        381,
        511,
        554,
        561,
        # 636,
        703,
    ]
    numbers.sort(reverse=True)
    operators = ["+", "*", "-", "/"]

    solution = solve_target(target, numbers, operators)
    print(f"Solution: {solution} = {target}")


# Now time it:
elapsed = timeit.timeit(test, number=1)
print(f"Elapsed time old: {elapsed:.6f} seconds")
