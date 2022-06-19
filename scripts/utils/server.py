import time
import socket
import os
import time
import threading

class Server():
    
    last_response_time: float = 0 # pause after last message is received
    host = '127.0.0.1'
    port = 4567


    def __init__(self):
        pass

    def connect(self):
        # thread 2
        action_thread = threading.Thread(target=self._update); action_thread.daemon = True; action_thread.start()  # daemon - thread will stop when main process exits # actually run coroutine, starts right now (not in next frame!)
        
        # main thread
        print('Connecting to socket:', self.host, self.port)
        while True:
            if self.last_response_time > 0:
                print('Connected')
                break
            
    def validate_connection_loop(self, max_pause = 3):
        """If client does not respond N sec, we will get a warning"""
        #print('last_response_pause=', time.time() - s.last_response_time)
        if  time.time() - self.last_response_time > max_pause:
            print('Warning: connection was lost for', max_pause, 'sec')
        else:
            print('connection is ok')

    def _update(self):
       
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5) 
        while True:
            csock, caddr = sock.accept() # this while loop waits connection
            #print("Connection from: " + str(caddr))
            self.last_response_time = time.time()

            req = csock.recv(1024)  # get the request, 1kB max
            #print(req)

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
            csock.close() # http://localhost:1234/ => Congratulations! The HTTP Server is working!

if __name__ == '__main__':
    #built_in_with_put()
    #send_old_style()
    print('after server')
