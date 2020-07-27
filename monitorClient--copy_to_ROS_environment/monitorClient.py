# -*- coding: utf-8 -*

from Tkinter import *
from nav_msgs.msg import Odometry
import os, time, glob, socket, sys, rospy, threading, re
from sys import argv
from subprocess import call


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

BUFSIZE = 1024
COUNT = 0
ROBOTID = 0
last_worktime=0
last_idletime=0
COMD_off = 0
timeQue = 0

multithread=False
if multithread==True:
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool

######################################################################################    


def update_display_bottom():
    
    listbox.see(END)


def update_display_top():
    
    listbox.see(0)
########################################################################################


def send_data(pdata):
    global timeQue
    timeQue = time.time()
    
    if len(pdata)>0:
        sock.send(pdata.encode(encoding='utf_8'))
        print("sendata : ===>" + pdata)    
    #else:
        #sock.close()

    #return


########################################################################################


def callback(data):
    global COUNT
    global COMD_off
    global timeQue
    #rospy.loginfo("I heard %s",data.pose.pose.position.x)
    #rospy.loginfo("I heard %s",data.twist.twist.linear.x)

    disk = disk_use()/100
    mem = mem_use()/100
    cpua = cpu_use()/100
    
    if COMD_off == 0 and os.path.exists("screenlog.0"):
    	with open('screenlog.0',"rb") as load_f:
	    for line in load_f:
		read = (line.decode(encoding='utf_8')).strip('\n')
		ifnol = bool(re.search('kill',read))

		if ifnol is True:
			COMD_off = 1
		else:
			continue
        load_f.close()


    datasend = "T:"+str(COUNT)+","+"ID:"+str(ROBOTID)+","+"tx:"+str(data.pose.pose.position.x)+","+"ty:"+str(data.pose.pose.position.y)+","+"vx:"+str(data.twist.twist.linear.x)+","+"vy:"+str(data.twist.twist.linear.y)+","+"cpu:"+str(cpua)+","+"mem:"+str(mem)+","+"comd:"+str(COMD_off)

    timeNow = time.time()
    if timeNow-timeQue > 1:
    	rospy.loginfo(datasend)
    	listbox.insert(END,datasend)
    	listbox.see(END)
    	send_data(datasend)
    	COUNT += 1

##########################################################################################

def listener():

    global ROBOTID
    ROBOTID = sys.argv[1]

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/robot_"+str(ROBOTID)+"/odom", Odometry, callback)
    #time.sleep(1)
    #spin() #simply keeps python from exiting until this node is stopped
    #rospy.spinOnce()

############################################################################################   



########################################################################################
def get_mem_usage_percent():
    try:
        f = open('/proc/meminfo', 'r')
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemFree:'):
                mem_free = int(line.split()[1])
            elif line.startswith('Buffers:'):
                mem_buffer = int(line.split()[1])
            elif line.startswith('Cached:'):
                mem_cache = int(line.split()[1])
            elif line.startswith('SwapTotal:'):
                vmem_total = int(line.split()[1])
            elif line.startswith('SwapFree:'):
                vmem_free = int(line.split()[1])
            else:
                continue
        f.close()
    except:
        return None
    physical_percent = usage_percent(mem_total - (mem_free + mem_buffer + mem_cache), mem_total)
    virtual_percent = 0
    if vmem_total > 0:
        virtual_percent = usage_percent((vmem_total - vmem_free), vmem_total)
    return physical_percent, virtual_percent
 
def usage_percent(use, total):
    try:
        ret = (float(use) / total) * 100
    except ZeroDivisionError:
        raise Exception("ERROR - zero division error")
    return ret
 
def disk_use():
    statvfs = os.statvfs('/')
    total_disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_disk_space = statvfs.f_frsize * statvfs.f_bfree
    disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
#    disk_tip = "硬盘空间使用率："+str(disk_usage)+"%"
#    print(disk_tip)
    return disk_usage
 
def mem_use():
    mem_usage = get_mem_usage_percent()
    mem_usage = mem_usage[0]
#    mem_tip = "物理内存使用率："+str(mem_usage)+"%"
#    print(mem_tip)
    return mem_usage
    
def cpu_use():
    global last_worktime, last_idletime
    f=open("/proc/stat","r")
    line=""
    while not "cpu " in line: line=f.readline()
    f.close()
    spl=line.split(" ")
    worktime=int(spl[2])+int(spl[3])+int(spl[4])
    idletime=int(spl[5])
    dworktime=(worktime-last_worktime)
    didletime=(idletime-last_idletime)
    rate=float(dworktime)/(didletime+dworktime+0.001)
    cpu_t = rate*100
    last_worktime=worktime
    last_idletime=idletime
    if(last_worktime==0): return 0
#    cpu_tip = "CPU使用率："+str(cpu_t)+"%"
#    print(cpu_tip)
    return cpu_t
########################################################################################

if __name__ == "__main__":


    root = Tk()
    root.title('moniotr client')
    root.geometry('500x500')
    #root.grid_rowconfigure(0, weight = 1)
    #root.grid_columnconfigure(0, weight = 1)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    listbox=Listbox(root,selectmode=MULTIPLE,yscrollcommand=scrollbar.set)
    listbox.configure(exportselection=False)
    
    destination='/media/cgarling/SS'
    external_source='/media/cgarling/My Passport'
    all_dirs=glob.glob(external_source+'/*/*/')

    times1=[]
    times2=[]
    for i in range(len(all_dirs)):
        times1.append(os.path.getmtime(all_dirs[i]))
        times2.append(time.ctime(times1[i]))
        all_dirs[i]=all_dirs[i][len(external_source)+1:-1]

    for i in range(len(all_dirs)):
        #Checkbutton(root,text=all_dirs[i],variable=a[all_dirs[i]]).grid(row=i+1,sticky=W)
        listbox.insert(i,all_dirs[i])
        if os.path.isdir(destination+'/'+all_dirs[i]):listbox.selection_set(i)

    listbox.pack(side=LEFT,fill=BOTH,expand=1)

    v1=IntVar()
    v1.set(1)
    Radiobutton(root, text="Flip to top", variable=v1,value=1,indicatoron=0, command=lambda: update_display_top()).pack(fill=X)
    Radiobutton(root, text="Turn to bottom", variable=v1,value=2,indicatoron=0, command=lambda: update_display_bottom()).pack(fill=X)

    v2=IntVar()
    v2.set(1)
    Checkbutton(root,text="Is-encode?",variable=v2,onvalue=1,offvalue=0).pack(fill=X)

    v3=IntVar()
    v3.set(1)
    Radiobutton(root, text="VBR", variable=v3, value=1,indicatoron=0).pack(fill=X)
    Radiobutton(root, text="CBR", variable=v3, value=2,indicatoron=0).pack(fill=X)

    v4=StringVar()
    v4.set('192.168.3.173')
    e=Entry(root,textvariable=v4)
    e.pack(fill=X)

###########connect the server , prepare to send monitoring data#####################
    ADDR =(v4.get(),8896)
    print(ADDR)

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        a = sock.connect(ADDR)
    except Exception as e:
        print ('error',e)
        sock.close()
        sys.exit()

    print ('have connected with server')     
#####################################################################################

    Button(root,text="Submit Mornitoring Data ",command=lambda: listener()).pack(fill=X)

    scrollbar.config(command=listbox.yview)

    #t = threading.Thread(target=listener)
    #t.start()

    root.mainloop()
#print listbox.get(listbox.curselection())

