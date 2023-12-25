# Imported Libraries
import socket
import threading
from cryptography.fernet import Fernet
            
        
        
#-----------------------------------------------------------------------  
        
# Default Lists        
  
clients = []
nicknames = []
ban_users = []
commands = ["/help", "/kick", "/ban", "/info", "/show", "/unban"]
cmd_command = """
*--------------------------------------------------------------------*
| Commands | What is for                                             |
*--------------------------------------------------------------------*
| /help    | Provides information on available commands              |
|--------------------------------------------------------------------|
| /kick    | Kicks a user out of the chat room                       |
|--------------------------------------------------------------------|
| /ban     | Bans a user from the chat room                          |
|--------------------------------------------------------------------|
| /info    | Provides information on the server and chat room        |
|--------------------------------------------------------------------|
| /show    | Shows a list of all users currently in the chat room    |
*--------------------------------------------------------------------*

How to use commands:

/help admin
/kick name
/ban name
/unban name
/info name
/info users
/info server
/show name
/show users
"""

        
        
#-----------------------------------------------------------------------  
        
# Setup a connection     

server_ip = ""

def check_for_port(p1, p2):
    for port in range(p1, p2+1):
        socket_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_port.settimeout(1)
        available_port = socket_port.connect_ex(('localhost', port))
        if available_port != 0:
            return port
        socket_port.close()
        
    raise Exception("[!] Couldn't find open port")


server_port = check_for_port(8000, 65535)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen()



if len(server_ip) >=1:
    xserver = f"[*] Server is running!, listening on, {server_ip}:{server_port}"
else:
    server_ip = socket.gethostbyname(socket.gethostname())
    xserver = f"[*] Server is running!, listening on, {server_ip}:{server_port}"
            
        
        
#-----------------------------------------------------------------------  
        
# Server details       
     
def server_details():
    global host_name, host_ip, server_info
    try:
        host_name = socket.gethostname()
        x = socket.gethostbyname(host_name)
        x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        x.connect(('10.0.0.0', 0)) 
        """
        x.connect(('10.0.0.0', 0)) 
        This line connects the x socket object to the IP address '10.0.0.0'
        on port 0. This is a dummy connection that is used to determine
        the local IP address of the machine.
        """
        
        host_ip =  x.getsockname()[0]
        """
        host_ip =  x.getsockname()[0]
        This line uses the getsockname function of the x socket object
        to get the local IP address of the machine and store it in the
        host_ip variable
        """
        server_info =  f"""--------------------------------------------------------------------
{xserver}
[-] Hostname: {host_name} 
[-] IP: {host_ip}       
[-] Port: {server_port}
[-] Share IP and port with the client
-------------------------------------------------------------------- """   
        print(server_info)
        
    except:
        print("[*] Unable to get Hostname and IP")
        
  
        
#----------------------------------------------------------------------- 

# Cryptography: Encryption and Decryption

key = b'rghg-eJVDepY3cZouOh0SWtHO8jeF1Kuq4ogA3hyfo7='
fernet = Fernet(key)



#-----------------------------------------------------------------------         
# Disconnect users     
        
def Remove(client):
    while True:
        if client in clients:
            user = clients.index(client)
            """
            This line retrieves the index of the client socket object
            in the users list and stores it in the user variable.
            """
            nickname = nicknames[user]
            """
            These lines retrieve the nickname associated with the client
            socket connection.
            """
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            """
            This line closes the client connection.
            Remove it from the nicknames list.
            """
            broadcast(f"[!] {nickname} left", client)
            print(f"[!] {nickname} left the group! ")
            """ 
            This line broadcasts a message to all other connected clients
            that the nickname associated with the client socket connection
            has left the chat.
            """
        elif client in nicknames:
            user = clients[nicknames.index(client)]
            send_msg_client(user, "bye")
            clients.remove(user)
            user.close()
            nicknames.remove(client)
            broadcast(f"[!] Admin removed {client}", user)
            print(f"[!] Admin removed {client}")
            
            
            
       
        
        
#-----------------------------------------------------------------------         
       
# Broadcasting messages  
    
