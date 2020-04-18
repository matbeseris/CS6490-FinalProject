import socket

# my bluetooth adapter MAC address
bluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20 # any port that is available

bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

bsock.bind((bluetoothMAC, port))
bsock.listen(1)

try:
    client, addr = bsock.accept()
    print("client connected")
    while 1:
        msg = client.recv(2048)
        if msg:
            print("Recieved message: " + msg.decode("UTF-8"))
            client.send(msg)
except:
    print("closing socket")
    client.close()
    bsock.close()
