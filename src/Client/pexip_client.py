'''
Client side code for Synchronised folder over IP solution
Author: Claire Fletcher
'''

import sys 
import socket
import os
import time 
import pydoc
import constant


def error_message(message):
    '''
    Prints and error message and exits the program with exit code 1.

    Parameters:
    e -- error
    message -- specific error message to be printed

    '''
    print(message)
    sys.exit(1)


def get_file_path(dir_path, filename):
    '''
    Gets the path of a file.

    Parameters:
    dir_path -- firectory of the file
    filename -- name of the file

    Returns:
    path -- the path of the file

    '''
    path = os.path.join(dir_path, filename)
    return path


def dir_info(path):
    '''
    Records the current files in a directory and the last time they were updates. 

    Parameters:
    path -- path of the directory

    Returns:
    dir -- dictionary with the directory filenames (key) and last updated time (value)

    '''
    dir = {}
    for file in os.listdir(path):
        filepath = get_file_path(path, file)
        status = os.stat(filepath)
        mod = status.st_mtime
        dir[file] = mod
    
    return dir


def send_file(sock, filename, filepath, command):
    '''
    Sends a file to a connected server with a command to tell the server what to do with the file.

    Parameters:
    sock -- socket that server connection is on
    filename -- name of the file being sent
    filepath -- path of the file being send
    command -- command telling server what to do with the file

    '''
    filesize = os.path.getsize(filepath)

    print("Sending file")
    try:
        sock.send((command + '*' + str(filesize) + '*' + filename).encode())
    except socket.error:
        error_message("Error sending data")

    with open(filepath,"rb") as sending:
        read = sending.read(constant.BUFFER)
        while read:
            try:
                sock.send(read)
            except socket.error:
                error_message("Error sending data")
            read = sending.read(constant.BUFFER)


def update(sock, filename, filepath):
    '''
    Calls send_file with update command to tell server to update file.

    Parameters:
    sock -- socket that server connection is on
    filename -- name of file being sent
    filepath -- path of file being sent

    '''
    print("Update command")
    send_file(sock, filename, filepath, "update")


def add(sock, filename, filepath):
    ''' 
    Calls send_file with add command to tell server to add file.

    Parameters:
    sock -- socket that server connection is on
    filename -- name of file being sent
    filepath -- path of file being sent

    '''
    print("Add command")
    send_file(sock, filename, filepath, "add")


def remove(sock, filename):
    '''
    Sends remove command and filename to tell server to remove the file.

    Parameters:
    sock -- socket that server connection is on
    filename -- name of file being sent
     
    '''
    print("Remove command")
    command = "remove"
    sock.send((command + '*' + '0' + '*' + filename).encode())


# Main functionality
def main():
    '''
    Main Client function.
    
    Setup:
    - Takes the directory path given as an argument for the program and checks it is valid.
    - Sets up a server connection using specified port and host.
    - Sends all the current files in the directory to the server as "initial" command.
    - Then begins monitoring the directory.

    Monitoring:
    - Makes a dictionary of the current directory file names and their last update times.
    - Then waits and repeats this giving two dictionaries of the previous and current file names and update times.
    - The two dictionaries are then compared and appropriate add, update, and remove commands are called.
    - Add and update will send the files but remove will only send the filename and command with filesize as 0.
    - No file that was already sent that hasn't been updated or removed will be sent.

    '''
    
    print("Starting Client")
    dir_path = sys.argv[1] # directory given as path 

    if os.path.isdir(dir_path):
        print("Found directory: " + dir_path)
    else:
        print("Directory not valid. Please input full directory path")
        sys.exit(1)

    # connects to server
    print("Setting up server connection... ")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        error_message("Error setting up socket")
    try:
        sock.connect((constant.SERVER, constant.PORT))
    except socket.error:
        error_message("Connection error")
    
    print("Connected to server \n")


    print("Sending over directory to be monitored \n")
    for file in os.listdir(dir_path):
        filepath = get_file_path(dir_path, file)
        send_file(sock, file, filepath, "initial")
        

    # getting the old info
    print("Monitoring Directory... \n")
    old = dir_info(dir_path)
    while True:
        time.sleep(5)
        new = dir_info(dir_path)

        # check for add or update
        for file in new:
            if not file in old:
                add(sock, file, get_file_path(dir_path, file))
            
            else:
                old_value = old[file]
                new_value = new[file]
                if old_value != new_value:
                    update(sock, file, get_file_path(dir_path, file))

        # check for removals
        for file in old:
            if not file in new:
                remove(sock, file)
        
        # set the old to the new 
        old = new
    

    # Clean up connections
    sock.close()
    print("Disconnectd from Server")


if __name__ == "__main__":
    main()
