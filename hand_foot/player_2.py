import socket
import time

HOST = '192.168.1.99'

PORT = 2929
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")

playing = True
while(playing):
    dataFromServer = sock.recv(1024);
    print(dataFromServer.decode());
    data = input()
    sock.send(data.encode())
    
    
    playing = False
    
time.sleep(3)
end_data = 'GOODBYE'
sock.send(end_data.encode())
