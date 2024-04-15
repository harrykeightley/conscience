name = "conscience"

from conscience.config import ConscienceConfiguration, GradescopeConfiguration, build_config, setup_config
from conscience.main import setup, run_tests


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
