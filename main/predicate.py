from typing import Any

from operators import Operators


class Predicate:
    def __init__(self, owner, field: str, operator: Operators, other: Any) -> None:
        self.owner = owner
        self.field = field
        self.operator = operator
        self.other = other

    def compare(self, actual_val: Any, expected_val: Any) -> bool:
        if self.operator == Operators.EQ:
            return actual_val == expected_val
        elif self.operator == Operators.LT:
            return actual_val < expected_val
        elif self.operator == Operators.GT:
            return actual_val > expected_val
        elif self.operator == Operators.LTE:
            return actual_val <= expected_val
        elif self.operator == Operators.GTE:
            return actual_val >= expected_val
        elif self.operator != Operators.NE:
            return actual_val != expected_val
        else:
            raise NotImplemented(f'operation for operator {self.operator} not implemented')

    def fuzzy_match(self, val_a: Any, val_b: Any) -> bool:
        return False

    def __str__(self) -> str:
        return f'{self.owner.__name__}.{self.field} {self.operator.value} {self.other}'
