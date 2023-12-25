import socket
import threading
import sys

nickname = input("[*] Enter your nickname: ")

if nickname.lower() == "admin":
    password = input("[*] Enter admin password: ")
    
server_ip = input("[*] Enter IP address of the server: ")

server_port = int(input("[*] Enter port of the server: "))





client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    
try:
    client.connect((server_ip, server_port))
except Exception as e:
    print(f"[!] Unable to connecet to the server: {e}")
   
        
        
#-----------------------------------------------------------------------  
        
        
    
def get_Host_name_IP():
    try:
        # Importing socket library
        # Function to display hostname and
        # IP address "Support windows and linux"
        host_name = socket.gethostname()
        x = socket.gethostbyname(host_name)
        x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        x.connect(('10.0.0.0', 0))
        host_ip = x.getsockname()[0]
        print("[-] Hostname:", host_name)
        print("[-] IP:", host_ip)

        
    except Exception or KeyboardInterrupt as e:
        print(f"[!] Unable to get Hostname and IP: {e}")
        close_connection()
   
        
        
#-----------------------------------------------------------------------  
        
        
    
def handle_rece_msg(client: socket.socket):

    
    while True:

        try:
            message = client.recv(1024).decode("ascii")
            
            if message == "NICK":
                client.send(nickname.encode("ascii"))
                admin_message = client.recv(1024).decode("ascii")
                
                if admin_message == 'PASS':
                    client.send(password.encode("ascii"))
                    
                    if client.recv(1024).decode("ascii") == "REFUSE":
                        print("[!] Connection Refused!: Wrong Password")
                        close_connection()
                        
            elif message == f"[!] Admin removed {nickname}":
                close_connection()
                break
                    
            else:
                print(message)

        except Exception or KeyboardInterrupt as e:
            print("[!] Error in handle_rece_msg: function")
            print(f"[!] Error handling message from server: {e}")
            close_connection() 
   
        
        
#-----------------------------------------------------------------------  
        
        
    
def handle_sent_msg(client: socket.socket):
    while True:
        try:
            x = input("")
            message = f'{nickname}: {x}'
            
            
            if x.lower() == "bye":
                client.send(message.encode("ascii"))
                client.close()
                sys.exit("Bye")

            else:
                client.send(message.encode("ascii"))

        except Exception or KeyboardInterrupt as e:
            print("[!] Error in handle_sent_msg: function")
            print(f"[!] Error handling message from server: {e}")
            close_connection()



#----------------------------------------------------------------------- 



def close_connection():
    msg = f'{nickname}: bye'
    client.send(msg.encode("ascii"))
    client.close()
    sys.exit("Bye")
 
        
        
#-----------------------------------------------------------------------  
        
        
    
def client_thread():
        send = threading.Thread(target=handle_sent_msg, args=(client,))
        rece = threading.Thread(target=handle_rece_msg, args=(client,))
        send.start()
        rece.start()
        send.join()
        rece.join()
   
        
        
#-----------------------------------------------------------------------  
        
        
     
while True:
    try:
        
        get_Host_name_IP()
        print("[$] Chat started")
        client_thread()
        
        
    except Exception or KeyboardInterrupt as e:
        print("[!] Error while trying to connect to the server")
        print(f"[!] Error handling message from server: {e}")
        close_connection()
