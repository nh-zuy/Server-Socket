import socket
import sys
import _thread

HOST = ""
LISTEN_PORT = 8888
MAX_CONNECTION = 10
BUFFER_SIZE = 8192
 
class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, LISTEN_PORT))
        self.server.listen(MAX_CONNECTION)

        print("<> Server set up successfully. Loading ... ")
        print("<> Available on port 8888 !!!\n")

    def run(self):
        while True:
            try:
                (connect, address) = self.server.accept()
                request = connect.recv(BUFFER_SIZE).decode("utf-8")
                _thread.start_new_thread(self._handleRequest, (connect, address, request))
            except KeyboardInterrupt:
                self.server.close()
                print("<!> Server closed successfully !")
                sys.exit(1)

        self.server.close()

    def _handleRequest(self, connect, address, request):

        Parts = request.split('\n')
        
        requestLine = Parts[0]

        method = requestLine.split(' ')[0]
        path = requestLine.split(' ')[1]
     
        print('<!> Client request for: ', path)
     
        requestedFile = path.split('?')[0] # After the "?" symbol not relevent here
        requestedFile = requestedFile.lstrip('/')

        if(requestedFile == ''):
            requestedFile = 'index.html'    # Load index file as default
    
        try:
            header = 'HTTP/1.1 200 OK\n'
       
            if (requestedFile != "favicon.ico"):
                if (method == "GET"):
                    response = self._readFile(requestedFile)
                elif (method == "POST"):
                    params = Parts[-1].split("&")
                    username = params[0].split('=')[1]
                    password = params[1].split('=')[1]
                    
                    if (username == "admin" and password == "admin"):
                        response = self._readFile("info.html")
                    else:
                        header = 'HTTP/1.1 404 Not Found\n\n'
                        response = self._readFile("404.html")
     
            
     
            if(requestedFile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(requestedFile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
     
            header += 'Content-Type: '+str(mimetype)+'\n\n'
     
        except Exception as error:
            print(error)
            sys.exit(1)
                 
        response_raw = header.encode('utf-8')
        response_raw += response
        connect.send(response_raw)
        connect.close()

    def _readFile(self, fileName):
        file = open(fileName,'rb') # open file , r => read , b => byte format
        data = file.read()
        file.close()
        return data;

if __name__ == "__main__":
    Server().run()
