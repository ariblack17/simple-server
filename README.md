# simple-server

## Overview

A few basic implementations of a simple client/server model, where the client queries the server for a pattern of characters and the server responds with
the number of matching words in the locally stored text file, as well as an array of all matching words.

The client's query may include a wildcard character (?), which indicates that the given single character can be any single member of the ASCII library.

The application's request/response protocol is roughly similar to that of HTTP, such that the client must send a request with a given keyword and query and the server must respond with a status code, status message, and optional body.
