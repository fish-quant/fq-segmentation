# Jupyter
!!! warning
    We recommend using these Jupyter notebooks only for more experienced users, e.g. for users who  want to integrate these workflows in other projects, or further improve them. 

We provide for all workflows available as ImJoy plugins, also corresponding Juypyter notebooks in the folder `notebooks`. We refer to many of the excellent online resources for how to work with Jupyter notebooks.


## Create environment
To run this code, we recommend installing an [Miniconda distribution of Python](https://docs.conda.io/en/latest/miniconda.html): choose Python 3.7 and your operating system. You  can then use the annoconda prompt to excecute the different commands listed below. 

We further recommend creating a **dedicated environment** to run code in this analysis package. This guarantess that only necessary code is installed. 

To create an environment called `fq-segmentation`, open an anaconda prompt and type (Confirm with `y` when asked if you want to proceed (`Proceed ([y]/n)?`): 

```
conda create --name fq-segmentation python=3.7
```

**Activate the environment**:
```
conda activate fq-segmentation
```

## Use package

First, install the code

```
pip install git+https://github.com/fish-quant/segmentation --upgrade
```

Then you can open a jupyter notebook for a paricular workflow. 

