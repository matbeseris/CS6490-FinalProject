import socket
import ssl

# Bluetooth server information
serverBluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20

bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

ssl_context = getSSLContext_client(DHERSA_AES256)
ssl_bsock_wrapped = ssl_context.wrap_socket(bsock, server_hostname=serverBluetoothMAC)

ssl_bsock_wrapped.connect((serverBluetoothMAC, port))
print("connected...")

if not ssl_bsock_wrapped:
    print("error connecting to server")
    exit(1)

while 1:
    sendmsg = input("Message to send: ")
    if sendmsg == "q":
        break
    ssl_bsock_wrapped.send(bytes(sendmsg, "UTF-8"))

    recvmsg = ssl_bsock_wrapped.recv(2048)
    if recvmsg:
        print("Recieved msg: " + recvmsg.decode("UTF-8"))

ssl_bsock_wrapped.close()
