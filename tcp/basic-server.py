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
Status code                         -> FIND a?t
Status message                      -> Bytes: 3
Body (matches and matches length)   -> Connection-type: single-request
-------------------------------------------------------------------------------
'''

## imports
from socket import *        ## get socket constructor and constants
import regex as re          ## for querying the database (txt file)
import pandas as pd         ## to read and load the txt file

## server constants
SERVERHOST = ''     ## server machine, '' means local host
SERVERPORT = 12000  ## a non-reserved port number to listen on
# DF = pd.read_csv('1442907.txt', sep=' ', header=None)    ## dataframe of word list
# serie = df.transpose()[0]
DF = pd.read_csv('1442907.txt', sep=' ', header=None, names=['word'])    ## dataframe of word list
DF = DF['word']


def startServer():
    ''' starts server by creating socket and calling handler methods '''
    ## create socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  ## TCP socket object
    serverSocket.bind((SERVERHOST,SERVERPORT))  ## bind server socket to port
    serverSocket.listen(1)                      ## allow just one pending client connect

    ## call handlers
    dispatcher(serverSocket)    ## start accepting incoming connections


def handleClient(connection, serverSocket):
    ''' receive and perform wildcard query from client '''
    request = connection.recv(1024)         ## accept query from the connection 
    num_matches, matches, query = performQuery(request)     ## perform and unpack the received query
    sendResponse(serverSocket, connection, num_matches, matches, query)   ## send response through the connection
    connection.close()                      ## close connection after just one query

def performQuery(request):
    ''' unpack and perform wildcard query logic '''

    ## decode query
    request = request.decode()                ## convert query to ASCII
    print(f'received request:\n{request}\n')

    ## unpack query
    query_string = request.split('\n')           ## separate headers in the request
    qbytes = int(query_string[1].split(': ')[1]) ## get number of bytes (query length)
    query1 = query_string[0][-qbytes:]            ## get the last qbytes characters as query
    query = query1.replace("?", ".")
    query = f'{query}'
    # query = re.escape(query, special_only=False)                    ## so regex characters don't break query
    
    ## note: we don't need to do anything with Connection-type, since we only support
    ## single-request queries for this assignment

    # print(query, qbytes)

    ## get words that match the regex query expression
    matches_tf = DF.str.contains(query, case=False) ## perform regex for series (true/false) object  
    # x = re.findall(query, DF.str)
    # print(x)

    # print(query)
    # matches = DF.str.extractall(r'query')
    # num_matches = len(matches)

    num_matches = matches_tf.sum()                  ## count number of matches in series

    matches = DF[matches_tf.fillna(False)]          ## get series containing all matching words
    print(matches.values)

    # print(len(matches_tf.notna()))
    # print(len(matches_tf))
    # print(len(DF))
    ## output and return result
    print(f'found {num_matches} matches for {query}.')  
    # print(len(matches))
    return num_matches, matches.values, query1

def sendResponse(serverSocket, connection, num_matches, matches, query):
    ''' send query response to client '''
    rcode = 00  ## no matches found, default
    rmsg = 'No matches found'
    if num_matches > 0:
        rcode = 11  ## matches found
        rmsg = f'Success: Found {num_matches} matches for {query}.'
    resp_msg = f'Code {rcode}\n{rmsg}\n{matches}'

    ## send query through the server socket            
    connection.sendall(resp_msg.encode('utf-8')) 
    

def dispatcher(serverSocket):
    ''' accept connections from clients '''
    print("\nserver started successfully!")
    while True:                                     ## wait for next connection
        print("\nwaiting for connections...", end=' ')
        connection, address = serverSocket.accept() ## accept connection
        print(f"server connected to {address}\n")     ## output connection info
        handleClient(connection, serverSocket)                    ## pass off to handleClient
        

startServer()


