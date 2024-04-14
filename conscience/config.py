import traceback
from io import BytesIO
from pathlib import Path
from types import ModuleType
from typing import NoReturn, Optional, TypedDict, override

from behave.__main__ import Configuration
from behave.formatter.base import Formatter, StreamOpener

from conscience.formatters import GradescopeFormatter
from conscience.score import GradeScopeScore
from conscience.suite import ConscienceSuite
from conscience.config import ConscienceConfiguration


class GradeScopeMetadata(TypedDict):
    student_categories: str
    student_metadata: str


class ConscienceConfiguration(Configuration):
    def __init__(self, command_args=None, load_config=True, verbose=None, **kwargs):
        super().__init__(command_args, load_config, verbose, **kwargs)
        self.suite: Optional[ConscienceSuite] = None
        self.paths: list[Path] = []
        self.under_test: Optional[ModuleType] = None
        self.more_formatters: Optional[dict[str, type[Formatter]]] = None
        self.working_directory: Optional[Path] = None

    def load_target(self, target: Path):
        self.under_test = load_under_test(target)

    def load_metadata(self, metadata: GradeScopeMetadata):
        pass

    def handle_load_failure(self, e: Exception) -> GradeScopeScore | NoReturn:
        raise e

    def reset_outputs(self):
        pass

    def read_score(self) -> GradeScopeScore:
        return GradeScopeScore(score=0, output="Dummy result")


class GradescopeConfiguration(ConscienceConfiguration):
    def __init__(self, command_args=None, load_config=True, verbose=None, **kwargs):
        super().__init__(command_args, load_config, verbose, **kwargs)
        self.student_categories: Optional[str] = None
        self.student_metadata: Optional[str] = None
        self.default_format = "gradescope"
        self.more_formatters = {"gradescope": GradescopeFormatter}

    @override
    def reset_outputs(self):
        self.output_stream = BytesIO()
        self.outputs = [self.output_stream]

    def handle_load_failure(self, e: Exception):
        return GradeScopeScore(score=0, output=traceback.format_exc())

    @override
    def load_metadata(self, metadata: GradeScopeMetadata):
        self.student_categories = metadata["student_categories"]
        self.student_metadata = metadata["student_metadata"]

    @override
    def read_score(self) -> GradeScopeScore:
        return GradeScopeScore.from_stream(self.output_stream)


def build_config(
    is_gradescope: bool = False,
) -> ConscienceConfiguration:
    extra_args = [] if not is_gradescope else ["--no-summary"]
    command_args = ["--no-source", "--no-timings"] + extra_args
    clz = GradescopeConfiguration if is_gradescope else ConscienceConfiguration
    return clz(command_args=command_args)


def setup_config(
    config: ConscienceConfiguration,
    suite: ConscienceSuite,
    tests: Path | list[Path],
    environment_file: Path = Path("../environment.py"),
    working_directory: Path = Path("."),
    metadata: Optional[GradeScopeMetadata] = None,
):
    config.steps_dir = "."
    config.paths = tests
    config.environment_file = environment_file
    config.suite = suite
    config.working_directory = working_directory
    config.log_capture = False

    if metadata:
        config.load_metadata(metadata)
