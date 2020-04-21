import socket
import ssl
from CipherSuites import *
from helpers import *

# Bluetooth server information
serverBluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20

#####
# Create a Bluetooth socket and wrap in an SSL connection
#####
def connectBluetoothServerSSL(mac, port):
    ssl_bsock_wrapped = None
    bsock = None
    
    try:
        bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    except socket.error as emsg:
        print("Error creating socket ({0}): {1}".format(emsg.errno, emsg.strerror))
        return None

    try:
        ssl_context = getSSLContext_client()
        ssl_bsock_wrapped = ssl_context.wrap_socket(bsock, server_hostname=serverBluetoothMAC)
    except ssl.SSLError as emsg:
        print("Error wrapping socket with ssl ({0}): {1}".format(emsg.errno, emsg.strerror))
        return None

    try:
        ssl_bsock_wrapped.connect((mac, port))
        return ssl_bsock_wrapped
    except ssl.SSLError as emsg:
        print("Error conencting to server ({0}): {1}".format(emsg.errno, emsg.strerror))
        return None

######
# Send user input to server who will echo the message back
######
def echoServer(bsock):
    sendMessage(ServerModes.ECHO.value, bsock)
    ack = recvMessage(bsock)

    if ack != b"ACK":
        return -1

    while 1:
        sendmsg = input("Message to send: ")
        if sendmsg == "q":
            break
        sendMessage(bytes(sendmsg, "UTF-8"), bsock)

        recvmsg = recvMessage(bsock)
        if recvmsg:
            print("Recieved msg: " + recvmsg.decode("UTF-8"))

    return 1

######
# Download a file from the server
######
def downloadFile(bsock):
    sendMessage(ServerModes.FILE_DOWNLOAD.value, bsock)
    ack = recvMessage(bsock)

    if ack != b"ACK":
        return -1

    ##### NEED A FILE NAME INSERTED HERE ################
    sendMessage(bytes("", "UTF-8"), bsock)

    try:
        # Open file for reading in binary
        with open("copy.txt", "wb+") as fileCopy:
        # read all data from the file and send it
            data = recvMessage(bsock)
            
            if ErrorMessages.isErrorMessage(fileName):
                print("Error message recieved: " + str(fileName))
                return
            
            fileCopy.write(data)
    except (OSError, IOError):
        print("Error: problem writing to the file.")
        sendMessage(ErrorMessages.FILE_ERROR.value, bsock)
        return

    sendMessage(b"ACK", bsock)

    print("File recieved successfullyrecvMessage")

######
# Handle the Bluetooth connection
######
def connectionHandler(mac, port, mode):
    ssl_bsock = connectBluetoothServerSSL(mac, port)
    
    if not ssl_bsock:
        return -1

    print("Connected to Bluetooth server")

    if mode == ServerModes.ECHO:
        echoServer(ssl_bsock)
    elif mode == ServerModes.FILE_DOWNLOAD:
        downloadFile(ssl_bsock)

    ssl_bsock.close()
    
if __name__ == "__main__":
    connectionHandler(serverBluetoothMAC, port, ServerModes.ECHO)
