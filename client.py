import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = './socket_file'
print('connecting to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    message = b'Sending a message to the server side'
    
    sock.sendall(message)
    sock.settimeout(60)

    try:
        data = sock.recv(128)
        data_str = data.decode('utf-8')
        if data:
            print(data_str)
        else:
            raise TimeoutError
        
        while True:
            message = input('Please input value:')
            sock.sendall(message.encode())
            
            data = str(sock.recv(128).decode('utf-8'))

            if data:
                print('Server response: ' + data)
            else:
                break

    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')

finally:
    print('closing socket')
    sock.close()