import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cellpose",
    version="0.0.1.0",
    author="Florian MUELLER",
    author_email="muellerf.research@gmail.com",
    description="wrapper package for cellpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ['numpy<1.17.0', 'tqdm', 'scikit-image', 
                        'matplotlib','jupyter', 'ipywidgets'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
