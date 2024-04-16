name = "conscience"

from conscience.config import (
    ConscienceConfiguration,
    GradescopeConfiguration,
    build_config,
    setup_config,
)
from conscience.main import (
    setup,
    witness,
    load_common_steps,
)
from conscience.score import (
    GradescopeResults,
    TestScore,
    aggregate_results,
    export_results,
)


# __export__ = [
#     MixinBase,
#     LogMixin,
#     RelayMixin,
#     MockMixin,
#     VacantLog,
#     RelayLog,
#     MockLog,
#     WidgetSelector,
#     setup,
# ]
# __test__ = {obj.__name__: obj for obj in __export__}
# __all__ = [cls.__name__ for cls in __export__] + ["logger", "find_widgets"]
