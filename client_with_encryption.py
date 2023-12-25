import socket
import threading
import sys
from cryptography.fernet import Fernet


 
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
key = b'rghg-eJVDepY3cZouOh0SWtHO8jeF1Kuq4ogA3hyfo7='
fernet = Fernet(key)
        
        
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
            
            message = fernet.decrypt(client.recv(2048)).decode("ascii")
            
            if message == "NICK":
                encrypted_message = fernet.encrypt(nickname.encode("ascii"))
                client.send(encrypted_message)
                
                admin_message = fernet.decrypt(client.recv(2048)).decode("ascii")
                
                if admin_message == 'PASS':
                    encrypted_message = fernet.encrypt(password.encode("ascii"))
                    client.send(encrypted_message)
                    
                    REFUSE_CODE = fernet.decrypt(client.recv(2048)).decode("ascii")
                    if REFUSE_CODE == "REFUSE":
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
            encrypted_message = fernet.encrypt(message.encode("ascii"))
            
            
            if x.lower() == "bye":
                client.send(encrypted_message)
                client.close()
                sys.exit("Bye")

            else:
                client.send(encrypted_message)

        except Exception or KeyboardInterrupt as e:
            print("[!] Error in handle_sent_msg: function")
            print(f"[!] Error handling message from server: {e}")
            close_connection()



#----------------------------------------------------------------------- 



def close_connection():
    message = f'{nickname}: bye'
    encrypted_message = fernet.encrypt(message.encode("ascii"))
    client.send(encrypted_message)
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
