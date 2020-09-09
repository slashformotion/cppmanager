from setuptools import setup, find_packages

__version__ = "0.0.1"


setup(
    name="cppmanager",
    version=__version__,
    packages=find_packages(exclude="tests"),
    install_requires=["click"],
    extras_require={"develop": ["pytest"]},
    entry_points={
        "console_scripts": [
            "custom_commands = cppmanager.cli:cli",
        ],
    },
)
