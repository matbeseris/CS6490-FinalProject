import socket
import ssl
from CipherSuites import *

# recieve messages from the client
def client_handler(ssl_sock):
    msg = ssl_sock.recv(2048)
    while msg:
        print("Recieved message: " + msg.decode("UTF-8"))
        ssl_client_wrapped.send(msg)
        msg = ssl_sock.recv(2048)


# my bluetooth adapter MAC address
bluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20 # any port that is available

bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

ssl_context = getSSLContext_server(DHERSA_AES256)

bsock.bind((bluetoothMAC, port))
bsock.listen(1)

print("Waiting for connection")

try:
    client, addr = bsock.accept()
    print("client connected")
    
    ssl_client_wrapped = ssl_context.wrap_socket(client, server_side=True)
    print("client socket wrapped in SSL with ciphers: " + 
        str(ssl_client_wrapped.cipher()))
    
    client_handler(ssl_client_wrapped)
except:
    print("closing socket")
    if ssl_client_wrapped:
        ssl_client_wrapped.shutdown(socket.SHUT_RDWR)
        ssl_client_wrapped.close()
        
    bsock.close()
