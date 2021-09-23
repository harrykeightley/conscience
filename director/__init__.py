name = "director"

import logging
logger = logging.getLogger(__package__)

from .formats import register_formats
from .mocking import MixinBase, LogMixin, RelayLog, MockMixin
from .mocking import VacantLog, RelayLog, MockLog
from .identify import WidgetSelector, find_widgets

def setup():
    register_formats()

__export__ = [MixinBase, LogMixin, RelayLog, MockMixin, VacantLog, RelayLog, MockLog, WidgetSelector, setup]
__test__ = {obj.__name__ : obj for obj in __export__}
__all__ = [cls.__name__ for cls in __export__] + ["logger", "find_widgets"]
