from typing import Any, List, Self, Union
from dataclasses import dataclass

from datasources import datasource_factory
from descriptors import Field
from predicate import Predicate
from models import DatasourceType
from operators import Operators


@dataclass
class Result:
    checked: str
    score: int


class Rule:
    def __init__(self, name):
        self.name = name
        self._result_set = []
        self.predicates = []
        self._data = {}

        self._executed = False

    def _extract(self, predicate: Predicate) -> (Any, Any):
        actual_val = getattr(self._data[predicate.owner.type_], predicate.field)
        expected_val = predicate.other
        if isinstance(predicate.other, Field):
            expected_val = getattr(self._data[predicate.other.owner.type_], predicate.other.name)
        return actual_val, expected_val

    def fetch(self, _type: DatasourceType, *_input: Any) -> Self:
        datasource = datasource_factory.get_datasource(_type)
        self._data[_type] = datasource.get(*_input)
        return self

    def where(self, *predicates: Predicate) -> Self:
        self.predicates += predicates
        return self

    def fuzzy_match(self, val_a: Field, val_b: Field) -> Self:
        self.predicates.append(Predicate(val_a.owner, val_a.name, Operators.Nil, val_b))
        return self

    def execute(self):
        self._executed = True

        for predicate in self.predicates:
            actual_val, expected_val = self._extract(predicate)
            score = int(predicate.compare(actual_val, expected_val))

            self._result_set.append(
                Result(checked=str(predicate), score=score))

    def result(self) -> List:
        if not self._executed:
            self.execute()
        return self._result_set

    def __str__(self) -> str:
        return f'Rule(name={self.name}, result={self._result_set})'


class RulesExecutor:
    def __init__(self, name: str):
        self.name = name

    def _execute(self, *rules: Rule) -> Self:
        for rule in rules:
            rule.execute()
        return self

    def either(self, *rules: Rule) -> Self:
        self._execute(*rules)
        return self

    def then(self, *rules: Rule) -> Self:
        self._execute(*rules)
        return self

    def or_(self, *rules: Rule) -> Self:
        self._execute(*rules)
        return self
