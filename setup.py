import setuptools

setuptools.setup(
    name="segwrap",
    version="0.0.1.3",
    author="Florian MUELLER",
    author_email="muellerf.research@gmail.com",
    description="wrapper package for cellpose",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ['numpy < 1.17.0', 
                        'tqdm', 
                        'scikit-image', 
                        'cellpose == 0.0.1.25'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
