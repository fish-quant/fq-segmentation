
# Installation
In order to use the workflows in this repository, you need to follows these steps, which we detail below: 

1. **Python**. Recommended with Miniconda:
0. Create a **dedicated environment** with Jupyter to run your code.
1. Install **CellPose**.
2. Install **code from this repositry**.  
   
## Pyton with Miniconda
We recommend installing an [Miniconda distribution of Python](https://docs.conda.io/en/latest/miniconda.html): choose Python 3.7 and your operating system. 

We then recommend using the annoconda prompt that is availabel to excecute the different commands listed below. 
This guarantees that the necessary terminal scripts are available. 

## Create dedicated environment to run Cellpose
We recommend creating a dedicated environment to run Cellpose. To create an environment called `cellpose`, open an anaconda prompt and type. Note that you will also install jupyter, which will allow 
to run the jupyter notebooks for easier execution (confirm with `y` when asked if you want to proceed): 

```
conda create --name cellpose python=3.7 jupyter
```

Then activate the `cellpose` environment (Note you will always have to run this command when using this workflow):
```
conda activate cellpose
```

## Installing Cellpose
From your `cellpose` environment, install Cellpose and its dependencies with
```
pip install cellpose --upgrade
```

## Installing this package
From your `cellpose` environment, install this package and its dependencies with
```
pip install git+https://github.com/muellerflorian/segmentation/ --upgrade
```
TODO: add commit tag?
