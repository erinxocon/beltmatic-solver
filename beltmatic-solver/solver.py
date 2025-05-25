import heapq
import timeit
from collections.abc import Callable
from operator import add, mul
from operator import pow as _pow
from operator import sub
from typing import Literal, TypeAlias

from operation_node import OperationNode

OperatorStr: TypeAlias = Literal["+"] | Literal["-"] | Literal["*"] | Literal["/"] | Literal["**"]

ArithmeticCallable: TypeAlias = Callable[[OperationNode, int], list[OperationNode]]

OPERATOR_MAP: dict[OperatorStr, ArithmeticCallable] = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": divmod,
    "**": _pow,
}


def apply_op(current: OperationNode, operand: int, op: OperatorStr) -> list["OperationNode"]:

    # no negative exponents for now, nothing above 10 or the numbers/search space gets unnessasarily large
    if op == "**" and (operand < 0 or operand > 11):
        return []

    if op == "**" and (current.total_value < 0) and operand % 2 == 1:
        return []

    # Do not divide by zero, the computer will blow up
    if op == "/" and operand == 0:
        return []

    # Skip redundant 0 for + and -
    if op in {"+", "-"} and operand == 0:
        return []

    # Skip redundant 1 for * and /
    if op in {"*", "/"} and operand == 1:
        return []

    try:
        return OPERATOR_MAP[op](current, operand)
    except KeyError:
        # unknown operator, skipping
        return []


def heapq_solve(
    target: int, start_numbers: list[int], allowed_ops: set[OperatorStr] | None = None
) -> OperationNode | None:
    if not allowed_ops:
        allowed_ops = {"+", "-", "*", "/", "**"}

    visited: dict[int, int] = dict()
    heap: list[tuple[int, OperationNode]] = []

    # Initialize with each starting number as its own node
    for num in start_numbers:
        node = OperationNode(total_value=num)
        heapq.heappush(heap, (node.node_id, node))
        visited[node.total_value] = node.node_id
        if num == target:
            return node

    while heap:
        _, current = heapq.heappop(heap)

        if current.total_value == target:
            return current

        for op in allowed_ops:
            for operand in start_numbers:
                try:
                    results: list[OperationNode] = apply_op(
                        current=current, operand=operand, op=op
                    )
                except (ZeroDivisionError, OverflowError, ValueError):
                    continue
                else:
                    for node in results:
                        if not (-3 * target <= node.total_value <= 3 * target):
                            continue
                        if (
                            node.total_value not in visited
                            or node.node_id < visited[node.total_value]
                        ):
                            visited[node.total_value] = node.node_id
                            heapq.heappush(heap, (node.node_id, node))
    return None


if __name__ == "__main__":
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

    start_numbers = [1, 2, 3, 5]
    target = 13

    def solve2() -> None:
        result_node: OperationNode | None = heapq_solve(
            target, start_numbers, allowed_ops={"*", "+", "-", "/"}
        )
        if result_node:
            print("Solution:", result_node)
            print("Steps:", result_node.node_id)
        else:
            print("No solution found.")

    elapsed: float = timeit.timeit(solve2, number=1)
    print(f"Elapsed time heapq: {elapsed:.6f} seconds")
