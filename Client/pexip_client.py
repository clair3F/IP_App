#!/usr/bin/python
##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 
#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python info on sending/receiving files as need to send in sections
#http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html 


import sys #needed for arguments 
import socket
import os
import time 

BUFFER = 4096




def get_file_path(dir_path, filename):
    path = os.path.join(dir_path, filename)
    return path


#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python info on sending/receiving files as need to send in sections


def dir_info(path):
    dir = {}
    for file in os.listdir(path):
        filepath = get_file_path(path, file)
        status = os.stat(filepath)
        mod = status.st_mtime
        dir[file] = mod
    
    return dir




def send_file(sock, filename, filepath, command):
    filesize = os.path.getsize(filepath)

    print("Sending file")
    sock.send((command + '*' + str(filesize) + '*' + filename).encode())

    with open(filepath,"rb") as sending:
        read = sending.read(BUFFER)
        while read:
            sock.send(read)#is send the best command? what protocol etc?
            print("Sending file")
            read = sending.read(BUFFER)




def update(sock, filename, filepath):
    print("Performing update command")
    send_file(sock, filename, filepath, "update")




def add(sock, filename, filepath):
    print("Performing add command")
    send_file(sock, filename, filepath, "add")




def remove(sock, filename):
    print("Performing remove command")
    command = "remove"
    sock.send((command + '*' + '0' + '*' + filename).encode())





def main():
    print("Starting Client")

    dir_path = sys.argv[1] #directory from arguments on command line, assume give me a path...

    #check for a valid directory 
    print("Found directory: " + dir_path)

    #First steps: connection to server
    print("Setting up server connection...")
    SERVER = '127.0.0.1'
    PORT = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER,PORT))
    #if statement then the print
    print("Connected to Server")

    print("Sending over directory to be monitored")
    for file in os.listdir(dir_path):
        filepath = get_file_path(dir_path, file)
        send_file(sock, file, filepath, "initial")
        

    #getting the old info
    print("Monitoring Directory...")
    old = dir_info(dir_path)
    while True:
        time.sleep(5)
        new = dir_info(dir_path)

        #check for add or update
        for file in new:
            if not file in old:
                add(sock, file, get_file_path(dir_path, file))
            
            else: #or can use .items() in the for loop but don't need value of every file so less efficient?
                old_value = old[file]
                new_value = new[file]
                if old_value != new_value:
                    update(sock, file, get_file_path(dir_path, file))

        #check for removals
        for file in old:
            if not file in new:
                remove(sock, file)
        
        #set the old to the new 
        old = new
    
    sock.close()
    print("Connection closed")



if __name__ == "__main__":
    main()