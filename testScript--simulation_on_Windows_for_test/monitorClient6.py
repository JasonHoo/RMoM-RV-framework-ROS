from tkinter import *
import os, time, glob, socket, sys
from subprocess import call

HOST = '127.0.0.1'
PORT = 8896
ADDR =(HOST,PORT)
BUFSIZE = 1024

multithread=False
if multithread==True:
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool

######################################################################################    


def update_display(times1,times2,all_dirs,destination):
    
    return listbox,times1,times2,all_dirs


########################################################################################

def send_data():
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        a = sock.connect(ADDR)
    except Exception as e:
        print ('error',e)
        sock.close()
        sys.exit()

    print ('have connected with server')

    
    with open('test6.txt','rb') as rbfile:
    
        for line in rbfile:
            time.sleep(1)
            data = (line.decode(encoding='utf_8')).strip('\n')
            if len(data)>0:
                print ('send:',data)
                sock.send(data.encode(encoding='utf_8'))
                #recv_data = sock.recv(BUFSIZE)
                #print ('receive::',recv_data.decode(encoding='utf_8'))
            else:
                sock.close()
                break

    return



########################################################################################


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
Radiobutton(root, text="Sortby BotID", variable=v1, value=1,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)
Radiobutton(root, text="Sortby Time-seq", variable=v1, value=2,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)

v2=IntVar()
v2.set(1)
Checkbutton(root,text="Is-encode?",variable=v2,onvalue=1,offvalue=0).pack(fill=X)

v3=IntVar()
v3.set(1)
Radiobutton(root, text="VBR", variable=v3, value=1,indicatoron=0).pack(fill=X)
Radiobutton(root, text="CBR", variable=v3, value=2,indicatoron=0).pack(fill=X)

v4=StringVar()
v4.set('2')
e=Entry(root,textvariable=v4)
e.pack(fill=X)

Button(root,text="Submit Mornitoring Data ",command=lambda: send_data()).pack(fill=X)

scrollbar.config(command=listbox.yview)
root.mainloop()
#print listbox.get(listbox.curselection())

