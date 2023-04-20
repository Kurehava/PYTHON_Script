# iPWS Tool
based iPWS Offical Tools

# Usgae
## -> script  run
1.```python/in/path/python -m pip install -r requirement.txt```
 or
 ```python -m pip install -r requirement.txt```
 
2.python iPWS_Tool.py

## -> package  .py
Try to exit the installation of the conda virtual environment. pandas' INTEL-specific linear library MKL will be installed in the conda virtual environment by default, which will increase the size of the package.

0.(select)```conda deactivate```

1.```python/in/path/python -m pip install -r requirement.txt```
or
 ```python -m pip install -r requirement.txt```
 
2.```python/in/path/python -m pip install pyinstaller```
or
 ```python -m pip install pyinstaller```
 
 3.```pyinstaller iPWS_Tool.py```
 
 4.Insert ```'import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)'``` in the second line of ```iPWS_Tool.spec``` file
 
 5.```pyinstaller iPWS_Tool.spec```

 6.Remove the packed iPWS_Tool from the dist folder, then delete ```dist, build, iPWS_Tool.spec```

