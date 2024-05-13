from socket import *
try:
    s=socket(AF_INET,SOCK_STREAM)
    Host= "127.0.0.1" #sever IP
    Port= 8000          #server port 

    
    s.connect((Host,Port)) #Actively starts the TCP server connection
    while True:
       
        s.send(input("Client: ").encode())
        x=s.recv(2048)
        print("Server: "+x.decode())
        
        s.close()

except error as e:
    print(e)