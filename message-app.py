# message-app

import socket

SERV_HOST = "127.0.0.1"
SERV_PORT = 64532  #re-evalute this choice



print("Do you want to start a listen for a connection or connect to an existing server? [listen/connect] ")

message_mode = input()
if message_mode == "listen":
    print("Enter your username: ")
    user_name = input()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERV_HOST, SERV_PORT))
        s.listen()
        conn, addr = s.accept()
       
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(user_name.encode('utf-8'))
            user_connect = conn.recv(1024)
            print(user_connect.decode('utf-8'), "has joined")
            while True:
                data = conn.recv(1024)
                print(user_connect.decode('utf-8'), "> ", end='')
                print(f"{data.decode('utf-8')}")
                print(user_name, "> ", end='')
                input1 = input()
                if input1 == "exit":
                    break
                conn.sendall(input1.encode('utf-8'))
               

elif message_mode == "connect":
    print("Enter the name of a contact or the ip address of a new contact ")
    CON_HOST = input()
    
    if CON_HOST.isupper() or CON_HOST.islower():
        config = open("contacts.txt")
        line = config.readline()
        while line != '':
            first_word = line.split(' ')
            if first_word[0] == CON_HOST:
                CON_HOST = first_word[1]
                CON_PORT = first_word[2]
            line = config.readline()
    else:
        
        print("What port would you like to connect to? ") #figure out ports
        CON_PORT = input()
        print("\nport is", CON_PORT, "\n")
        print("Would you like to save this connection? [y/n]")
        save = input()
        name = input("this contact will be saved as: ")
        if save == "y" or "Y" or "yes":
            config = open("contacts.txt", "a")
        
            config.write(f"{name} {CON_HOST} {CON_PORT} \n") #maybe make this a sqlite db later
            config.close
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CON_HOST, int(CON_PORT)))
        user_connect = s.recv(1024)
        print("Enter your username: ")
        user_name = input()
        s.sendall(user_name.encode('utf-8'))
        print("You have entered the chat with" , user_connect.decode('utf-8'),"  - type exit to leave \n")
        while True:
            print(user_name, "> ", end='')
            input1 = input()
            if input1 == "exit":
                break
            s.sendall(input1.encode('utf-8'))
            data = s.recv(1024)
            print(user_connect.decode('utf-8'),"> ", end='')
            print(f"{data.decode('utf-8')}")

else:
    print("Incorrect input")
