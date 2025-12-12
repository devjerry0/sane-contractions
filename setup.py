from setuptools import find_packages, setup

MAJOR_VERSION = "0"
MINOR_VERSION = "2"
MICRO_VERSION = "0"
VERSION = f"{MAJOR_VERSION}.{MINOR_VERSION}.{MICRO_VERSION}"

setup(
    name="sane-contractions",
    version=VERSION,
    description=(
        "Enhanced fork of contractions library - "
        "Expands English contractions with improved performance and new features"
    ),
    author="Jeremy Bruns",
    author_email="99199491+devjerry0@users.noreply.github.com",
    maintainer="Jeremy Bruns",
    maintainer_email="99199491+devjerry0@users.noreply.github.com",
    url="https://github.com/devjerry0/sane-contractions",
    project_urls={
        "Original Repository": "https://github.com/kootenpv/contractions",
        "Bug Tracker": "https://github.com/devjerry0/sane-contractions/issues",
        "Documentation": "https://github.com/devjerry0/sane-contractions#readme",
    },
    package_data={
        "contractions": ["data/*.json"]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    platforms="any",
    python_requires=">=3.10",
    install_requires=["textsearch>=0.0.24"],
)
