from functools import total_ordering
from typing import Any


@total_ordering
class OperationNode:
    __slots__: tuple[str, ...] = ("total_value", "op", "prev", "node_id")

    def __init__(
        self,
        total_value: int,
        *,
        op: str | None = None,
        prev: "OperationNode | None" = None,
        node_id: int | None = None,
    ) -> None:
        self.total_value: int = total_value
        self.op = op
        self.prev = prev
        self.node_id = (
            node_id if node_id is not None else (prev.node_id + 1 if prev is not None else 0)
        )

    def __add__(self, a: int, /) -> list["OperationNode"]:
        return [OperationNode(self.total_value + a, op=f"+ {a}", prev=self)]

    def __sub__(self, a: int, /) -> list["OperationNode"]:
        return [OperationNode(self.total_value - a, op=f"- {a}", prev=self)]

    def __mul__(self, a: int, /) -> list["OperationNode"]:
        return [OperationNode(self.total_value * a, op=f"* {a}", prev=self)]

    def __pow__(self, a: int, /) -> list["OperationNode"]:
        return [OperationNode(self.total_value**a, op=f"^{a}", prev=self)]

    def __divmod__(self, a: int, /) -> list["OperationNode"]:
        q, r = divmod(self.total_value, a)
        results = [OperationNode(q, op=f"/ {a}", prev=self)]
        if r != 0:
            results.append(OperationNode(r, op=f"% {a}", prev=self))
        return results

    def __hash__(self):
        return hash((self.total_value, self.node_id))

    def __eq__(self, a: Any) -> bool:
        if not isinstance(a, OperationNode):
            return NotImplemented
        return self.total_value == a.total_value and self.node_id == a.node_id

    def __lt__(self, a: Any) -> bool:
        if not isinstance(a, OperationNode):
            return NotImplemented
        return (
            (self.total_value < a.total_value)
            if self.total_value != a.total_value
            else (self.node_id < a.node_id)
        )

    def __str__(self) -> str:
        steps = []
        node = self
        while node:
            if node.op:
                steps.append(node.op)
            else:
                steps.append(f"{node.total_value}")  # This would be a starting node
            node = node.prev
        return " ".join(reversed(steps))

    def __repr__(self) -> str:
        return f"OperationNode({self.total_value}, node_id={self.node_id})"
