
from typing import Any, Self, Union

from predicate import Predicate
from operators import Operators


class Field:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.owner = owner
        self.name = name
        self.obj = None

    def __get__(self, obj: Any, obj_type: Any = None) -> Union[Any, Self]:
        if obj:
            return obj.__dict__[self.name]
        else:
            return self

    def __set__(self, obj: Any, value: Any) -> None:
        self.obj = obj
        obj.__dict__[self.name] = value

    def __eq__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.EQ, other)

    def __le__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.LTE, other)

    def __lt__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.LT, other)

    def __ge__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.GTE, other)

    def __gt__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.GT, other)

    def __ne__(self, other: Any) -> Predicate:
        return Predicate(self.owner, self.name, Operators.NE, other)

    def __str__(self) -> str:
        return f'{self.owner.__name__}.{self.name}'
