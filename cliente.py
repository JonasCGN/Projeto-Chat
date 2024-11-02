import socket
import sys

SERVER_POST = 8080
BUFFER = 1024

def connecting():
    
    value = input('Digite o endereço de IP: ')
    
    return start_connection(value)

def checking_ip_address(ip_address):
    
    if len(ip_address) == 9 and ip_address is not None:
        return True
    
    print('Endereço de IP inválido')
    exit()
    
def start_connection(ip_address):
    
    checking_ip_address(ip_address)
    tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        destination = (ip_address, SERVER_POST)
        tcp_connection.connect(destination)
    except ConnectionError as error:
        print('Conexão encerrada\nErro:', error)
        
    return tcp_connection

def close_connection(tcp_connection):
    tcp_connection.close()
    
def conversation(tcp_connection):
        
        while True:
            mensagem = input("Voce: ")
            
            if mensagem != '':
                tcp_connection.send(bytes(mensagem, 'utf-8'))
                if mensagem == 'exit':
                    print('Conexão encerrada')
                    break
            
            recv_msg = tcp_connection.recv(BUFFER).decode('ascii')
            
            if recv_msg != '':
                if recv_msg == 'exit':
                    print('Conexão encerrada')
                    break
                else:
                    print(f'Server: {recv_msg}')
    
        close_connection(tcp_connection)     
        
if __name__ == '__main__':
    
    print('Conexão iniciada')
    tcp_connection = connecting()
    conversation(tcp_connection)
    
    try:
        close_connection(tcp_connection)
    except ConnectionError as error:
        print('Conexão encerrada\nErro:', error)