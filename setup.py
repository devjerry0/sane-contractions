import re
from pathlib import Path

from setuptools import find_packages, setup

version_file = Path(__file__).parent / "contractions" / "_version.py"
version_content = version_file.read_text()
version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_content, re.M)
if not version_match:
    raise RuntimeError("Unable to find version string.")
VERSION = version_match.group(1)

setup(
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "contractions": ["data/*.json"]
    },
)
