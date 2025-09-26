"""
Setup script for ClipGenius
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh.readlines() if line.strip() and not line.startswith("#")]

setup(
    name="clipgenius",
    version="1.0.0",
    author="ClipGenius Team",
    author_email="team@clipgenius.com",
    description="AI-powered command-line tool for downloading videos from YouTube and other platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexusa404-creator/Vidyne",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "clipgenius=clipgenius.cli:main",
        ],
    },
    include_package_data=True,
)