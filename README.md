# RMoM-RV-framework-ROS
RV framework for the swarming systems on ROS. The related work is published on IEEE Trans on R. 

*cite::* Hu, Chi, et al. "Runtime Verification on Hierarchical Properties of ROS-Based Robot Swarms." IEEE Transactions on Reliability (2019).

# HOW TO USE

 Python_version > 3.7
 
    -pip install metric-temporal-logic==0.1.7 (Version 0.1.7 is recommended)


 ### Step one
 run ..\monitorServer-master\monitorServerMain.py
 
    -input the username and password, password: nudtuserhc
    -press server launch button
 ### step two
 
 run the clientMonitor 
 
    -run the clientMonitor.py on ROS environment of each robot node
    -(or) run the testScripts on Windows for simulation 



# FAQ:

1. Error: "Tkinter" module cannont be found
   
    python3--->use "import Tkinter"
    python2--->use "import tkinter"
