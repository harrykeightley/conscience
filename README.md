# director

_Perform automated testing of Tkinter GUI applications_

Director is a tool that allows automated acceptance testing
of Tkinter GUI applications.

The tool is designed for automated assessment of introductory
programming assignments.
As such, there is included support to recognize GUI widgets
based upon a description of their functionality.

## Requirements

* Python 3.9+
* Tkinter
* behave (https://behave.readthedocs.io/en/stable/)

## Installation

For unix users, you can run a tiny bash setup script.
```bash
. ./bin/setup.sh
```

For Windows users, use pip to install all the requirements in `requirements.txt`.

To ensure that everything is install correctly, run the test suite.

```bash
./bin/test.sh
```
