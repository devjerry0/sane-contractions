from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "contractions": ["data/*.json"]
    },
)
