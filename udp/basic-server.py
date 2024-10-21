## udp single-threaded server

'''
-------------------------------------------------------------------------------
Single-threaded server: opens a socket on a port, then waits for a 
wildcard query from a client and sends a response through the server socket.

The wildcard query supported follows the format: "x?x", where x is any
combination of letters and ? is any single letter. There may be multiple
? characters in the query.

Application protocol: the request from the client contains a command, and
the response from the server contains a status code and the number of words
matching the wildcard query.

Response format and example:
Status code                         -> Code 11
Status message (n: num matches)     -> Success: Found <n> matches for <x>.
Body (matches)                      -> [<word_1> <word_2> ... <word_n>]
-------------------------------------------------------------------------------
'''

## imports
from socket import *        ## get socket constructor and constants
import regex as re          ## for querying the database (txt file)
import pandas as pd         ## to read and load the txt file

## server constants
SERVERHOST = ''     ## server machine, '' means local host
SERVERPORT = 13000  ## a non-reserved port number to listen on

DF = pd.read_csv('1442907.txt', sep=' ', header=None, names=['word'])    ## dataframe of word list
DF = DF['word'] ## to convert from a dataframe to a series object


def startServer():
    ''' start server by creating socket and calling handler methods '''

    ## create socket
    serverSocket = socket(AF_INET,SOCK_DGRAM)   ## UDP socket object
    serverSocket.bind((SERVERHOST,SERVERPORT))  ## bind server socket to port

    ## call handlers
    handleClient(serverSocket)    ## start accepting incoming datagrams


def handleClient(serverSocket):
    ''' receive and perform wildcard query from client '''

    ## print to console
    print("\nserver started successfully!")

    ## listen for incoming datagrams
    while True:

        ## accept bytes from the socket
        request, client_address = serverSocket.recvfrom(1024)

        ## perform and unpack the received query
        num_matches, matches, query = performQuery(request)

        ## send response back to the client
        sendResponse(serverSocket, client_address, num_matches, matches, query)                     

def performQuery(request):
    ''' unpack and perform wildcard query logic '''

    ## decode query
    request = request.decode()                  ## convert query to ASCII
    print(f'received request:\n{request}\n')

    ## unpack query
    query_string = request.split('\n')           ## separate headers in the request
    qbytes = int(query_string[1].split(': ')[1]) ## get number of bytes (query length)
    original_query = query_string[0][-qbytes:]   ## get the last qbytes characters as query

    ## reformat query for regex
    query = original_query.replace("?", ".")     ## replace all ? with . for regex
    
    ## note: we don't need to do anything with Request-type, since we only support
    ## single-request queries for this portion of the assignment

    ## get words that match the regex query expression
    matches_tf = DF.str.contains(query, case=False) ## perform regex for series (true/false) object  
    num_matches = matches_tf.sum()                  ## count number of matches in series
    matches = DF[matches_tf.fillna(False)]          ## get series containing all matching words
    print(matches.values)

    ## output and return result
    print(f'\nfound {num_matches} matches for {query}.\n')  
    
    return num_matches, matches.values, original_query

def sendResponse(serverSocket, address, num_matches, matches, query):
    ''' send query response to client '''

    ## set response values for case 00
    rcode = 00  ## no matches found, default
    rmsg = 'No matches found'

    ## set response values for case 11
    if num_matches > 0:
        rcode = 11  ## matches found
        rmsg = f'Success: Found {num_matches} matches for {query}.'

    ## generate full response message
    resp_msg = f'Code {rcode}\n{rmsg}\n{matches}'

    ## send query through the server socket            
    serverSocket.sendto(resp_msg.encode('utf-8'), address) 
    
## driver code
startServer()


