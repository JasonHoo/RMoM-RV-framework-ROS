from Tkinter import *
from nav_msgs.msg import Odometry
import os, time, glob, socket, sys, rospy, threading
from sys import argv
from subprocess import call

BUFSIZE = 1024
COUNT = 0
ROBOTID = 0

multithread=False
if multithread==True:
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool

######################################################################################    


def update_display(times1,times2,all_dirs,destination):
    
    return listbox,times1,times2,all_dirs


########################################################################################


def send_data(pdata):
    
    
    if len(pdata)>0:
        sock.send(pdata.encode(encoding='utf_8'))
        print("sendata : ===>" + pdata)    
    else:
        sock.close()

    #return


########################################################################################


def callback(data):
    global COUNT
    #rospy.loginfo("I heard %s",data.pose.pose.position.x)
    #rospy.loginfo("I heard %s",data.twist.twist.linear.x)
    datasend = "T:"+str(COUNT)+","+"ID:"+str(ROBOTID)+","+"tx:"+str(data.pose.pose.position.x)+","+"ty:"+str(data.pose.pose.position.y)+","+"vx:"+str(data.twist.twist.linear.x)+","+"vy:"+str(data.twist.twist.linear.y)
    rospy.loginfo(datasend)
    listbox.insert(END,datasend)
    listbox.see(END)
    send_data(datasend)
    time.sleep(1)
    COUNT += 1
    


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
    
    destination='/media/cgarling/SS/Music'
    external_source='/media/cgarling/My Passport/Music'
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
    Radiobutton(root, text="Sortby BotID",variable=v1,value=1,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)
    Radiobutton(root, text="Sortby Time-seq",variable=v1,value=2,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)

    v2=IntVar()
    v2.set(1)
    Checkbutton(root,text="Is-encode?",variable=v2,onvalue=1,offvalue=0).pack(fill=X)

    v3=IntVar()
    v3.set(1)
    Radiobutton(root, text="VBR", variable=v3, value=1,indicatoron=0).pack(fill=X)
    Radiobutton(root, text="CBR", variable=v3, value=2,indicatoron=0).pack(fill=X)

    v4=StringVar()
    v4.set('127.0.0.1')
    e=Entry(root,textvariable=v4)
    e.pack(fill=X)
##########################################################################################

    def listener():
    	global ROBOTID
    	ROBOTID = sys.argv[1]

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

    	rospy.init_node('listener', anonymous=True)
    	rospy.Subscriber("/robot_"+str(ROBOTID)+"/odom", Odometry, callback)
    	#time.sleep(1)
    	# spin() simply keeps python from exiting until this node is stopped
    	rospy.spinOnce()

############################################################################################

    Button(root,text="Submit Mornitoring Data ",command=lambda: listener()).pack(fill=X)

    scrollbar.config(command=listbox.yview)

    #t = threading.Thread(target=listener)
    #t.start()
    root.mainloop()
#print listbox.get(listbox.curselection())