def broadcast(message: str, client: socket.socket):
    for client_conn in clients:
        if client_conn != client:
            try:
                encrypted_message = fernet.encrypt(message.encode("ascii"))
                client_conn.send(encrypted_message)
                
            except Exception or BrokenPipeError as e:
                print(f"Error broadcasting message: {e}")
                Remove(client_conn)
        
        
        
#-----------------------------------------------------------------------  
        
# Handle users' messages       
        
def handle_clients_messages(client):
    while True:
        try:
            cmd = close_conn = message = fernet.decrypt(client.recv(1024)).decode("ascii")
            
            nickname_admin = "admin"
            
            if nickname_admin in cmd:
                
            
                if cmd[len(nickname_admin)+2:].startswith("/"):
                    for command in commands:
                        if cmd[len(nickname_admin)+2:].startswith(command):
                            cmd_admin = cmd.split()
                            x = cmd_admin[1]
                            y = cmd_admin[2]
                            admin(client, x, y)
                            
    
                elif "bye" in cmd.lower():
                    Remove(client)
            
                else:
                    broadcast(message, client)
                    

            
            elif "bye" in close_conn.lower():
                Remove(client)
                
            
            else:
                broadcast(message, client)
            "Send a message to all the clients"
            
            
        except Exception or KeyboardInterrupt as e:
            print(f"Error from handle_clients_messages: {e}")
            Remove(client)
    """  
    Overall, this function handles received messages from the client
    and broadcasts them to all other clients until the client disconnects
    or an exception is raised. If an exception is raised, it removes
    the client from the users list, closes the connection, and broadcasts
    a message to all other clients that the associated nickname has
    left the chat.
    """
         
         
         
#-----------------------------------------------------------------------  
        
# Handle users' connections     
    
def user_management():
    
    while True:

        
        client, address = server.accept()
        print("[$] Accepted connection from: %s:%d" % (address[0], address[1]))
        """
        This line waits for an incoming client connection, accepts it, and returns
        a new socket object client and the address of the client as a tuple address.
        """
        
        
        send_msg_client(client, "NICK")
        nickname = fernet.decrypt(client.recv(1024)).decode("ascii")
        
        
        

            
        """ 
        These lines send the NICK command to the newly connected client and waits
        for the client to send back a nickname, which is then stored in the nickname
        variable.
        """
        
        
        """
        Check for admin
        """
        if nickname.lower() == "admin":
            admin_login(client, address, nickname)
        
        elif nickname in ban_users:
            clients.append(client)
            nicknames.append(nickname)
            thread = threading.Thread(target=handle_clients_messages, args=(client,))
            thread.start()
            ban_checker(address, nickname)         
            
        
        else:
            
            """ 
            These lines add the nickname to the nicknames list and add the client socket
            object to the clients list.
            """
            clients.append(client)
            nicknames.append(nickname)
            
            
            print("[-] Nickname of the user %s:%d" % (address[0], address[1]), f"is {nickname}") 
            broadcast(f"[$] {nickname} has joined the group", client)
            send_msg_client(client, "[$] Connected to the server ")
            thread = threading.Thread(target=handle_clients_messages, args=(client,))
            thread.start()
            ban_checker(address, nickname)
            
        
         
         
#-----------------------------------------------------------------------  
        
# Handle Admin login
        
def admin_login(client, address, nickname):
        
        # prompt admin for password
        send_msg_client(client, 'PASS')
        password = fernet.decrypt(client.recv(1024)).decode("ascii")

        # check if password matches
        if password == "adminpass":
            clients.append(client)
            nicknames.append(nickname)
            print("[-] Nickname of the user %s:%d" % (address[0], address[1]), f"is {nickname}")
            broadcast(f"[$] {nickname} has joined the group", client)
            send_msg_client(client, "[$] Connected to the server ")
            send_msg_client(client, cmd_command)
            thread = threading.Thread(target=handle_clients_messages, args=(client,))
            thread.start()
        

        else:
            # refuse connection
            print(f"[!] Warning: Connection refused for {address[0]}:{address[1]} due to wrong password.")
            print(f"[!] Warning: Someone attemped to login as admin")
            send_msg_client(client, "[!] Connection refused: Wrong password")
            client.close()
            
            
     
         
       
#-----------------------------------------------------------------------  

# Admin commands

