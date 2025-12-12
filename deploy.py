"""
DEPRECATED: Use GitHub Actions (.github/workflows/publish.yml) instead
This script is kept for backward compatibility and manual releases
"""
import re
import subprocess
import sys


def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def main():
    commit_count = run_command("git rev-list --all --count").strip()

    with open("setup.py") as f:
        setup = f.read()

    setup = re.sub('MICRO_VERSION = "[0-9]+"', f'MICRO_VERSION = "{commit_count}"', setup)

    major_match = re.search('MAJOR_VERSION = "([0-9]+)"', setup)
    minor_match = re.search('MINOR_VERSION = "([0-9]+)"', setup)
    micro_match = re.search('MICRO_VERSION = "([0-9]+)"', setup)

    if not all([major_match, minor_match, micro_match]):
        print("Error: Could not extract version numbers from setup.py", file=sys.stderr)
        sys.exit(1)

    major = major_match.groups()[0]
    minor = minor_match.groups()[0]
    micro = micro_match.groups()[0]
    version = f"{major}.{minor}.{micro}"

    print(f"Building version: {version}")

    with open("setup.py", "w") as f:
        f.write(setup)

    with open("contractions/__init__.py") as f:
        init = f.read()

    with open("contractions/__init__.py", "w") as f:
        f.write(re.sub('__version__ = "[0-9.]+"', f'__version__ = "{version}"', init))

    print("Building distribution...")
    run_command("python -m build")

    print("Checking distribution...")
    run_command("twine check dist/*")

    response = input(f"Upload version {version} to PyPI? [y/N]: ")
    if response.lower() == 'y':
        run_command("twine upload dist/*")
        print(f"Successfully published version {version}!")
    else:
        print("Upload cancelled")


if __name__ == "__main__":
    main()
