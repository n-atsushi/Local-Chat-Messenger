import socket
import os
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = './socket_file'
fake = Faker()

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:       
        print('connection from', client_address)
        
        data = connection.recv(128)
        data_str =  data.decode('utf-8')
        print('Received ' + data_str)
        
        connection.sendall('== TYPE: name or address or text =='.encode())
        
        while True:
            data = connection.recv(128)
            data_str =  data.decode('utf-8')
        
            print('Received ' + data_str)
            
            fake_hash = {
                'name' : fake.name(),
                'address' : fake.address(),
                'text' : fake.text()
            }

            if data:
                response = 'nothing'
                if data_str in fake_hash:
                    response = fake_hash[data_str]
                    
                connection.sendall(response.encode())
            else:
                print('no data from', client_address)
                break
    finally:
        print("Closing current connection")
        connection.close()