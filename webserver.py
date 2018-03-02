# https and http multithreaded webserver
import logging
import os.path
import ssl
import threading
from socket import *
from threading import _start_new_thread

from utils import *

SSL_PORT = 8890  # ssl sport
HTTP_PORT = 8899  # http sport
BUFFER_SIZE = 4096

# define logging
logging.basicConfig(filename="webserver.log", format='%(asctime)s %(message)s', level=logging.DEBUG)

# http socket
httpServerSocket = socket(AF_INET, SOCK_STREAM)
httpServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
httpServerSocket.bind(('', HTTP_PORT))
httpServerSocket.listen()
logging.info("INFO   HTTP server is running on port 8899")

# https socket
sslServerSocket = socket(AF_INET, SOCK_STREAM)
sslServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sslServerSocket.bind(('', SSL_PORT))
sslServerSocket.listen()
ssl_socket = ssl.wrap_socket(sslServerSocket, server_side=True, certfile="ssl/myCert.cert", keyfile="ssl/myKey.key")
logging.info("INFO   HTTPS server is running on port 8890")


def sendResponse(header, connectSocket, address):  # parse request header and send response in a thread
    try:
        st = str(header).split("\n")[0]
        st1 = st.split(" ")
        filePath = st1[1]
        method = st1[0]
        # log request
        logging.info("INFO  " + method + " " + address + " " + filePath)
        if method == 'GET':
            if filePath == "/":  # index
                mFile = "root/index.html"
            else:
                mFile = "root/" + filePath

            if os.path.exists(mFile):  # file exists read and decide content-type
                file = open(mFile, "rb")
                fileContentBytes = file.read()
                header = SUCCESS_HEADER % (CONTENT_TYPES[os.path.splitext(mFile)[1]], str(len(fileContentBytes)))
                connectSocket.send(header.encode())  # send header
                connectSocket.send(fileContentBytes)  # send body
                file.close()
            else:  # not found
                header = NOT_FOUND_HEADER
                connectSocket.send(header.encode())
        else:
            connectSocket.send(POST_UNSUPPORTED_HEADER.encode())
    except Exception as e:
        # raise e
        logging.error("ERROR  " + address + "  connection failed")
    finally:
        connectSocket.close()


def listenHttp():
    while True:
        httpConnectSocket, httpAddr = httpServerSocket.accept()
        if httpAddr is not None and httpConnectSocket is not None:
            print("http connection ...........................................")
            header = httpConnectSocket.recv(BUFFER_SIZE).decode()
            _start_new_thread(sendResponse, (header, httpConnectSocket, httpAddr[0]))


def listenSSL():
    while True:
        httpsConnectSocket, sslAddr = ssl_socket.accept()
        if sslAddr is not None and httpsConnectSocket is not None:
            print("ssl connection ...........................................")
            header = httpsConnectSocket.recv(BUFFER_SIZE).decode()
            _start_new_thread(sendResponse, (header, httpsConnectSocket, sslAddr[0]))


# two threads running at the same time
# parrellel excution for 2 infinate loops
t1 = threading.Thread(target=listenSSL)
t2 = threading.Thread(target=listenHttp)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
t1.join()
t2.join()
