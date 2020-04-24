import socket
import ssl
import os

from CipherSuites import *
from helpers import *

# my bluetooth adapter MAC address
bluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20 # any port that is available

print("PID: " + str(os.getpid()))

######
# Create a Bluetooth server at the MAC, port and return the listening socket
######
def createServer(mac, port):
    try:
        bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        bsock.bind((mac, port))
        bsock.listen(1)
        return bsock
    except socket.error as emsg:
        print("Error creating socket ({0}): {1}".format(emsg.errno, emsg.strerror))
        return None

######
# Recieve messages from the client and send them right back
######
def echoServer(bsock):
    sendMessage(b"ACK", bsock)

    msg = recvMessage(bsock)
    while msg:
        print("Recieved message: " + msg.decode("UTF-8"))
        sendMessage(msg, bsock)
        msg = recvMessage(bsock)

######
# Send a file to the client
######
def sendFile(bsock):
    sendMessage(b"ACK", bsock)

    fileName = recvMessage(bsock)

    if ErrorMessages.isErrorMessage(fileName):
        print("Error message recieved: " + str(fileName))
        return

    fileName = fileName.decode("UTF-8")
    print("Attempting to send " + fileName)
    
    try:
        # Open file for reading in binary
        with open(fileName, "rb") as fileData:
            # read all data from the file and send it
            #data = fileData.read()
            fileData.seek(0, os.SEEK_END)
            filesz = fileData.tell().to_bytes(64, byteorder="big")
            # send length of file so client know what to expect
            sendMessage(filesz, bsock)
            fileData.seek(0)
            
            # get ACK from client
            ack = recvMessage(bsock)

            if ErrorMessages.isErrorMessage(ack):
                print("Error message recieved: " + str(ack))
                return
            elif ack != b"ACK":
                print("Error ACK not recieved: " + str(ack))
                return

            data = fileData.read((2**16)-1)
            while data != b"":
                sendMessage(data, bsock)

                # get ACK from client
                ack = recvMessage(bsock)

                if ErrorMessages.isErrorMessage(ack):
                    print("Error message recieved: " + str(ack))
                    return
                elif ack != b"ACK":
                    print("Error ACK not recieved: " + str(ack))
                    return

                data = fileData.read((2**16)-1)

    except (OSError, IOError) as emsg:
        print("Error: problem reading from file ({0}): {1}".format(emsg.errno, emsg.strerror))
        sendMessage(ErrorMessages.FILE_ERROR.value, bsock)
        return

    ack = recvMessage(bsock)

    if ErrorMessages.isErrorMessage(ack):
        print("Error message recieved: " + str(ack))
        return
    elif ack != b"ACK":
        print("Error ACK not recieved: " + str(ack))
        return

    print("File sent successfully")
        
######
# Handle the interaction with the client
######
def clientHandler(bsock):
    mode = recvMessage(bsock)
    if mode == ServerModes.ECHO.value:
        echoServer(bsock)
    elif mode == ServerModes.FILE_DOWNLOAD.value:
        sendFile(bsock)


######
# Start the bluetooth server socket and wait for a client to connect
# Wrap the connection in SSL and handle it
######
def startServer(mac, port, ciphers):
    # create an SSL context for the selected cipher along with a bluetooth socket server
    ssl_context = getSSLContext_server(ciphers)
    bsock = createServer(mac, port)

    if not bsock:
        return -1
    
    print("Waiting for connection")

    try:
        client, addr = bsock.accept()
        print("client connected")
    
        ssl_client_wrapped = ssl_context.wrap_socket(client, server_side=True)
        print("client socket wrapped in SSL with ciphers: " + 
            str(ssl_client_wrapped.cipher()))
    
        clientHandler(ssl_client_wrapped)
    except (socket.error, ssl.SSLError) as emsg:
        print("Error communicating with client ({0}): {1}".format(emsg.errno, emsg.strerror))
        print("Closing socket")
        if ssl_client_wrapped:
            ssl_client_wrapped.shutdown(socket.SHUT_RDWR)
            ssl_client_wrapped.close()
        
        bsock.close()
        
if __name__ == "__main__":
    startServer(bluetoothMAC, port, CipherSuites.ECDHERSA_CHACHA20)
