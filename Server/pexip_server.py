#!/usr/bin/python
##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket
import os

BUFFER = 4096

def make_directory(dir):
    cwdir = os.getcwd() 
    path = os.path.join(cwdir, dir)
    os.mkdir(path) #note this takes a path and also throws OSError if directory exists. Handle this.
    #if exists then don't do the mkdir and just move into it? or do error message as may not realise it exists.
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
    cwdir = os.getcwd() 
    oldpath = os.path.join(cwdir, "temporary")
    newpath = os.path.join(cwdir, filename)
    os.rename(oldpath, newpath)



def receive_file(conn, filesize, name):
    print("Receiving file")

    with open(name, "wb") as receiving:
        size_left = filesize
        while size_left: 
            filedata = conn.recv(BUFFER)
            receiving.write(filedata)
            size_left -= len(filedata)

        print("File received")
#use the size for the filedata so while less than filesize and then increment it.
#doesnt check for missing parts of files, doesn't check for file that isnt a full 4096 buffer size?





def main():
    
    print("Starting Server")
    dir = sys.argv[1] #could also just assume it takes in a path
    path = make_directory(dir)
    print("Directory setup")
    os.chdir(path) #move into this directory 
    print("Current working directory: " + os.getcwd())

    #Server setup, note that only accepts one connection atm
    print("Setting Server to Listen")
    HOST = "127.0.0.1"  # listening on all (assuming python same as C)
    PORT = 8080      # Port to listen on (non-privileged ports are > 1023)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, PORT))
    sock.listen()
    print("Server Listening for connections...") #add if statement on this

    conn, addr = sock.accept()
    print("Connected to Client: ", addr)

    print("Listening for client commands...")
    while True:
        
        receive = conn.recv(BUFFER).decode()
        command, filesize, filename = receive.split('*')
        print("Received command: " + command)
        print("Received file size: " + filesize)
        print("Received filename: " + filename)
        filesize = int(filesize)

        if command == "initial":
            receive_file(conn, filesize, filename)
            
        
        if command == "add":
            #tell client received add
            #assume next data is file
            receive_file(conn, filesize, "temporary") #should create file called temporary
            add(filename)

        elif command == "update":
            #tell client received update
            #assume next data is file
            receive_file(conn, filesize, "temporary")
            update(filename)


        elif command == "remove":
            #tell client received remove
            remove(filename)

        else:
            print("Command not recognised")
            #send client message telling them



    conn.close()
    print("Client disconnected")
    print("Shutting down server")
    sock.close()
    os.rmdir(path)


if __name__ == "__main__":
    main()


