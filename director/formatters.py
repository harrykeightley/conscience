import json
from behave.formatter.base import Formatter
from behave.model import Scenario, Step
from behave.model_core import Status


def parse_tag_value(scenario: Scenario, tag_name: str, default=None):
    marks = filter(lambda tag: tag.startswith(tag_name), scenario.tags)
    marks = map(lambda tag: tag[len(tag_name):].strip("()"), marks)
    marks = filter(lambda tag: tag.isnumeric(), marks)

    return next(marks, default)

class GradescopeFormatter(Formatter):
    # def feature(self, feature):
    #     print(feature)

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)

        self._tests = []
        self._results = {
            "tests": self._tests
        }

        self.reset(None)

    def reset(self, scenario):
        self._current_scenario: Scenario = scenario
        self._passed = True
        self._output = ""

    def _make_test(self):
        weight = parse_tag_value(self._current_scenario, "weight", default=1)

        return {
            "score": weight if self._passed else 0,
            "max_score": weight,
            "name": f"Scenario: {self._current_scenario.name}",
            "output": self._output,
            "visibility": "visible",
        }
    
    def scenario(self, scenario):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        self.reset(scenario)

    def result(self, step: Step):
        if step.status == Status.passed:
            self._output += f"{step.keyword} {step.name}\n"
            return

        self._passed = False

        if step.status == Status.skipped:
            self._output += f"{step.keyword} {step.name} (skipped)\n"
            return

        self._output += f"""{step.keyword} {step.name}
    status: {step.status}
    {step.error_message}

    output: {step.captured.output}
"""

        

    def eof(self):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        print()

    def close(self):
        self.stream.write(json.dumps(self._results))
        super().close()

    # def step(self, step):
    #     print(step)
