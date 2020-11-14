##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket
import os

BUFFER = 4096

def make_directory(dir):
    cwdir = os.chdir() 
    path = os.path.join(cwdir, dir)
    os.mkdir(path) #note this takes a path and also throws OSError if directory exists. Handle this.
    return path



def update(filename):
    print("Performing update command")
    print("Removing old file and adding new")
    remove(filename)
    add(filename)



def remove(filename):
    print("Performing remove command")
    os.remove(filename)#note may need to be a path but are in correct directory...



def add(filename):
    print("Performing add command")
    cwdir = os.chdir() 
    oldpath = os.path.join(cwdir, "temporary")
    newpath = os.path.join(cwdir, filename)
    os.rename(oldpath, newpath)



def receive_file(conn, filesize):
    print("Receiving file")
    with open("temporary", "wb") as receiving:
        filedata = sock.recv(BUFFER)
        while filedata: #will this work or will it receive the next command?
            receiving.write(filedata)
        
        print("File received")






def main():
    
    print("Starting Server")
    dir = sys.argv[0] #could also just assume it takes in a path
    path = make_directory(dir)
    print("Directory setup")
    os.chdir(path) #move into this directory 
    print("Current working directory: " + os.chdir())

    #Server setup, note that only accepts one connection atm
    print("Setting Server to Listen")
    HOST = "0.0.0.0"  # listening on all (assuming python same as C)
    PORT = 8080      # Port to listen on (non-privileged ports are > 1023)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, PORT))
    sock.listen()
    print("Server Listening for connections...") #add if statement on this

    conn, addr = sock.accept()
    print("Connected to Client: ", addr)

    print("Listening for client commands...")
    while True:
        
        command = conn.recv(BUFFER).decode()
        filename = conn.recv(BUFFER).decode()
        filesize = conn.recv(BUFFER).decode()
        filesize = int(filesize)
        print("Received data")
        
        if command = "add":
            #tell client received add
            #assume next data is file
            receive_file(conn, filesize) #should create file called temporary
            add(filename)

        elif command = "update":
            #tell client received update
            #assume next data is file
            receive_file(conn, filesize)
            update(filename)


        elif command = "remove":
            #tell client received remove
            remove(filename)

        else:
            print("Command not recognised")
            #send client message telling them

        if not data:
            break #break if what is received is not correct format as expecting



    conn.close()
    print("Client disconnected")
    print("Shutting down server")
    sock.close()


if __name__ == "__main__":
    main()


