import json
from json.decoder import JSONDecodeError
import subprocess


def test_file(file):
    output = subprocess.check_output(f"python3.9 {file}", shell=True)

    try:
        results = json.loads(output)
    except JSONDecodeError:
        print(json.dumps({"score": 0, "output": f"unable to decode json: {output}"}))
        return None

    if "tests" not in results:
        print(results)
        return None

    return results["tests"]


def main():
    task1 = test_file("task1.py")
    task2 = test_file("task2.py")

    if task1 is None or task2 is None:
        return

    print(json.dumps({"tests": task1 + task2}))


if __name__ == "__main__":
    main()
