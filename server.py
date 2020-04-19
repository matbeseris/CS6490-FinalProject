import socket
import ssl

# my bluetooth adapter MAC address
bluetoothMAC = "00:C2:C6:6F:B6:15"
port = 20 # any port that is available

bsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
ssl_context.load_dh_params("dhparams.pem")
ssl_context.set_ciphers("DHE-RSA-AES256-GCM-SHA384")

bsock.bind((bluetoothMAC, port))
bsock.listen(1)

print("Waiting for connection")

try:
    client, addr = bsock.accept()
    print("client connected")
    
    ssl_client_wrapped = ssl_context.wrap_socket(client, server_side=True)
    print("client socket wrapped in SSL with ciphers: " + 
        str(ssl_client_wrapped.cipher()))
    
    while 1:
        msg = ssl_client_wrapped.recv(2048)
        if msg:
            print("Recieved message: " + msg.decode("UTF-8"))
            ssl_client_wrapped.send(msg)
except:
    print("closing socket")
    if ssl_client_wrapped:
        ssl_client_wrapped.close()
    bsock.close()
