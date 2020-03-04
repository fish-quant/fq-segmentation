# Tools
Here, we describe the different software packages that are used. We provide for all analysis workflows
dedicated **ImJoy plugins**, to faciliate their use. 

We also provide Python source code illustrating the basic usage in the folder `workflows`.

For installation instruction, please consult the dedicated [**section**](installation.md). 

A more detailed description of each workflow is provided in the dedicated sections. 


## Miniconda
The provided code is written in Python, and we recomend using
[Miniconda with Python 3.7](https://docs.conda.io/en/latest/miniconda.html)
for its execution. 

## ImJoy
[**ImJoy**](https://imjoy.io/docs/#/) is image processing platform with an easy
 to use interface. Some important features

 2. Specific functionality is provided by plugins, which can be installed with simple links. Available 
    plugins are listed in the plugin list on the left part of the interface. Depending on the implementation 
    plugins are either executed directly by pressing on their name, or a simple interface can be displayed when
    pressing on the arrow down symbol. 
 3. ImJoy can have several workspaces. Each workspace can contain multiple plugins and is often
    dedicated to a specific data processing task. Workspaces can be selected from little puzzle symbol in the upper left part of the interface.
 
    ![imjoy-interface](img/imjoy-interface.png)


### Installing plugins
We provide links to install the different ImJoy plugins. These installation links also specify
in which **ImJoy workspaces** the plugin will be installed. 

If you press on the installation link, the ImJoy web app will open and display a
dialog asking if you want to install the specified plugin. To confirm, press the `install` button.

![imjoy-interface](img/imjoy-interface.png)

Once installed, ImJoy remembers the workspaces and plugins and you simply have to
open the ImJoy app and select the workspace [https://imjoy.io/#/app](https://imjoy.io/#/app)

### Running Python plugins 
Some of the provided plugins use code written in Python. In order for ImJoy this code, it can connect 
to a **Jupyter notebook**, which can be installed via Miniconda.
    
Once you have the computational environment set up (see Installation), you start an Jupyter Notebook, 
to which ImJoy can connect: 

1. **Activate the environment**:
    ```
    conda activate cellpose
    ```
2. **Start Jupyter notebook**. Type
    ```
    jupyter notebook --NotebookApp.allow_origin='*' --no-browser
    ```
    Copy the provided URL including the token, something like `http://127.0.0.1:8889/?token=16126ce8b02ee35103200c46d71b3f946bfb408d1cae0f68`
3. In ImJoy, press on the rocket symbol in the upper right corner, select `Add Jupyter-Engine` 
    and past the URL from the step above. 
4. You can now connect your plugin to this Juypyter Kernel, by clicking on the puzzle symbol 
    next to the plugin name, and selecting the Juypyter Notebook as engine.  