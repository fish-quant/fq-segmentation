
## Documentation

Documentation is written with mkdocs using the readthedocs theme.

* [mkdocs website](https://www.mkdocs.org/)

# Installation

Install mkdocs:  `pip install mkdocs`

# Basic use

* Launch dev-server: `mkdocs serve`
* Building the site: `mkdocs build`
* Deploy to GitHub pages: `mkdocs gh-deploy`

    __Note__ if this does not work, force commit with `mkdocs gh-deploy --clean --force`

## Update imjoy manifest

After changes in ImJoy plugins, update the plugin manifest.

Install `node.js` with conda

``` bash
conda install -c conda-forge nodejs
```

Run this command in project root path

``` bash
node update_manifest.js
```
