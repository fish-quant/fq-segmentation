# Overview

[ImJoy](https://imjoy.io/docs/#/) is image processing platform with an easy to use interface running in your browser.  

* While ImJoy is a browser app, **NO** user data will be transferred over the internet. 
* For best stability, we recommend using [**Chrome**](https://www.google.com/chrome/) to run the ImJoy app.  
* Some of its main **features** are:

    1. Specific functionality is provided by **plugins**, which can be installed with simple links. Available 
        plugins are listed in the plugin list on the left part of the interface. Plugins using Python require a Plugin engine to be executed. Installation and usasage is detailed below.  

    2. ImJoy can have several **workspaces**. Each workspace can contain multiple plugins and is 
        dedicated to a specific data processing task. Workspaces can be selected from little puzzle 
        symbol in the upper left part of the interface.

![imjoy-interface](img/imjoy-interface.png)

## Running Python plugins

Most of the provided plugins use Python for data processing. To use these plugins, 
you have to connect ImJoy to a Plugin engine. For this repository, we use **Jupyter notebooks** as 
and engine, which can be installed via Miniconda (see [**installation instructions**](#install-jupyter-engine-for-imjoy)). 

## Installing plugins

We provide links to install ImJoy plugins for the different workflows. 

If you press on the installation link, the ImJoy app will open and display a
dialog asking if you want to install the specified plugin. To confirm, press 
the `install` button.

![imjoy-plugin-installation](img/imjoy-plugin-installation.png){: style="width:400px"}

These installation links also specify in which [ImJoy workspaces](imjoy-overview.md#opening-a-workspace) the plugin will be installed. 

## Opening a workspace

Once a plugin is installed, ImJoy remembers the workspaces and plugins it contains. 

If you want to redo an analysis, you simply have to open the [ImJoy app](https://imjoy.io/#/app) 
and select the workspace `fq-segmentation` for this package.

If **updates** for the installed plugins 
are available, you will see a corresponding symbol next to the plugin name.

![imjoy-workspacer.gif](img/imjoy-workspace.gif){: style="width:500px"}
