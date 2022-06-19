import time
import socket
import os
import time

class Server():
    
    last_response_time: float

    def run(self):
        last_response_time = time.time()
        host = ''
        port = 4567
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5) 
        while True:
            print('Connecting...')
            csock, caddr = sock.accept() # this while loop waits connection
            print("Connection from: " + str(caddr))
            last_response_time = time.time()

            req = csock.recv(1024)  # get the request, 1kB max
            print(req)

            filename = 'index.html'
            f = open(filename, 'r')
            csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
            csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
            csock.send(str.encode('\r\n'))
            for l in f.readlines():
                print('Sent ', repr(l))
                csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
                l = f.read(1024)
            f.close()
            csock.close() # http://localhost:1234/ => Congratulations! The HTTP Server is working!


import http.server

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        path: str = self.translate_path(self.path) # C:\Users\user\Desktop\notes\mipt4\repos\xukechun\Recreate_v2\PythonApplication1\PythonApplication1/
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("My mes!\n".encode())
        length: int = int(self.headers['Content-Length'])
        NewData: str = self.rfile.read(length)
        #print('in', self.request)
        print('REQUEST==',NewData)

def built_in_with_put():
    http.server.test(HandlerClass=HTTPRequestHandler, port=4567, bind='127.0.0.1')

if __name__ == '__main__':
    #built_in_with_put()
    s = Server()
    s.run()
    print('after server')
