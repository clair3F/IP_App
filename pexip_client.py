##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket
import os
import time 


def find_path(directory): #currently assumes the file is in the same directory as the script 
    #may not work as using directory not file
    path = os.path.abspath(filename)
    return path


#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python info on sending/receiving files as need to send in sections

def update():


def add():


def remove():


def main():
    print("Starting Client")

    directory = sys.argv[0] #directory from arguments on command line
    path = find_path(directory)

    #use os.listdir and os.stat() and then status.st_mtime 
    old = 
    while true:
        time.sleep(5)




    #dict store all files before and also all their mod times
    #then wait
    #then compare all files check for new and check for old at same time if find it then check updated 
    #when find one then call event to send to server command and file name 
    #file = open() then data = read() then send this along with filename 



    #First steps: connection to server
    SERVER = '127.0.0.1'
    PORT = 8080

    #initial message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    byte_message = bytes("Hello, World!", "utf-8")

    sock.connect((SERVER,PORT))
    sock.send(byte_message)
    sock.close()


if __name__ == "__main__":
    main()
