'''
Client side code for Synchronised folder over IP solution
Author: Claire Fletcher
'''

import sys
import socket
import os
import pydoc
import constant


def error_message(message):
    '''
    Prints an error message and exits the program with exit code 1

    Parameters:
    message -- specific error message to be printed
    '''
    print(message)
    sys.exit(1)


def make_directory(dir):
    '''
    Makes a new directory in the location of the server program using given directory name. If it already exists, continue with warning.

    Parameters:
    dir -- name of directory being created

    Returns:
    path -- path of the created directory

    '''
    cwdir = os.getcwd() 
    path = os.path.join(cwdir, dir)
    try:
        os.mkdir(path) 
    except OSError:
        print("Directory already exists") 
        print("WARNING: Continuing in the existing directory")
        # continues so that user can choose to use an exising directory for their monitored files

    return path


def get_file_path(dir_path, filename):
    '''
    Gets the path of a file.

    Parameters:
    dir_path -- directory of the file
    filename -- name of the file

    Returns:
    path -- the path of the file

    '''
    path = os.path.join(dir_path, filename)
    return path


def remove(filename):
    '''
    Removes the file with filename from the directory.

    Parameters:
    filename -- name of the file being removed
    
    '''
    os.remove(filename)


def receive_file(conn, filesize, name, dir_path):
    '''
    Receives a file from the client with a given name.

    Parameters:
    conn -- client connection receiving the file on
    filesize -- size of the file being received
    name -- name of the file being created. 
    dir_path -- the path of the directory being synchronised

    '''
    print("Receiving file")
    
    filepath = get_file_path(dir_path, name)

    # checks for an existing file with the same name 
    if os.path.isfile(filepath):
        print("File exists in directory. Adding integer to existing filename")
        
        new_name = name + '1'
        new_filepath = get_file_path(dir_path, new_name)
        
        os.rename(filepath, new_filepath) #alters the existing name to be +1 so that client file can be received with correct name

    # receives the file 
    with open(name, "wb") as receiving: 
        
        size_left = filesize
        
        while size_left: 
            try:
                filedata = conn.recv(constant.BUFFER)
            except socket.error:
                error_message("Error receiving data")

            receiving.write(filedata)
            size_left -= len(filedata)

    if os.path.getsize(filepath) != filesize:
        print("File  may not be fully received. Some data  may be missing")
    
    else:
        print("File received")


def close_server(conn, sock):
    '''
    Closes the connections of the server and the sockets.

    Parameters:
    conn -- client connection being closed
    sock -- server socket being closed

    '''
    # Clean up connections
    conn.close()
    print("Shutting down server")
    sock.close()


# Main functionality
def main():
    '''
    Main Server function.

    Setup:
    - Takes the directory name given as an argument for the program and creates a directory from this in the current working direcory of the server.
    - If the directory already exists it will continue with a warning.
    - Sets up the server listening on a given host and port.
    - Accepts a client connection on the socket.
    - Then begins monitoring for client commands.

    Monitoring:
    - Receives concatenated filename, filesize, and command wherein filesize is sent as 0 for remove command.
    - Then uses simple if/elif/else to check for which command has been sent and then performs the command.
    - For initial nothing is done excepting receiving the files.
    - For update the old file is removed then the new file received
    - For add the file is received same as for initial.
    - For remove the filename is received and then this filename removed from the directory.

    '''
    
    print("Starting Server \n")
    
    dir = sys.argv[1]
    path = make_directory(dir) # takes in directory name not path so create path and directory
    print("Directory setup")
    os.chdir(path) 
    print("Current working directory: " + os.getcwd() + "\n")

    # Server setup
    print("Setting Server to Listen \n")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        error_message("Error setting up socket")

    try:
        sock.bind((constant.HOST, constant.PORT))
    except socket.error:
        error_message("Error binding socket")
    
    print("Server Listening... \n")

    sock.listen(1) # accepts only one connection
    conn, addr = sock.accept()

    # Synchronising the directory
    print("Listening for client commands to sychronise directory... ")
    while True:
        try:
            receive = conn.recv(constant.BUFFER).decode()
        except socket.error:
            print("Error receiving data")

        # happens when client disconnects etc.
        if len(receive) == 0 :
            break

        command, filesize, filename = receive.split('*') # concatenated information in first packet
        
        filesize = int(filesize)
        print("Received command: " + command)

        # parse commands
        if command == "initial":
            receive_file(conn, filesize, filename, path)
            
        elif command == "add":
            print("Adding file")
            receive_file(conn, filesize, filename, path)

        elif command == "update":
            print("Updating file")
            remove(filename)
            receive_file(conn, filesize, filename, path)

        elif command == "remove":
            print("Removing file")
            remove(filename)

        else:
            print("Command not recognised")


    close_server(conn, sock)


if __name__ == "__main__":
    main()


