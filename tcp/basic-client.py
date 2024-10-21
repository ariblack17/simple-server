## tcp client for single-threaded server

'''
------------------------------------------------------------------------------
Client: opens a socket and connects to the server, sends a wildcard query 
request, and receives and unpacks a response from the server.

The wildcard query supported follows the format: "x?x", where x is any
combination of letters and ? is any single letter. There may be multiple
? characters in the query.

Application protocol: the request from the client contains a command, and
the response from the server contains a status code and the number of words
matching the wildcard query.

Request format and example:
Command                  -> FIND a?t
Bytes header             -> Bytes: 3
Connection-type header   -> Connection-type: single-request
-------------------------------------------------------------------------------
'''

## imports
from socket import *        ## get socket constructor and constants

## server constants
SERVERHOST = ''     ## server machine, '' means local host
SERVERPORT = 12000  ## a non-reserved port number to listen on

def runClient():
    ''' starts client process by creating socket and calling handler methods '''

    ## create socket
    clientSocket = socket(AF_INET,SOCK_STREAM)      ## TCP socket object
    clientSocket.connect((SERVERHOST,SERVERPORT))   ## connect to server socket

    ## perform request/response logic
    sendRequest(clientSocket)                       ## get and send request to server
    readResponse(clientSocket)                      ## unpack server response
    
    ## close socket
    clientSocket.close()                            ## close socket after one query

def sendRequest(clientSocket):
    ''' send wildcard query request to server '''

    ## get wildcard query from keyboard input
    query = input("wildcard query: ")  

    ## package into protocol's request format
    ## FIND <word> \n Bytes: <num-bytes> \n Connection-type: <single- or multi-request>
    qbytes = len(query.encode('utf-8'))
    qtype = "single-request"
    query_msg = f'FIND {query}\nBytes: {qbytes}\nConnection-type: {qtype}' 

    ## send query through the client socket            
    clientSocket.send(query_msg.encode())   

def readResponse(clientSocket):
    ''' read server response '''

    ## get response
    response = clientSocket.recv(1024)         ## accept response from the server

    ## decode response
    response = response.decode()               ## convert query to ASCII
    print(f'received response:\n\n{response}\n') 


## driver code
runClient()


