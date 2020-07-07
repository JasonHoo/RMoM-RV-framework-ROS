from socketserver import BaseRequestHandler,ThreadingTCPServer
import threading
#import mmap
#import contextlib
import time
import socket



class Handler(BaseRequestHandler):
    def handle(self):
        print(self.client_address)
        while True:
            try:
                data_rv = (self.request.recv(1024)).decode(encoding='utf_8')
                if len(data_rv) == 0: break
                #print("RecieveData :=="+ str(data_rv)+">>>>> \n")
                sock.send(data_rv.encode(encoding='utf_8'))
            except Exception:
                break
        self.request.close()

  
       # while True:
       #     data_rv = self.request.recv(1024).decode(encoding='utf_8') #接收
        #    if len(data_rv)>0:
        #        print('receive=',data_rv)
        #        ##sock.sendall(data_rv.encode(encoding='utf_8'))
       #     else:
         #       sock.close()
          #      break
                
        



def link_main():
    
    HOST = '127.0.0.1'
    PORT = 65335
    ADDR = (HOST,PORT)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        alink = sock.connect(ADDR)
        print('initializing momery map...')
    except Exception as e:
        print ('error',e)
        sock.close()
        #sys.exit()

#def serverCreate():
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8896
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
    print('listening')
    #with open("test.dat", "w") as f:
    #    f.write('\x00' * 1024)
    #f.close()
    link_main()

    server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
