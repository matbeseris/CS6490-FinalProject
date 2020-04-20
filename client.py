import socket

serverBluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20

bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
bsock.connect((serverBluetoothMAC, port))
print("connected...")

while 1:
    sendmsg = input("Message to send: ")
    if sendmsg == "q":
        break
    bsock.send(bytes(sendmsg, "UTF-8"))

    recvmsg = bsock.recv(2048)
    if recvmsg:
        print("Recieved msg: " + recvmsg.decode("UTF-8"))

bsock.close()
