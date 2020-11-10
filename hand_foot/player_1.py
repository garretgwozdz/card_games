import socket
import time

HOST = '127.0.0.1'

PORT = 2020
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
    
    if(data == "GOODBYE"):
    	playing = False
    
time.sleep(3)
end_data = 'GOODBYE'
sock.send(end_data.encode())
