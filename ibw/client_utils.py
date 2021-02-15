import socket

def get_localhost_name_ip():
    return socket.gethostbyname(socket.gethostname() + '.local')
    

