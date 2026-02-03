from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("automation_cli/__init__.py", "r", encoding="utf-8") as fh:
    version = fh.read().split("=")[-1].strip().strip('"')

setup(
    name="simple-automation-cli",
    version=version,
    author="Mohamed Abdelwahab",
    author_email="mohamed@example.com",
    description="Simple Automation CLI for data engineering tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MohamedAbdelwahab24/simple-automation-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "automation-cli=automation_cli.cli:main",
        ],
    },
)
