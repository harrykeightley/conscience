import subprocess, os

from behave.model import Status
from director import setup, logger


def before_feature(context, feature):
    setup(context)
    logger.debug("environment setup")


def after_step(context, step):
    if step.status == Status.failed:
        window_id = context.window.winfo_id()
        # my_env = os.environ.copy()
        # my_env["DISPLAY"] = ":1"
        # subprocess.Popen(["import", "-window", str(window_id), "/autograder/results/screenshot.png"], env=my_env)
        # subprocess.Popen(["xwininfo", "-tree", "-root"])
        # check_output(["DISPLAY=:0", "import", "-window", str(window_id), "/autograder/results/screenshot.png"])
