import socket
import threading

PORT =5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE ='!DISCONNECT'
clients =[]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg = conn.recv(20).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            
        print(f"[{addr}] {msg}")
        print(len(msg))
        message =msg
        conn.send(message.encode(FORMAT))
        
    conn.close()
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn ,addr = server.accept()
        print(f"[ACTIVE CONNECTION] {threading.active_count}")
        clients.append(conn)
        thread =threading.Thread(target=handle_client,args=())
        thread.start()
        thread.join()
        
print("[STARTING] server is starting ...")
start()
    

