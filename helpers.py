from enum import Enum

######
# The different modes the bluetooth server can run in
######
class ServerModes(Enum):
    ECHO = b"ECHO"
    FILE_DOWNLOAD = b"FILE DOWNLOAD"

######
# Possible error messages sent/recieved
######
class ErrorMessages(Enum):
    FILE_ERROR = b"FILE ERROR"

    @classmethod
    def isErrorMessage(cls, msg):
        return msg in cls._value2member_map_

######
# Send a message over the socket. The first 2 bytes will be the length
# of the message to be sent
######
def sendMessage(msg, sock):
    msg_length = len(msg)
    this_msg_begin = 0

    while msg_length > 0:
        msg_length_bytes = None
        this_msg_length = None
        if msg_length >= 2**16:
            msg_length_bytes = ((2**16)-1).to_bytes(2, byteorder="big")
            this_msg_length = (2**16)-1
        else:
            msg_length_bytes = msg_length.to_bytes(2, byteorder="big")
            this_msg_length = msg_length

        sock.sendall(msg_length_bytes + msg[this_msg_begin:this_msg_length])
        msg_length = msg_length - this_msg_length
        this_msg_begin = this_msg_length

######
# Receive a message over the socket. The first 2 bytes will be the length
# of the message. Keep receiving until the whole message has arrived
######
def recvMessage(sock):
    msg = sock.recv(2048)
    total_msg_len = int.from_bytes(msg[:2], byteorder="big")

    recv_msg_len = len(msg) - 2

    while recv_msg_len < total_msg_len:
        new_msg = sock.recv(2048)
        msg += new_msg
        recv_msg_len += len(new_msg)

    return msg[2:]
