import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="director-tester",
    version="0.0.1",
    packages=[
        'director',
    ],
    install_requires=["behave", "Pillow"],
    description="Perform automated testing of Tkinter GUI applications",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/BraeWebb/director",
    author="Brae Webb",
    author_email="b.webb@uq.edu.au",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)