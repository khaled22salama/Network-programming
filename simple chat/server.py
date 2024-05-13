from socket import *
try:
    print("server is up and running")

    """""""""""""""" @socket_ref """"""""""""""""""""
    The family of protocols ised for transport mechanism like AF_INET, PF_INET, AF_UNIX
            AF_INET    IPv4
    
    Socket type:
            SOCK_STREAM     TCP
            SOCK_DGRAM      UDP
    
    """
    s= socket(AF_INET,SOCK_STREAM) #socket_ref

    Host="127.0.0.1"  #use local network
    Port= 8000 # 0 - 1023 reserved and has own permission

    """""""""""""""" @bind_ref """"""""""""""""""""
    Binds address to the socket. The address contains the two tuple of hostname (IP add.) in string format and the port number,
     so that it can listen to incoming requests on that IP and port
    """
    s.bind((Host,Port))  #@bind_ref

    s.listen() # Puts the server into listening mode to allow the server to listen to incoming connections.

   

   

    while True:
        conn,addr=s.accept() #Passively accepts the client connection and blocks until the connection arrives (initiates a session with the client)
            #conn = session ID
            #addr = Client address (address, Port number)
        print("connection from",addr[1])
        x=conn.recv(2048) # Receives the TCP message.
            #2048 is number of bytes of data 

        print("client : ", x.decode())

        conn.send(input("server: ").encode())

        conn.close()

except error as e:
    print(e)



