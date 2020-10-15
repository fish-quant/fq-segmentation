"""
Setup script.
"""

import setuptools

# package version
VERSION = None
with open('segwrap/__init__.py', encoding='utf-8') as f:
    for row in f:
        if row.startswith('__version__'):
            VERSION = row.strip().split()[-1][1:-1]
            break

# package dependencies
with open("requirements.txt", encoding='utf-8') as f:
    REQUIREMENTS = [l.strip() for l in f.readlines() if l]

# setup
setuptools.setup(
    name="segwrap",
    version=VERSION,
    author="Florian MUELLER",
    author_email="muellerf.research@gmail.com",
    description="wrapper package for cellpose",
    url="https://github.com/fish-quant/segmentation",
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