def admin(client, message_cmd, name):# ["/help", "/kick", "/ban", "/info", "/show"]

    for command in commands:
        if message_cmd == command:
            
            if message_cmd == "/help" and name.lower() == "admin":
                send_msg_client(client, cmd_command)
               
                
            elif message_cmd == "/kick":
                admin_kick(client, name)
                
                
            elif message_cmd == "/info":
                admin_info(client, name)
            
            
            elif message_cmd == "/ban":
                admin_ban(client, name) 
                
                
            elif message_cmd == "/unban":
                admin_unban(client, name)
            
            
            elif message_cmd == "/show":
                admin_show(client, name)
            
         
         
#-----------------------------------------------------------------------   
  
# Information of user

def admin_info(client, name_info):
    
    if name_info.lower() == "server":
        send_msg_client(client, server_info)
    
    
    elif name_info in nicknames:
        info_user = clients[nicknames.index(name_info)]
        inf_msg = f"[-] Info of {name_info}\n{info_user}"
        send_msg_client(client, inf_msg)
        
        
    elif name_info.lower() == "users":
        for i in nicknames:
            info_user = clients[nicknames.index(i)]
            inf_msg = f"[-] Info of {i}\n{info_user}\n"
            send_msg_client(client, inf_msg)
            
    
    else:
        msg_error = f"[!] User not found. {name_info}"
        send_msg_client(client, msg_error)   


#-----------------------------------------------------------------------

# Kick user

def admin_kick(client, name):
    if name in nicknames:
        remove_user = clients[nicknames.index(name)]
        clients.remove(remove_user)
        remove_user.close()
        nicknames.remove(name)
        msg_a = f"[!] You removed {name}"
        msg_k = f"[!] Admin removed {name}"
        send_msg_client(client, msg_a)
        print(msg_k)
        broadcast(msg_k, client)
                
                    
    else:
        else_msg = f"[!] User not found: {name}"
        send_msg_client(client, else_msg)
  
    
    
#-----------------------------------------------------------------------

# Ban user

def admin_ban(client, name):
    msg_a = f"[!] You banned {name}"
    msg_b = f"[!] Admin banned {name}"
    msg_n = f"[!] {name} not found"
    msg_u = f"[!] {name} already banned"
    
    if name in ban_users:
        send_msg_client(client, msg_u)
    
    elif name not in ban_users:
        ban_users.append(name)
        admin_kick(client, name)
        send_msg_client(client, msg_a)
        print(msg_b)
        broadcast(msg_b, client)
             
                
    else:
        send_msg_client(client, msg_n)
    
  
    

#-----------------------------------------------------------------------

# Unban user

def admin_unban(client, name):
    msg_a = f"[!] You unbanned {name}"
    msg_b = f"[!] Admin unbanned {name}"
    msg_n = f"[!] {name} not found"
    
    if name in ban_users:
        ban_users.remove(name)
        send_msg_client(client, msg_a)
        broadcast(msg_b, client)
                
    else:
        send_msg_client(client, msg_n)
    
  
    
    
#-----------------------------------------------------------------------    

# View the status of a user

def admin_show(client, name):
    if name == "users":
        msg_show = f"[-] Available users: \n"
        send_msg_client(client, msg_show)
        for i in nicknames:
            msg_active = f"-> {i} : Active\n"
            send_msg_client(client, msg_active)
        for i in ban_users:
            msg_ban = f"-> {i} : Banned\n"
            send_msg_client(client, msg_ban)
            
    elif name in nicknames:
        msg_user = f"[-] User is active"
        send_msg_client(client, msg_user)
        
  
    
    
#----------------------------------------------------------------------- 

# Check if the user is banned or not

def ban_checker(address, name):
    for i in ban_users:
        if i == name:
            remove_user = clients[nicknames.index(name)]
            clients.remove(remove_user)
            remove_user.close()
            nicknames.remove(name)
            print(f"[!] Warining a banned user tried to connect to the server - {name}")
            print("[!] Warining  connection from: %s:%d" % (address[0], address[1]))
            print(f"[!] Removed")


    
#----------------------------------------------------------------------- 

# Send a message for a single user  
    
def send_msg_client(client, message):
    encrypted_message = fernet.encrypt(message.encode("ascii"))
    client.send(encrypted_message)
                
#-----------------------------------------------------------------------              
                
                
server_details()
user_management()






