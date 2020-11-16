# Reporting bugs

If you encounter a bug, best is to create a [**GitHub issue**](https://github.com/fish-quant/segmentation/issues). This would allow other users to see 
reported bugs and proposed solutions. If possible, please provide the following information

1. **How** can the bug be produced?
2. Which **browser** and browser version are you using?
3. **Complete plugin log**. Can be obtained by clicking on the `i` next to the FISH-QUANT plugin. Please copy to a text file. This will also contain the version of the plugin and the used code
    
    ``` bash
    Loading plugin SegmentCellsNuclei_i862g1602770955978 (TAG=stable,  WORKSPACE=fq-segmentation)
    ENGINE_URL=http://127.0.0.1:9527/
    Setting up plugin.

    Plugin SegmentCellsNuclei initialized
    * plugin version: 0.1.11
    * segwrap version: 0.1.7
    * utils_cellpose location: c:\users\muellerf\miniconda3\envs\fq-segmentation\lib\site-packages\segwrap\utils_cellpose.py
    ```

4. **Console log**. The console log of the browser provides further details that can help for debugging. To acces the console log in **Chrome**:

      1. In the ImJoy app mouse-right-click.
      2. Select `Inspect`.
      3. This will open a new interface on the right size of your browser windows. Select the panel `Console` and copy the entire content, and paste it to a file.  

# Development team

* Florian Mueller. [Github](https://github.com/muellerflorian).
