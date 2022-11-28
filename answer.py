import socket
import stat
import datetime
from pathlib import Path
import logging
import os
import sys
import argparse
from threading import Thread


class ClientRequestThread(Thread):
    def __init__(self, port, host, request_string, root_dir):
        '''
        :param port: port number on which app runs
        :param host: default value is localhost
        :param request_string: Client requested string
        :param root_dir: directory on which all the necessary files exist
        '''
        Thread.__init__(self)
        self.PORT = port
        self.HOST = host
        self.request_string = request_string
        self.root_dir = root_dir
        self.path = ''
        self.response = None
        self.status_code = ''
        self.thread_header = ''
        print("New Thread created to handle a request %s at %s:%s" %(request_string,  host,port))

    def run(self):
        '''
        Thread's main functionality
        Check's for the request type and serves the request based on factors like
        availability of string in the file, validity of the request and accessibility to the file.
        :return: None
        '''
        self.request_string = self.request_string.lstrip('/')
        if self.request_string == '':
            print("Please input a string to search for")  # Ensures the user doesnot input an empty string to search for
        self.path = self.root_dir + self.request_string
        
        try:
            # looks for string in the file and returns it
            if self.request_string != '' and (self.request_string in self.path):
                check_file_exists = Path(self.path)
                if not check_file_exists.is_file():
                    self.status_code = open_file(self.path)
                    if self.status_code != 200:
                        raise Exception()

            # Check if client has access to search for the given file if not pass 403
            if is_group_readable(self.path):
                read_file = open(self.path, 'rb')
                self.response = read_file.read()
                read_file.close()
                file_length = os.path.getsize(self.path)
                self.thread_header = 'HTTP/1.1 200 OK\n'
                self.thread_header += 'Content-Length: ' + str(file_length) + '\n'
            else:
                self.status_code = 403
                raise Exception()

        except Exception as e:
            # serve 400 status code
            if self.status_code == 400 or self.status_code == "" :
                self.thread_header = 'HTTP/1.1 400 Bad Request\n'
                self.thread_header += 'Content-Type: ' + '' + '\n'
                self.thread_header += 'Content-Length: ' + str(0) + '\n'
                self.response = '<html><body><center><h3>Error 400: Bad Request</h3><p>Python HTTP ' \
                                'Server</p></center></body></html>'.encode('utf-8')
            # serve 403 status code
            elif self.status_code == 403:
                self.thread_header = 'HTTP/1.1 403 Permission denied\n'
                self.thread_header += 'Content-Type: ' + '' + '\n'
                self.thread_header += 'Content-Length: ' + str(0) + '\n'
                self.response = '<html><body><center><h3>Error 403: Permission denied</h3><p>Python HTTP ' \
                                'Server</p></center></body></html>'.encode('utf-8')

            # serve 404 status code
            elif self.status_code == 404:
                self.thread_header = 'HTTP/1.1 404 Not Found\n'
                self.thread_header += 'Content-Type: ' + '' + '\n'
                self.thread_header += 'Content-Length: ' + str(0) + '\n'
                self.response = '<html><body><center><h3>Error 404: Not Found</h3><p>Python HTTP ' \
                                'Server</p></center></body></html>'

        finally:
            # After checking all factors send the header to notify client
            self.thread_header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'
            print("HEADERS:", self.thread_header)
            final_response = self.thread_header.encode('utf-8')
            if isinstance(self.response, str):
                self.response = self.response.encode('utf-8')
            final_response += self.response
            connection.send(final_response)
            connection.close()


def is_group_readable(file_path):
    '''
    :param file_path: requested client file
    :return: if user has access return True else False
    '''
    st = os.stat(file_path)
    return bool(st.st_mode & stat.S_IRGRP)


def open_file(path):
    '''
    Get only functions in the config path whose path starts with linuxpath
    Create an empty array and append all values gotten from the array
    '''
    files = []
    with open(path, 'wb') as handler:
        for file in handler:
            if file.startswith("linuxpath="):
                files.append(file)
    return files

def Reread_on_query(request_file, path):
    '''
    Param: request_file - input file gotten from the user
    Is the request_file contained in the file path
    print yes if it is contained else return No
    '''
    if request_file in path:
        print("String exists\n")
        return True
    else:
        print("String not found\n")
        return False

# Stripping extra payload off, client_socket is the socket of our user 
# that we are receiving information from
def handle_client(client_socket):
    '''
    :Param: receive a request from the
    if it is more than the maximum input, tell the user 
    '''
    try:
        bufSize = 1024
        request = client_socket.recv(1024).decode()
        if not len(request):
            print("Attempting to crash the server")
            return False
        #Decoding the length of our request after removing all spaces
        requestLength = int(request.strip()).decode()
        # if the length of the request is more than the bufSize, 
        # remove any extra characters from the end of the string
        if requestLength > bufSize:
            request.rstrip(requestLength-bufSize)
    except:
        return False

def parse_arguments():
    '''
    Parse document root and port value from commandline
    :return: arguments parsed from the commandline
    '''
    parser = argparse.ArgumentParser(description='Start a web server on port 44445')
    parser.add_argument('-document_root', dest='DOCUMENT_ROOT', action='store', help='Root location',
                        default='/Users/Sarima/Projects/')
    parser.add_argument('-PORT', dest='PORT', type=int, default='44445')
    result = parser.parse_args()
    return result



args = parse_arguments()
DOCUMENT_ROOT = args.DOCUMENT_ROOT
PORT = args.PORT
HOST = ''

logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s,%(levelname)s:%(message)s", 
    datefmt="%d-%m-%Y %H:%M:%S",
)

'''
Setup a socket connection with client, bind it to the port and host
'''
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    try:
        my_socket.bind((HOST, PORT))
    except socket.error as msg:
        print("Bind failed. Error code: " + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print("Socket bind complete")
    my_socket.listen(1)
    print("Socket is currently active and listening to requests")
except:
    print("Please try reconnecting to the server")
    sys.exit(1)

threads = []
header = ''

print('Serving on port ', PORT)

'''
Initiate forever loop to accept client requests
'''
while True:
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')  # Split request from spaces
    method = string_list[0]
    if request != '' and (Reread_on_query == True):
        requesting_file = "String Found"
    else:
        requesting_file = 'String Not Found'
    print('Client request ', method, requesting_file)

    if method == 'GET' or method == 'HEAD':
        newClientThread = ClientRequestThread(PORT, HOST, requesting_file, DOCUMENT_ROOT)
        newClientThread.start()
        threads.append(newClientThread)
    else:
        ''' If method type is anything other than get or head throw 500 error'''
        print("Status : 500 - Not Implemented %s method." % method)
        header = "HTTP/1.0 501 Not Implemented"
        header += 'Content-Length: ' + str(0) + '\n\n'
        header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'
        print("HEADERS: ", header)
        header = header.encode('utf-8')
        connection.send(header)
        connection.close()

    for t in threads:
        t.join()
