##Client side code for Synchronised folder over IP solution
##Author: Claire Fletcher

#Currently running over TCP 

import sys #needed for arguments 
import socket


def main():
    print("Starting Server")

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
        if not data:
            break #break if what is received is not correct format as expecting

    conn.close()
    print('client disconnected')


if __name__ == "__main__":
    main()


