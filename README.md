# IP_App

My solution to the synchronised directory across a client and a server is written in python on a windows OS and uses TCP.

I spent approximately 7 hours on this - including research and documentation. I researched both documentation in python and also methods to synchronise directories in python. This led me to information on pydoc thus providing the html documentation found in the doc folder. I also found information on how to use the os package to interact with the files and to monitor them. 

The solution does not consider the optimisation of partial files but does consider the optimisation of not sending the same file multiple times.

Note: the solution currently uses the loopback address 127.0.0.1 but this IP could be altered for the server.

# How to Run the Application

The src folder contains a client and server folder. Within these there are: pexip_client.py and pexip_server.py Once both are running correctly, as below, the system will monitor and synchronise the directory with no further input. The system will also print what is happening to the console for ease.

First:
Run the server using: __pexip_server.py <directory_name>__

Where the directory name is the name of the directory you want to create. This does not have to be the same as the client-side directory name.
*If the directory name is already used for a directory where the server is running (as the new directory is created in the same current working directory as the server) the application will continue but with a warning of this in case it was unknown.*

Then:
Run the client using: __py pexip_client.py <directory_path>__

Where the directory path is the absolute path to the directory that will be synchronised.


# Known Shortcomings

My solution does have a few shortcomings and also some assumptions:.
* If a file is altered on the server side the synchronistion will break unless the client side is also altered manually. This is only a one-way synchronisation.
* There is no server to client communication and thus any errors with the received data will stop the program instead of handling it and continuing.
* Doesn't handle missing data so if part of a file is missing it will stay missing until another update sends that file again. However, the solution will note the missing data with a print statement.
* .send() is used for sending which may not work over a network with high traffic as effectively.
* The data being sent is not currently being encrypted or secured in any way.
* Does not handle folders within the directory, only files.
* Assumes that after the concatenated command, file, filesize data sent to the server the next packets are the data needed. This is a fair assumption as long as there are no crashes or lost packets.
* The system will likely not scale well to monitoring large amounts of files as it goes through every file whilst monitoring and handles each one consecutively which would likely become slow in larger directories. It also cannot monitor more than one directory.
* Allows use of an existing server-side directory with a warning of this in case the user is not aware. Then if there are files with the same name attempting to be sent, it adds 1 to the existing filename. However, it does not do this well as it adds the number after the extension.
* The Server can only accept one connection (as I set it to listen(1)) and will shut down when the client disconnects.


# Improvements

There are a few improvements based on the shortcomings but also some that would make it more interesting.

Shortcoming Improvements:
* I would add tracking of folders as well as files by including checks for folders and then repeating the same file monitoring within each of these. Potentially a thread that checks and sends commands to the server could be started for each folder within the directory so that it is more efficient.
* I would enable server client communication by having the server send the client a message and the client listen for messages from the server. The server would send back an error, the command it errored on, and then the filename. The client would then redo the command for that file. This would then enable handling for missing data as the client would know and repeat. This could also be extended to the server receiving an incorrect command. This allows the program to continue without exiting when the data sent is wrong.
* I would add in the use of TLS and then encrypt the data with AES 128 bit or higher for a more secure sending of data. Other protocols and security principles could be looked into the extend this further. The solution could also implement FTPS protocol which is a good file transfer protocol which uses the TLS protocol.
* I would look into ways to extend this to a larger system such as testing it with large amounts of data and also the folder solution discussed in the first improvement.
* I would also optimise the file sending with partially similar data by potentially noting what the previous file contained and then only sending the new data. The server would then need to know where to write the new data in the file.
* Currently when a client disconnects the server also shuts down. This could be improved to keep the server constant by starting to listen again when the client disconnects and then checking that the connecting client still wants to monitor the same directory. This could also be extended to have the server accept multiple connections and monitor multiple directories at once.

Interesting Improvements:
* It would be interesting to implement this with a threaded system for quicker checks of the dictionary and updates; however, this would need to involve good concurrency and checks that files are not being sent multiple times. Potentially it would not work effectively but looking into it could be interesting and, in fact, a good exercise to test concurrency. A thread for each folder within the directory is more likely to be useful than threads looking at a certain number of files. This is because when the directory being monitored is large enough for threads to be beneficial it likely also already contains a file system. 
* It would be interesting to implement a GUI for this so that someone could track exactly what was being sent and any missing packets etc. However, this would only be useful for someone that wanted to actively monitor the progress such as an admin. Most users would be content with just having their directories synchronised and not needing to do anything else.
* It would be interesting to implement this with synchronisation in both directions. This would allow for alterations to the server and client directories which would be kept synchronised and emulate the ability to work on your machine or access the data from elsewhere (i.e. access and work with the server files which would also synchronise with your machine). This also has an element of concurrency handling or an assumption that a file is not being worked on in both locations at once.
* It could also be interesting, and useful, to print what happens to a log which can then be kept once the system is stopped. This would be useful for the history of the changes and also potentially helpful to create a system that can be restarted upon crashing or in the extension to multiple connections and directories mentioned previously.
