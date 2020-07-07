import random, sys, time


#list = []

wr = open('test15.txt','w+')#写入到文本中
    
for i in range(0,1000):
    #time.sleep(1)
    #for j in range(0,20):
        wrstr="T:"+str(i)+","
        wrstr+="ID:"+"15"+","
        wrstr+="tx:"+str(random.randint(0,100))+","
        wrstr+="ty:"+str(random.randint(0,100))+","
        wrstr+="tth:"+str(random.randint(1,20))+","
        wrstr+="vx:"+str(random.randint(0,100))+","
        wrstr+="vy:"+str(random.randint(0,100))+"\n"

        #print(list,"\n")
        wr.write(wrstr)
        
