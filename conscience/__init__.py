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
from conscience.suite import ConscienceSuite
