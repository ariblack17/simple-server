## tcp single-threaded server

'''
-------------------------------------------------------------------------------
Single-threaded server: opens a socket on a port, listens for a client,
then waits for a wildcard query from that client once a connection is
established. 

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
SERVERPORT = 12000  ## a non-reserved port number to listen on

DF = pd.read_csv('1442907.txt', sep=' ', header=None, names=['word'])    ## dataframe of word list
DF = DF['word'] ## to convert from a dataframe to a series object

def startServer():
    ''' start server by creating socket and calling handler methods '''

    ## create socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  ## TCP socket object
    serverSocket.bind((SERVERHOST,SERVERPORT))  ## bind server socket to port
    serverSocket.listen(1)                      ## allow just one pending client connect

    ## call handlers
    dispatcher(serverSocket)    ## start accepting incoming connections


def handleClient(connection, serverSocket):
    ''' receive and perform wildcard query from client '''

    ## accept query from the connection 
    request = connection.recv(1024)

    ## perform and unpack the received query
    num_matches, matches, query = performQuery(request)

    ## send response through the connection
    sendResponse(connection, num_matches, matches, query)

    ## close connection after just one query
    connection.close()                      

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
    
    ## note: we don't need to do anything with Connection-type, since we only support
    ## single-request queries for this portion of the assignment

    ## get words that match the regex query expression
    matches_tf = DF.str.contains(query, case=False) ## perform regex for series (true/false) object  
    num_matches = matches_tf.sum()                  ## count number of matches in series
    matches = DF[matches_tf.fillna(False)]          ## get series containing all matching words
    print(matches.values)

    ## output and return result
    print(f'found {num_matches} matches for {query}.')  
    
    return num_matches, matches.values, original_query

def sendResponse(connection, num_matches, matches, query):
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
    connection.sendall(resp_msg.encode('utf-8')) 
    

def dispatcher(serverSocket):
    ''' accept connections from clients '''
    
    ## print to console
    print("\nserver started successfully!")

    ## call handler method for each incoming connection
    while True:                                     ## wait for next connection
        print("\nwaiting for connections...", end=' ')
        connection, address = serverSocket.accept() ## accept connection
        print(f"server connected to {address}\n")   ## output connection info
        handleClient(connection, serverSocket)      ## pass off to handleClient


## driver code
startServer()


