import socket
import ssl
import os

from CipherSuites import *
from helpers import *

# Bluetooth server information
serverBluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20

print("PID: " + str(os.getpid()))

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

    # request a file
    print("Requesting mobydick.txt from the server")
    sendMessage(bytes("mobydick.txt", "UTF-8"), bsock)
    
    # get the file size from the server
    filesz = recvMessage(bsock)
    
    if ErrorMessages.isErrorMessage(filesz):
        print("Error message recieved: " + str(filesz))
        return
        
    filesz = int.from_bytes(filesz, byteorder="big")
    print("File size: " + str(filesz))
    
    sendMessage(b"ACK", bsock)

    try:
        # Open file for reading in binary
        with open("copy.txt", "wb+") as fileCopy:
            # receive all data from the file and write it to the copy
            bytesDownloaded = 0
            while bytesDownloaded < filesz:
                data = recvMessage(bsock)
            
                if ErrorMessages.isErrorMessage(data):
                    print("Error message recieved: " + str(data))
                    return
            
                fileCopy.write(data)
                bytesDownloaded += len(data)
                print("Downloaded: " + str(bytesDownloaded) + "/" + str(filesz))
                
                sendMessage(b"ACK", bsock)
    except (OSError, IOError):
        print("Error: problem writing to the file.")
        sendMessage(ErrorMessages.FILE_ERROR.value, bsock)
        return

    sendMessage(b"ACK", bsock)

    print("File recieved successfully")

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
    connectionHandler(serverBluetoothMAC, port, ServerModes.FILE_DOWNLOAD)
