import socket
import sys

SERVER_IP = ''
SERVER_PORT = 8080
BUFFER = 1024

def bind_to_the_server():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((SERVER_IP, SERVER_PORT))
    tcp_server.listen(1)
    
    return tcp_server

def client_confirmation(tcp_connection):
    
    connection, address = tcp_connection.accept()
    print(f'Conexão estabelecida com {address}')
    return connection, address

def close_connection(tcp_connection):
    tcp_connection.close()

def listening(tcp_connection, addres):
    
    while True:
        
        recv_msg = tcp_connection.recv(BUFFER).decode('ascii')
        
        if recv_msg != '':
            if recv_msg == 'exit':
                print('Conexão encerrada: Digite "exit" para sair')
            else:
                print(f'Client {addres}: {recv_msg}')
                
        mensagem = input('Voce: ')
        
        if mensagem != '':
            if mensagem != 'exit':
                tcp_connection.send(bytes(mensagem, 'utf-8'))
            else:
                
                break
            
    close_connection(tcp_connection)
        
if __name__ == '__main__':
    
    tcp_server = bind_to_the_server()
    connection, address = client_confirmation(tcp_server)
    listening(connection, address)
    
    close_connection(tcp_server)
    sys.exit()