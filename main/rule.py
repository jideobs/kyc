from dataclasses import dataclass
from typing import Any, List, Self

from datasources import datasource_factory
from descriptors import Field
from models import DatasourceType
from operators import Operators
from predicate import Predicate


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
        self._data_to_fetch = {}

        self._executed = False
        self._threshold = 1
        self._score = 0

    def _fetch(self, _type: DatasourceType) -> None:
        if _type in self._data:
            return self._data[_type]
        datasource = datasource_factory.get_datasource(_type)
        self._data[_type] = datasource.get(*self._data_to_fetch[_type])
        return self._data[_type]

    def _extract(self, predicate: Predicate) -> (Any, Any):
        actual_val = getattr(self._fetch(predicate.owner.type_), predicate.field)
        expected_val = predicate.other
        if isinstance(predicate.other, Field):
            expected_val = getattr(self._fetch(predicate.other.owner.type_), predicate.other.name)
        return actual_val, expected_val

    def threshold(self, val: float) -> Self:
        self._threshold = val
        return self

    @property
    def score(self) -> float:
        return self._score

    def fetch(self, _type: DatasourceType, *_input: Any) -> Self:
        self._data_to_fetch[_type] = _input
        return self

    def where(self, *predicates: Predicate) -> Self:
        self.predicates += predicates
        return self

    def fuzzy_match(self, val_a: Any, val_b: Any) -> Self:
        self.predicates.append(Predicate(val_a.owner, val_a.name, Operators.Nil, val_b))
        return self

    def execute(self):
        self._executed = True

        for predicate in self.predicates:
            actual_val, expected_val = self._extract(predicate)
            score = int(predicate.compare(actual_val, expected_val))

            self._score += score
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
        self._either_rules = []
        self._or_rules = []

        self._threshold = 1

        self._score = 0
        self._either_score = 0

    def is_valid(self) -> bool:
        return self._score >= self._threshold

    def threshold(self, val: float) -> Self:
        self._threshold = val
        return self

    def either(self, rules: List[Rule]) -> Self:
        self._either_rules = rules
        return self

    def or_(self, rules: List[Rule]) -> Self:
        self._or_rules = rules
        return self

    @property
    def score(self) -> float:
        return self._score

    def execute(self) -> Self:
        score = 0
        for rule in self._either_rules:
            rule.execute()
            score += rule.score
        self._score = score/len(self._either_rules)

        if self._score >= self._threshold:
            self._either_score = self._score
            score = 0
            for rule in self._or_rules:
                rule.execute()
                score += rule.score
        self._score = score/len(self._or_rules)

        return self

    def __bool__(self):
        return self.is_valid()
