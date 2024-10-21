## udp client for single-threaded server

'''
------------------------------------------------------------------------------
Client: opens a socket and sends a wildcard query request to the server,
then receives and unpacks a response from the server.

The wildcard query supported follows the format: "x?x", where x is any
combination of letters and ? is any single letter. There may be multiple
? characters in the query.

Application protocol: the request from the client contains a command, and
the response from the server contains a status code and the number of words
matching the wildcard query.

Request format and example:
Command               -> FIND a?t
Bytes header          -> Bytes: 3
Request-type header   -> Request-type: single-request
-------------------------------------------------------------------------------
'''

## imports
from socket import *        ## get socket constructor and constants

## server constants
SERVERHOST = ''     ## server machine, '' means local host
SERVERPORT = 13000  ## a non-reserved port number to listen on
SERVERADDRESS = (SERVERHOST, SERVERPORT)    ## where client messages will be sent to

def runClient():
    ''' starts client process by creating socket and calling handler methods '''

    ## create socket
    clientSocket = socket(AF_INET,SOCK_DGRAM)       ## UDP socket object

    ## perform request/response logic
    sendRequest(clientSocket)                       ## get and send request to server
    readResponse(clientSocket)                      ## unpack server response

def sendRequest(clientSocket):
    ''' send wildcard query request to server '''

    ## get wildcard query from keyboard input
    print('========================================================')
    query = input("wildcard query: ")  
    print('========================================================') 

    ## package into protocol's request format
    ## FIND <word> \n Bytes: <num-bytes> \n Connection-type: <single- or multi-request>
    qbytes = len(query.encode('utf-8'))
    qtype = "single-request"
    query_msg = f'FIND {query}\nBytes: {qbytes}\nConnection-type: {qtype}' 

    ## send query through the client socket            
    clientSocket.sendto(query_msg.encode(),SERVERADDRESS)   

def readResponse(clientSocket):
    ''' read server response '''

    print(f'received response:\n')

    ## get response
    while True:
        response = clientSocket.recvfrom(1024)         ## accept response from the server

        ## decode response
        response = response[0].decode()     ## convert query to ASCII
        print(f'{response}', end='')        ## print what's been received so far
        
        if ']' in response: break   ## break when final packet is received
        
    print('\n--------------------------------------------------------')


## driver code
runClient()


