from director import test


def main():
    test(
        "tests1",
        "/autograder/submission/a3.py",
        gradescope=True,
        metadata={
            "student_metadata": "/autograder/submission_metadata.json",
            "student_categories": "/autograder/source/metadata/student_types.csv",
        },
    )


if __name__ == "__main__":
    main()
