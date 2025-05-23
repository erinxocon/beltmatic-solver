import timeit
from collections import deque

from operator import add, mul
from operator import pow as _pow
from operator import sub

import heapq
from .operation_node import OperationNode

OPERATOR_MAP = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": divmod,
    "**": _pow,
}


def apply_op(current: "OperationNode", operand: int, op: str) -> list["OperationNode"]:
    # no negative exponents for now
    if op == "**" and operand < 0:
        raise ValueError("No negative operators please!")
    # Do not divide by zero, the computer will blow up
    if op == "/" and operand == 0:
        raise ZeroDivisionError

    # # Avoid duplicates due to communitivity
    # if op in {"+", "*"} and current.total_value > operand:
    #     return []

    try:
        return OPERATOR_MAP[op](current, operand)
    except KeyError:
        # unknown operator, skipping
        return []


def bfs_solve(
    target: int,
    start_numbers: list[int],
    allowed_ops: list[str] = ["+", "-", "*", "**", "/"],
) -> OperationNode | None:
    visited = dict()
    queue: deque[OperationNode] = deque()

    # Initialize with each starting number as its own node
    for num in start_numbers:
        node = OperationNode(total_value=num)
        queue.append(node)
        visited[node.total_value] = node.node_id

        if num == target:
            return node

    while queue:
        current = queue.popleft()

        # Success!
        if current.total_value == target:
            return current

        # Try every operation with every allowed operand
        for op in allowed_ops:
            for operand in start_numbers:
                try:
                    results = apply_op(current=current, operand=operand, op=op)
                except (ZeroDivisionError, OverflowError, ValueError):
                    continue
                else:
                    for node in results:
                        if (
                            node.total_value not in visited
                            or node.node_id < visited[node.total_value]
                        ):
                            visited[node.total_value] = node.node_id
                            queue.append(node)

    # If target not found
    return None


def heapq_solve(
    target: int,
    start_numbers: list[int],
    allowed_ops: list[str] = ["+", "-", "*", "**", "/"],
) -> OperationNode | None:
    visited = dict()
    heap = []

    # Initialize with each starting number as its own node
    for num in start_numbers:
        node = OperationNode(total_value=num)
        heapq.heappush(heap, (node.node_id, node))
        visited[node.total_value] = node.node_id
        if num == target:
            return node

    while heap:
        cost, current = heapq.heappop(heap)
        # print(f"Heap pop: {current} (steps={current.node_id})")

        if current.total_value == target:
            return current

        for op in allowed_ops:
            for operand in start_numbers:
                try:
                    results = apply_op(current=current, operand=operand, op=op)
                except (ZeroDivisionError, OverflowError, ValueError):
                    continue
                else:
                    for node in results:
                        if (
                            node.total_value not in visited
                            or node.node_id < visited[node.total_value]
                        ):
                            visited[node.total_value] = node.node_id
                            heapq.heappush(heap, (node.node_id, node))
    return None


start_numbers = list(
    set(
        [
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
    )
)
target = 4795


def solve1():
    result_node = bfs_solve(target, start_numbers, allowed_ops=["+", "*", "/"])
    if result_node:
        print("Solution:", result_node)
        print("Steps:", result_node.node_id)
    else:
        print("No solution found.")


def solve2():
    result_node = heapq_solve(target, start_numbers, allowed_ops=["+", "*", "/"])
    if result_node:
        print("Solution:", result_node)
        print("Steps:", result_node.node_id)
    else:
        print("No solution found.")


# Now time it:
elapsed = timeit.timeit(solve1, number=1)
print(f"Elapsed time BFS: {elapsed:.6f} seconds")

elapsed = timeit.timeit(solve2, number=1)
print(f"Elapsed time heapq: {elapsed:.6f} seconds")
