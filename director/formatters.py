import json
from behave.formatter.base import Formatter
from behave.model import Scenario, Step
from behave.model_core import Status


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
        return {
            "score": 1 if self._passed else 0,
            "max_score": 1,
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
        print()

    def close(self):
        self.stream.write(json.dumps(self._results))
        super().close()

    # def step(self, step):
    #     print(step)
