import time
import socket
import os
import time
import threading

class Server():
    
    last_response_time: float = 0 # pause after last message was received
    message_default = 'connection check'
    message_to_send = ''

    host = '127.0.0.1'
    port = 4567


    #def __init__(self):
    #    pass

    @staticmethod
    def connect():
        # thread 2 - like coroutine
        action_thread = threading.Thread(target=Server._loop); action_thread.daemon = True; action_thread.start()  # daemon - thread will stop when main process exits # actually run coroutine, starts right now (not in next frame!)
        
        # main thread - wait connection
        print('Connecting to socket:', Server.host, Server.port)
        while True:
            if Server.last_response_time > 0:
                print('Connected')
                break
         

    @staticmethod
    def _loop():
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((Server.host, Server.port))
            sock.listen(1) 

            csock, caddr = sock.accept() # this while loop waits connection
            Server.last_response_time = time.time()

            req = csock.recv(1024)  # get the request, 1kB max
            print('question == ', req)

            #send html to client
            filename = 'index.html'
            f = open(filename, 'r')
            csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
            csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
            csock.send(str.encode('\r\n'))
            for l in f.readlines():
                csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
                l = f.read(1024)
            f.close()

            csock.sendall(str.encode("received",'iso-8859-1'))

            print('answered', time.time())
            #csock.close() # <- this was a reason of many errors!!! Not receiving message. http://localhost:1234/ => Congratulations! The HTTP Server is working!
            #sock.shutdown(0)
            #sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            del sock


    @staticmethod
    def check_connection(_MaxPause = 3):
        """If client does not respond N sec, we will get a warning"""
        #print('last_response_pause=', time.time() - s.last_response_time)
        if  time.time() - Server.last_response_time > _MaxPause:
            #print('Warning: connection was lost for', _MaxPause, 'sec')
            pass
        else:
            #print('ok')
            pass


if __name__ == '__main__':
    #built_in_with_put()
    #send_old_style()
    print('after server')




"""
# send html to client
filename = 'index.html'
f = open(filename, 'r')
csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
csock.send(str.encode('\r\n'))
for l in f.readlines():
    #print('Sent ', repr(l))
    csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
    l = f.read(1024)
f.close()
#            Hello html!
#<div>Hi! I am html.</div>
# send command to client
#csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
#csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
#csock.send(str.encode('\r\n'))
"""


#import socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(('localhost', 50000))
#s.listen(1)
#conn, addr = s.accept()
#while 1:
#    data = conn.recv(1024)
#    if not data:
#        break
#    conn.sendall(data)
#conn.close()



    #@staticmethod
    #def _loop_legacy():

    #    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    sock.bind((Server.host, Server.port))
    #    sock.listen(1) 
    #    #csock, caddr = sock.accept() # this while loop waits connection

    #    while True:
    #        time.sleep(0.1)

    #        csock, caddr = sock.accept() # this while loop waits connection
    #        # 1) connect, accept loop pauses thread until connection is done
    #        #print("Connection from: " + str(caddr))
    #        Server.last_response_time = time.time()

    #        # 2) get question
    #        #req = csock.recv(1024)  # get the request, 1kB max
    #        req = csock.recv(1024)  # get the request, 1kB max
    #        #print('question == ', req)

    #        #encoding = 'utf-8'
            
    #        #print('question == ', unicode(req, encoding))

    #        res = req.decode("utf-8").splitlines()
    #        received: bool = (len(res) == 9)
    #        print('question == ', type(res), len(res), 'last=', res[-1]  )
    #        print()

    #        # 3) send answer
    #        # send sanity check message (each loop)
    #        #csock.sendall(str.encode(Server.message_default, 'iso-8859-1'))
    #        #print('message is sent')

    #        # send html to client
    #        filename = 'index.html'
    #        f = open(filename, 'r')
    #        csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
    #        csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
    #        csock.send(str.encode('\r\n'))
    #        for l in f.readlines():
    #            #print('Sent ', repr(l))
    #            csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
    #            l = f.read(1024)
    #        f.close()
    #        #print('answered')
    #        csock.sendall(str.encode('received='+str(received), 'iso-8859-1'))
    #        print()


    #        # send custom message
    #        #if Server.message_to_send != '':
    #        #    csock.send(str.encode(Server.message_to_send + '\r\n'))
    #        #    Server.message_to_send = ''

    #        csock.close() # http://localhost:1234/ => Congratulations! The HTTP Server is working!
               