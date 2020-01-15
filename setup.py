#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="presenzialo",
    version="0.1.2",
    description="presence web manager",
    long_description="presence web manager",
    author="so07",
    author_email="",
    maintainer="so07",
    url="https://github.com/so07/Presenzialo",
    download_url="",
    requires=["requests"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "presenzialo=presenzialo.presenzialo:main",
            "presenziamelo=presenzialo.presenzialo:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
)