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



def main():
    print("Starting Client")

    directory = sys.argv[0] #directory from arguments on command line
    path = find_path(directory)

    #use os.listdir and os.stat() and then status.st_mtime 
    old = 
    while true:
        time.sleep(5) #waits and then gets new info from the 
    #function to monitor the directory 
    #dict store all files before and also all their mod times
    #then wait
    #then compare all files check for new and check for old at same time if find it then check updated 
    #when find one then call event to send to server command and file name 



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




################### Plan:
#DECISION: Always connected or open and close connections bsed on time elapsed/always. Depends on how often the files system is updated.

#Set monitoring directory based on the argument passed in 

#Monitor this directory constantly and then trigger events

#event: update <files> -> send update relevant files
#event: delete <files> -> send delete relevant files
#def update():
#def delete():

#in later versions will update these events to be more optimal
