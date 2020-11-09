##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket


def main():
    print("Starting Client")


    #First steps: connection to server
    SERVER = '127.0.0.1'
    PORT = 8080

    #initial message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    byte_message = bytes("Hello, World!", "utf-8")

    sock.connect((SERVER,PORT))
    sock.send(byte_message)
    sock.close()


main()






################### Plan:
#DECISION: Always connected or open and close connections bsed on time elapsed/always. Depends on how often the files system is updated.

#Set monitoring directory based on the argument passed in 

#Monitor this directory constantly and then trigger events

#event: update <files> -> send update relevant files
#event: delete <files> -> send delete relevant files

#in later versions will update these events to be more optimal
