import time
import socket
import os
import time
import threading

class Server():
    

    host = '127.0.0.1'
    port = 4567

    #def __init__(self):
        #pass

    @staticmethod
    def connect():
        print('Connecting to socket:', Server.host, Server.port)
        print('Connected')
       