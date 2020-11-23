
# Developer

Here we provide some information for developers who want to contribute to this repository. 

## Documentation
Documentation 

* is **written** with mkdocs using the readthedocs theme: [mkdocs website](https://www.mkdocs.org/)

* **Online documentation** is automatically build by [readthedocs.com](https://readthedocs.org/) from the GitHub repository.


### Local build

You can build the documentation locally, before pushing to GitHub:

Install mkdocs:  `pip install mkdocs`

__Basic use__:

* Launch dev-server: `mkdocs serve`
* Building the site: `mkdocs build`


## ImJoy plugins

### Update imjoy manifest

After changes in ImJoy plugins, update the plugin manifest.

Install `node.js` with conda

``` bash
conda install -c conda-forge nodejs
```

Run this command in project root path

``` bash
node update_manifest.js
```
