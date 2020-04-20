import socket
import ssl
from CipherSuites import *

# Bluetooth server information
serverBluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20

#####
# Create a Bluetooth socket and wrap in an SSL connection
#####
def connectBluetoothServerSSL(mac, port):
    bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    ssl_context = getSSLContext_client()
    ssl_bsock_wrapped = ssl_context.wrap_socket(bsock, server_hostname=serverBluetoothMAC)

    ssl_bsock_wrapped.connect((mac, port))
    return ssl_bsock_wrapped

######
# Send user input to server who will echo the message back
######
def echoServer(bsock):
    while 1:
        sendmsg = input("Message to send: ")
        if sendmsg == "q":
            break
        bsock.send(bytes(sendmsg, "UTF-8"))

        recvmsg = bsock.recv(2048)
        if recvmsg:
            print("Recieved msg: " + recvmsg.decode("UTF-8"))
    return

######
# Handle the Bluetooth connection
######
def connectionHandler(mac, port):
    ssl_bsock = connectBluetoothServerSSL(mac, port)
    
    if not ssl_bsock:
        print("error connecting to server")
        return -1
    print("Connected to Bluetooth server")

    echoServer(ssl_bsock)

    ssl_bsock.close()
    
if __name__ == "__main__":
    connectionHandler(serverBluetoothMAC, port)

