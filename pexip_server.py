##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket
import os


def make_directory():
    cwdir = os.chdir() 
    path = os.path.join(cwdir, dir)
    os.mkdir(path) #note this takes a path and also throws OSError if directory exists. Handle this.
    return path


def update(file, filename):
    os.remove(filename)
    add(file, filename)


def remove(filename):
    os.remove(filename)


def add(file, filename):
    #change file already written to correct filename


def write_file(file, data):
    file.write(data)
    #use this to create a file from the incoming file info in a loop. called if update or add.


def main():
    print("Starting Server")


    #Make directory currently in same path as the server.
    dir = sys.argv[0]
    path = make_directory(dir)
    os.chdir(path) #move into this directory 


    #listening server
    #parse data look for command. if update or add then need to loop through receiving file and creating new file then call their functs
    #if remove then just send filename to remove function
    #else break and close


    #First step: constantly listening server 
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 8080      # Port to listen on (non-privileged ports are > 1023)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    print('Connected to Client', addr)

    while True:
        data = conn.recv(4096)
        print("Received data")

        #checks on the data in here

        if not data:
            break #break if what is received is not correct format as expecting

    conn.close()
    print('client disconnected')


if __name__ == "__main__":
    main()


