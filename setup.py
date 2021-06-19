# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup

version = ""
with open("funfetch/__init__.py", encoding="UTF8") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

requirements = []
with open(f"{path}/requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

if not version:
    raise RuntimeError("version is not defined")

readme = ""
with open(f"{path}/README.md", encoding="UTF8") as f:
    readme = f.read()

setup(
    name="funfetch",
    author="decave27",
    author_email="decave27@gmail.com",
    url="https://github.com/decave27/funfetch",
    project_urls={
        "Source": "https://github.com/decave27/funfetch",
        "Tracker": "https://github.com/decave27/funfetch/issues",
    },
    version=version,
    keywords=["aiohttp", "ipc", "request", "fetch"],
    packages=find_packages(),
    license="MIT",
    description="Remote execution of a simple function on the server",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
