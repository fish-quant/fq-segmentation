# General behavior
Here, we describe some general concepts that are shared by most plugins. 


## Recursive search for data
Some plugins will perform by default a recursive search for data, for other this is an option. 

A recursive search means simply that not only the provided folder will be searched for files fitting
the specified criteria, but also all subfolders. 

## Specify folder to save results
Several possibilities are provided to specify the folder to save the results of the different workflows. Here, the general options are described, if
a plugin deviates from this default behavior it will be described in the respective plugin. 

When asked to define a folder to save results, you can 

1. Directly define a **full path** where the results should be stored. If the folder doesn't exist, it will be created. 
2. Define a folder with a **text replacement**. This option can be useful if many folders are processed, e.g. when a recursive search is performed.
     
    * Such a replacement operation is indicated with a string in the format  `str_orig>>str_new`,
      where 'str_orig' is the orginal string, 'str_new' is the new string.
      
    * For instance, using the string `acquisition>>analysis` implies that in the folder name
      `D:\example_data\acquisition`,  `acquisition` will be replaced with `analysis`, yielding 
      `D:\example_data\analysis`. 