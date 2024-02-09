"""
setup.py: Setup script for mac-signing-buddy application.

Usage:
    python3 -m build --wheel
"""

from setuptools import setup, find_packages


def fetch_property(property: str) -> str:
    """
    Fetch a property from the main mac-signing-buddy class.

    Parameters:
        property (str): The name of the property to fetch.

    Returns:
        The value of the property.
    """
    for line in open("mac_signing_buddy/__init__.py", "r").readlines():
        if not line.startswith(property):
            continue
        return line.split("=")[1].strip().strip('"')
    raise ValueError(f"Property {property} not found.")


def status_to_classifier(status: str) -> str:
    """
    Convert a status to a classifier.

    Parameters:
        status (str): The status to convert.

    Returns:
        The classifier.
    """
    statuses = [
        "Planning",
        "Pre-Alpha",
        "Alpha",
        "Beta",
        "Production/Stable",
        "Mature",
        "Inactive",
    ]

    if status not in statuses:
        raise ValueError(f"Status {status} not found.")

    return f"Development Status :: {statuses.index(status) + 1} - {status}"


setup(
    name="mac-signing-buddy",
    version=fetch_property("__version__:"),
    description=fetch_property("__description__:"),
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    author=fetch_property("__author__:"),
    author_email=fetch_property("__author_email__:"),
    license=fetch_property("__license__:"),
    url=fetch_property("__url__:"),
    python_requires=">=3.6",
    packages=find_packages(include=["mac_signing_buddy"]),
    package_data={
        "mac-signing-buddy": ["*"],
    },
    entry_points={
        "console_scripts": [
            "mac-signing-buddy = mac_signing_buddy.cli:main",
        ],
    },
    py_modules=["mac-signing-buddy"],
    include_package_data=True,
    # install_requires=open("requirements.txt", "r").readlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        status_to_classifier(fetch_property("__status__:")),
    ],
)