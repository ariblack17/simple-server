## tcp client for multi-threaded server


'''
------------------------------------------------------------------------------
Client: opens a socket and connects to the server, sends a wildcard query 
request, and receives and unpacks a response from the server. Repeats this
process until client disconnect.

The wildcard query supported follows the format: "x?x", where x is any
combination of letters and ? is any single letter. There may be multiple
? characters in the query.

Application protocol: the request from the client contains a command, and
the response from the server contains a status code and the number of words
matching the wildcard query.

Request format and example:
Command                  -> FIND a?t
Bytes header             -> Bytes: 3
Connection-type header   -> Connection-type: multi-request
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

    ## loop until client requests disconnect
    while True:
        query = sendRequest(clientSocket)           ## get and send request to server
        if query == 'quit': break                   ## break if requests disconnect
        readResponse(clientSocket)                  ## unpack server response
    clientSocket.close()                            ## close socket after queries

def sendRequest(clientSocket):
    ''' send wildcard query request to server '''

    ## get wildcard query from keyboard input
    print('========================================================')
    query = input("wildcard query: ") 
    print('========================================================') 

    ## package into protocol's request format
    ## FIND <word> \n Bytes: <num-bytes> \n Connection-type: <single- or multi-request>
    qbytes = len(query.encode('utf-8'))
    qtype = "multi-request"
    query_msg = f'FIND {query}\nBytes: {qbytes}\nConnection-type: {qtype}' 

    ## send query through the client socket            
    clientSocket.send(query_msg.encode())   

    ## return the client's request to check termination
    return query

def readResponse(clientSocket):
    ''' read server response '''

    print(f'received response:\n')

    ## get response
    while True:
        response = clientSocket.recv(1024)         ## accept response from the server

        ## decode response
        response = response.decode()               ## convert query to ASCII
        print(f'{response}', end='')

        if ']' in response: break   ## break when final packet is received

    # print(f'received response:\n{response}') 
    print()

## driver code
runClient()


