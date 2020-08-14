# import tkinter module 

import tkinter
from tkinter import messagebox
from tkinter import *

from socketserver import BaseRequestHandler,ThreadingTCPServer
# import other necessery modules
import sys
import random 
import time 
import datetime
import mtl
import threading
import socket

#######################################################
# creat global flags
lastdata = ""
monRunIF = 0           #开始监控标识位
linkOK = 0             #取得链接标识位
timeUnify = 0          #服务器监控器-外时统
timeUniInner = {}      #分布式监控器-内时统
verdictRet = "Uncertain"       #判定结果
# creat a global monitorFrame data as a dict
dataDict = {}
atompDict = {}
specificDict = {}
# config parameters
bot_num = 0
#######################################################

if __name__ == "__main__":


        # creating root object 
        root = Tk()

        # defining size of window 
        root.geometry("1100x1600")

        # setting up the title of window 
        root.title("Runtime Monitoring for Robotics")

        Tops = Frame(root, width = 1100, height = 600, relief = SUNKEN)
        Tops.pack(side = TOP)

        lblCanvas = Canvas(root, bg='LightSeaGreen', height=82, width=2000)

        lblphoto = PhotoImage(file='nudt4bg.png')

        image = lblCanvas.create_image(550, 3, anchor='n', image=lblphoto)

        lblCanvas.pack()

        f0 = Frame(root, width = 1100, height = 5,
							relief = SUNKEN)
        f0.pack()

        f1 = Frame(root, width = 1100, height = 300,
							relief = SUNKEN) 
        f1.place(x = 40, y = 350)

        f00 = Frame(root, width = 1100, height = 5,
							relief = SUNKEN)
        f00.pack()

        f2 = Frame(root, width = 1100, height = 300,
							relief = SUNKEN)
        f2.place(x = 200, y = 650)


        # =================================================================== 
        #				 TIME 
        # =================================================================== 
        localtime = time.asctime(time.localtime(time.time())) 

        lblInfo = Label(Tops, font = ('helvetica', 50, 'bold'), 
		text = "RUNTIME MONITOR @ \n ROS robotic system",
					fg = "Black", bd = 10, anchor='w') 
					
        lblInfo.grid(row = 0, column = 0)

        lblInfo = Label(Tops, font=('arial', 20, 'bold'),
			text = localtime, fg = "Steel Blue", 
						bd = 10, anchor = 'w') 
						
        lblInfo.grid(row = 1, column = 0)



        Rand = StringVar() 
        Token = StringVar() 
        Key = StringVar()
        IP = StringVar()
        Result = StringVar() 



        def check_pass(username, password):
            with open('userfile.txt', 'r+') as f:
                content = f.readlines()
            for i in content:
                if i.split(',')[0].strip() == username and i.split(',')[1].strip().strip('\n') == password:
                    return True
                    break
            else:
                return False

        # exit function 
        def qExit(): 
                root.destroy() 

        # Function to reset the window 
        def Launch_Serv():

                login = check_pass(Rand.get(),Key.get())
                if login == True:
                        t1 = threading.Thread(target=Recieve_serv,args=())
                        t1.start()

                        messagebox.showinfo(title='GUIDANCE', message='MonitorServer has been launched. When you are ready to start the client monitors, click the >>>Run Monitor<<< button.')
                else:
                        messagebox.showerror('LOGIN ERROR','Incorrect user name or password!')

                

        #def Launch_Thread():
        #        #variables = {} #add a variable with witch execfile can return
        #        exec(open("serverLaunch.py", encoding = 'utf-8').read())

                
        # reference 
        lblReference = Label(f1, font = ('arial', 16, 'bold'), 
				text = "UserID:", bd = 16, anchor = "w") 
				
        lblReference.grid(row = 0, column = 0) 

        txtReference = Entry(f1, font = ('arial', 16, 'bold'), 
			textvariable = Rand, bd = 10, insertwidth = 4, 
						bg = "powder blue", justify = 'right') 
						
        txtReference.grid(row = 0, column = 1)


        txtReference.insert('insert','huchi16@nudt.edu.cn')              # 预设UserID值

        # labels 
        lblToken = Label(f1, font = ('arial', 16, 'bold'), 
		text = "TOKEN:", bd = 16, anchor = "w") 
		
        lblToken.grid(row = 1, column = 0) 

        txtToken = Entry(f1, font = ('arial', 16, 'bold'), 
		textvariable = Token, bd = 10, insertwidth = 4, 
				bg = "powder blue", justify = 'right') 
				
        txtToken.grid(row = 1, column = 1)

        txtToken.insert('insert','dVCTwXh9mP')              # 预设Token值

        lblkey = Label(f1, font = ('arial', 16, 'bold'), 
			text = "PASSWORD:", bd = 16, anchor = "w") 
			
        lblkey.grid(row = 2, column = 0) 

        txtkey = Entry(f1, font = ('arial', 16, 'bold'), 
		textvariable = Key, bd = 10, insertwidth = 4, 
				bg = "powder blue", justify = 'right',show="*") 
				
        txtkey.grid(row = 2, column = 1)

        txtkey.insert('insert', 'nudtuserhc')

        lblIP = Label(f1, font = ('arial', 16, 'bold'), 
		text = "DATA SOURCE:", bd = 16, anchor = "w") 
								
        lblIP.grid(row = 3, column = 0) 

        txtIP = Entry(f1, font = ('arial', 16, 'bold'), 
		textvariable = IP, bd = 10, insertwidth = 4,
				bg = "powder blue", justify = 'right') 
					
        txtIP.grid(row = 3, column = 1)

        txtIP.insert('insert', '192.168.3.173')

        lblService = Label(f1, font = ('arial', 16, 'bold'), 
			text = "SPECIFICATION:", bd = 16, anchor = "w")
			
        lblService.grid(row = 4, column = 0)

        txtService = Entry(f1, font = ('arial', 16, 'bold'), 
			textvariable = Result, bd = 10, insertwidth = 4, 
					bg = "powder blue", justify = 'right') 
						
        txtService.grid(row = 4, column = 1)

        txtService.insert('insert', "C:\\Users\Administrator\\PycharmProjects\\Versions\\RMoM-V1.3\\RMoM-RV-framework-ROS-master\\monitorServer-master\\Specification.txt")

        # display region

        lblverdict = Label(root, font = ('arial', 10, 'bold'), 
			text = "Monitor Display", bd = 16, anchor = "w")
        lblverdict.place(x = 580, y = 322)


        scroll = Scrollbar() # 创建滚动条

        initDispVar = StringVar()

        initDispVar.set(['    This tool is to address the challenge of specifying and monitoring',
                 ' the robotic property and swarm property at runtime.',
                 '    The monitoring scenarios is powered by the RMoM platform.',
                 '    ......',
                 '    ......',
                 '    Setting the parameters, then click the Run Monitor button......',
                 ' '])

        lbverdict = Listbox(root, listvariable=initDispVar, width='60', height='14') # 创建文本窗

        scroll.place(x = 1022, y = 366, height = '256')  # 将滚动条填充


        lbverdict.place(x = 600, y = 366, anchor = 'nw')

        scroll.config(command=lbverdict.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        lbverdict.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框

        txtdisp = ' This tool is built to address the challenge of specifying and monitoring the robotic property and swarm property at runtime.\n' \
      ' The monitoring scenarios is powered by the RMoM platform. \n' \
      ' ... ...\n' \
      ' \n' \
      ' Setting the parameters, then click the Run Monitor button. \n' \
      ' ... ...\n' 


        def ParseSpecs(ppath):
		global bot_num
                global specificDict
                with open(ppath,"rb") as load_f:
                        for line in load_f:
                                read = (line.decode(encoding='utf_8')).strip('\n')

                                ifnol = bool(re.search(':', read))
                                
                                if ifnol is True:
                                        keySpecific = (read[0: read.rfind(':', 1)]).replace("\n", "").strip()
                                        valueSpecific = read[read.rfind(':', 1) +1 : ].replace("\n", "").strip()
					
					#解析参数化保留字FORALL 和 EXISTS
                                        if bool(re.search('FORALL', valueSpecific)) is True:
                                                tmp_valueSpecific = valueSpecific.replace("FORALL","").strip()
                                                valueSpecific = ""
                                                for itor in range(0,bot_num):
                                                        valueSpecific = valueSpecific + tmp_valueSpecific.replace("_i",("_"+str(itor)))
                                                        if itor+1 != bot_num:
                                                                valueSpecific = valueSpecific + " and "
                                                                
                                        elif bool(re.search('EXISTS', valueSpecific)) is True:
                                                tmp_valueSpecific = valueSpecific.replace("EXISTS","").strip()
                                                valueSpecific = ""
                                                for itor in range(0,bot_num):
                                                        valueSpecific = valueSpecific + tmp_valueSpecific.replace("_i",("_"+str(itor)))
                                                        if itor+1 != bot_num:
                                                                valueSpecific = valueSpecific + " or "
					
                                        specificDict[keySpecific] = []
                                        specificDict[keySpecific] = valueSpecific
                print(specificDict)
    

        def Run_monitor():
                global monRunIF
                global timeUnify
                
                lbverdict.delete(0, END)
        
                lbverdict.insert(END, '等待链接...')
                
                monRunIF=1

                timeUnify = time.time()                    #从开始监控时刻，初始化外时统信号
                print("当前时统信号：" +str(timeUnify)+"\n")

                specpath = Result.get()
                ParseSpecs(specpath)

                t2 = threading.Thread(target=Verdict_calc,args=())
                t2.start()



        


        # Launch button 
        btnReset = Button(f2, padx = 16, pady = 8, bd = 16,
				fg = "black", font = ('arial', 16, 'bold'), 
					width = 10, text = "Launch Server", bg = "green", 
				command = Launch_Serv).grid(row = 5, column = 1, padx = 20, pady = 20)
        

        # Show message button
        btnMonitor = Button(f2, padx = 16, pady = 8, bd = 16,
                                fg = "black", font = ('arial', 16, 'bold'),
                                        width = 10, text = "Run Monitor", bg = "yellow",
				command = Run_monitor).grid(row = 5, column = 2, padx = 20, pady = 10)

       

        # Exit button
        btnExit = Button(f2, padx = 16, pady = 8, bd = 16,
				fg = "black", font = ('arial', 16, 'bold'), 
					width = 10, text = "Exit", bg = "red",
				command = qExit).grid(row = 5, column = 3, padx = 20, pady = 10)
        
        def ParseMTL(pdict):

                if len(atompDict[list(atompDict.keys())[0]])>0:  #判断原子命题字典中的第一个命题是否已经装入真值
                        phi = specificDict['phi']

                        phi_parse = mtl.parse(phi)
                
                        ret = str(phi_parse(pdict))
                else:
                        ret = "?"
                        
                #print(ret)

                return ret



        def extractAtomP(pDict):
                global atompDict
                subvar = []
                for keyAtom in specificDict:
                        if keyAtom != "phi":
                                atompDict[keyAtom] = []
                                find_obj = re.findall('Robot\d{1,3}\.[a-z]\w{1,4}',specificDict[keyAtom])
                                if find_obj:
                                        #for kd_num in range(0, len(find_obj)):
                                            #kd_str = find_obj[kd_num]
                                            #print(kd_str)
                                           
                                        evalstr = specificDict[keyAtom]
                                        set_obj = set(find_obj)
                                        set_list = list(set_obj)
                                        for i in range(0, len(set_list)):
                                            evalstr = evalstr.replace(set_list[i], "subvar["+ str(i) +"]")
                                        #print(evalstr)

                                        if set_obj.issubset( set(dataDict.keys()) ) is True:

                                            Taulist = []
        
                                            for i in range(0, len(set_list)):
                                                Taulist.append(len(dataDict[set_list[i]]))
                                                
                                            Taulist.sort()
                                            Tau = Taulist[0]-1
                                            
                                            for itime in range(0,Tau):
                                                    
                                                for kd_i in range(0, len(set_list)):
                                                    #print("\n")
                                                    #print("now itime = "+str(itime)+" , Tau = " +str(Tau))
                                                    #print("\n")
                                                    #print("and now kd_i = "+ str(kd_i)+"   , dataDict key = "+str(set_list[kd_i]))
                                                    #print("\n")
                                                    setturple = dataDict[set_list[kd_i]][itime]
                                                    listturple = list(setturple)                                                   
                                                    subvar.append(listturple[-1])
                                                    
                                                Tvalue = eval(evalstr)
                                                subvar = []
                                                Tturple = (itime, Tvalue)
                                                if keyAtom not in atompDict:
                                                        atompDict[keyAtom] = []
                                                        atompDict[keyAtom].append(Tturple)
                                                else:
                                                        atompDict[keyAtom].append(Tturple)

                                            
                                      #  else:
                                      #      print("Error: no dict !!!")
             
                #print(atompDict)         
                                

        def StoreDict(data):
                global dataDict
                global timeUniInner
                #data = data.strip("\r")
                prolist = data.rstrip("\r").split(",")

                tdlist = []
                kdlist = []

                #print(str(prolist)+"\n")

                for td in prolist:
                        td = td[td.rfind(':', 1) +1:]   # tdlist表示:后面的数字串
                        tdlist.append(td)
                
                for kd in prolist:
                        kd = kd[0: kd.rfind(':',1)]     # kdlist表示:前面的键值串
                        kdlist.append(kd)
                #print(kdlist)
                #print("\n")
                #print(tdlist)

                ######依据外时统计算每个监控器客户端的内时统，以修改当前时刻T值##########
                if tdlist[0] == "0":
                        timeNow = time.time()
                        timeUniInner_value = int(timeNow - timeUnify) #计算内时统信号
                        timeUniInner_key = "Robot"+ tdlist[1]
                        timeUniInner[timeUniInner_key] = timeUniInner_value
                        #print( timeUniInner)
                        tdlist[0] = str(timeUniInner_value)
                else:
                        tdlist[0] = str(timeUniInner["Robot"+ tdlist[1]] + int(tdlist[0]))


                #构造字典dataDict中的keyword
                #keylist = []
                for i in range(2,len(kdlist)):
                        keyname = "Robot"+ tdlist[1]+"."+ kdlist[i]
                        if keyname not in dataDict:
                                dataDict[keyname] = []
                        tup = (eval(tdlist[0]),eval(tdlist[i]))
                        dataDict[keyname].append(tup)
                        
                        #keylist.append(keyname)


                with open ('runtimeMon.dat', 'w') as f:     
                        f.write(str(dataDict))
                        f.write("\n")
                


                

        def Recieve_serv():

            HOST = IP.get()
            PORT = 8896
            ADDR = (HOST,PORT)
            server = ThreadingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
            print('Main----listening')
            server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程

        class Handler(BaseRequestHandler):
            def handle(self):
                global verdictRet
                global lastdata
                global linkOK
                while True:
                    data_rv = (self.request.recv(1024)).decode(encoding='utf_8') #从serverlaunch接收

                    #print("Main:Recieve == "+str(data_rv)+"  >>>>>>> %s \n" % len(data_rv))
                    
                    if lastdata != data_rv and len(data_rv)>0:

                    ##每从分布式监控器上收取一帧数据，就进行STEP.1-3的步骤###
                                        
                                #解析并存储到字典dataDict中--STEP.1
                                StoreDict(data_rv)
                                
                                lastdata = data_rv

                                if monRunIF==1 and linkOK == 0:
                                        lbverdict.insert(END, '已链接...正在接收监控数据...')
                                        linkOK = 1

                                
                                ####为解决计算性能问题，STEP.2-3步骤用单独线程Verdict_calc实现

                                #####读取判定解析，输出到界面###########################
                                                
                                if monRunIF==1:
                                        lbverdict.insert(END,verdictRet + " ==>[ " + data_rv + " ]")
                                        lbverdict.see(END)
        
                                
                        
        def Verdict_calc():
            global verdictRet
            while True:
                    if len(lastdata)!=0:

                        #使用数据字典更新原子命题真值--STEP.2
                        extractAtomP(dataDict)
                                        
                        #进行MTL性质规约公式结果判定--STEP.3
                        TrueRet = ParseMTL(atompDict)
                
                        if TrueRet == "1":
                                verdictRet = "True"
                        elif TrueRet == "0":
                                verdictRet = "False"
                        else:
                                verdictRet = "Uncertain"
                                                



        root.mainloop() # keeps window alive


