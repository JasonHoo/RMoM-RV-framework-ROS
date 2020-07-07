# RMoM-RV-framework-ROS
RV framework for the swarming systems on ROS

# HOW TO USE
 Python_version > 3.7
 pip install mtl (Version 0.1.7 is recommended )
    >if cannot install, copy the \site-packages into $python_path\Lib\site-packages


 run ..\monitorServer-master\monitorServerMain.py
    >input the username and password, password: nudtuserhc
    >press server launch button
 
 run the clientMonitor.py on ROS environment of each robot node
 or run the testScripts on Windows for simulation 



# FAQ:

1. Error: "Tkinter" module cannont be found
   
    python3--->use "import Tkinter"
    python2--->use "import tkinter"
