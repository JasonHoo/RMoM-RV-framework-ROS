1. 在ROS下安装micros_swarm_framework库包，非常简单，直接在ROS wiki下搜索即可 （indigo，kinetic版本均可）


2. 然后直接将client程序放在目录/home/xxx(你的路径)/catkin_ws/src/micros_swarm_framework-master/applications/app3（或者app1，app2）/src 
（我一般放这个位置，但是其实linux下面任何位置都可以的）

3. 启动micros_swarm_framework的 launch文件，stage或者gazebo的都可以的，跑起来之后ROS上的node节点和topic就启动起来了，下一步就是启动我们的客户端监控器

4. 在程序路径下执行 
   python monitorClient.py 4   
   传入的这个参数表示你要监控的机器人的ID，默认的例子是
