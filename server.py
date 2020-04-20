import socket
import ssl
from CipherSuites import *

# my bluetooth adapter MAC address
bluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20 # any port that is available

######
# Recieve messages from the client and send them right back
######
def echoServer(bsock):
    msg = bsock.recv(2048)
    while msg:
        print("Recieved message: " + msg.decode("UTF-8"))
        bsock.send(msg)
        msg = bsock.recv(2048)
        
######
# Handle the interaction with the client
######
def clientHandler(bsock):
    echoServer(bsock)

######
# Start the bluetooth server socket and wait for a client to connect
# Wrap the connection in SSL and handle it
######
def startServer(mac, port):
    bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    ssl_context = getSSLContext_server(CipherSuites.DHERSA_AES256)

    bsock.bind((mac, port))
    bsock.listen(1)

    print("Waiting for connection")

    try:
        client, addr = bsock.accept()
        print("client connected")
    
        ssl_client_wrapped = ssl_context.wrap_socket(client, server_side=True)
        print("client socket wrapped in SSL with ciphers: " + 
            str(ssl_client_wrapped.cipher()))
    
        clientHandler(ssl_client_wrapped)
    except:
        print("closing socket")
        if ssl_client_wrapped:
            ssl_client_wrapped.shutdown(socket.SHUT_RDWR)
            ssl_client_wrapped.close()
        
        bsock.close()
        
if __name__ == "__main__":
    startServer(bluetoothMAC, port)
