from dataclasses import dataclass
from io import BytesIO
import json
from typing import IO, TypedDict


class GradeScopeScoreDict(TypedDict):
    score: int
    output: str


class GradeScopeAggregatedTests(TypedDict):
    tests: list[GradeScopeScoreDict]


@dataclass
class GradeScopeScore:
    score: int
    output: str

    def to_dict(self) -> GradeScopeScoreDict:
        return {"score": self.score, "output": self.output}

    def to_aggregated_tests(self) -> GradeScopeAggregatedTests:
        return {"tests": [self.to_dict()]}

    @staticmethod
    def from_dict(data: GradeScopeScoreDict):
        return GradeScopeScore(data["score"], data["output"])

    @staticmethod
    def from_json(fp: IO):
        return GradeScopeScore.from_dict(json.load(fp))

    @staticmethod
    def from_stream(stream: BytesIO):
        try:
            stream.seek(0)
            return GradeScopeScore.from_json(stream)
        except json.JSONDecodeError:
            stream.seek(0)
            return GradeScopeScore(score=0, output=stream.read().decode())
