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



def get_dir_path(directory): #currently assumes the file is in the same directory as the script 
    path = os.path.abspath(filename)#may not work as using directory not file
    return path


def get_file_path(dir, filename):
    #takes in the directory path and the filename and creates absolute path from this




def dir_info(path):
    dir = {}
    for file in os.listdir(path):
        status = os.stat(file)
        mod = status.st_mtime
        dir[file] = mod
    
    return dir




def send_file(sock, filename, filepath, command):
    filesize = os.path.getsize(filepath)

    print("Connected to server")
    sock.send(command.encode())
    sock.send(filesize.encode())#need to encode all three of these correctly
    sock.send(filename.encode())

    with open(filename,"rb") as sending:
        read = sending.read(BUFFER)
        while read:
            sock.send(read)#is send the best command? what protocol etc?
            print("Sending file")
            read = sending.read(BUFFER)




def update(sock, filename, filepath):
    print("Performing update command")
    send_file(sock, filename, "update")




def add(sock, filename, filepath):
    print("Performing add command")
    send_file(sock, filename, "add")




def remove(sock, filename):
    print("Performing remove command")
    command = "remove"
    sock.send(command.encode())
    sock.send(filename.encode())





def main():
    print("Starting Client")

    directory = sys.argv[0] #directory from arguments on command line
    path = get_dir_path(directory)
    print("Found directory: " + path)

    #First steps: connection to server
    print("Setting up server connection...")
    SERVER = '127.0.0.1'
    PORT = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER,PORT))
    #if statement then the print
    print("Connected to Server")

    #getting the old info
    print("Monitoring Directory...")
    old = dir_info(path)
    while true:
        time.sleep(5)
        new = dir_info(path)

        #check for add or update
        for file in new:
            if not file in old:
                add(sock, file, get_file_path(dir, file))
            
            if #test value comparison

            #check the update values

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
