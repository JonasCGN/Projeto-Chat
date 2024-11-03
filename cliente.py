import socket
import sys

SERVER_POST = 9000
BUFFER = 1024
ADDRESS = "127.0.0.1"


class Cliente:

    def enviar_mensagem(self, address):
        while True:
            username = input("Username: ")
            if username != "":
                mensagem = input("Voce: ")

                if mensagem != "":
                    mensagem = f"{username}, {mensagem}"

                    address.send(bytes(mensagem, "utf-8"))
                    if mensagem == "exit":
                        print("Conexão encerrada")
                    break
            else:
                print("Username inválido")

    def escutar_mensagem(self, address):
        while True:
            recv_msg = address.recv(BUFFER).decode("ascii")

            if recv_msg != "":
                if recv_msg == "exit":
                    print("Conexão encerrada")
                    break
                else:
                    print(f"Server: {recv_msg}")
                    break

    def enviar_e_escutar_mensagem(self, address):

        while True:
            self.enviar_mensagem(address)
            self.escutar_mensagem(address)


def start_connection(ip_address):

    tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        destination = (ip_address, SERVER_POST)
        tcp_connection.connect(destination)
        name = input("Seu username: ")
        tcp_connection.send(bytes(name, "utf-8"))
    except ConnectionError as error:
        print("Conexão encerrada\nErro:", error)

    return tcp_connection


def close_connection(tcp_connection):
    tcp_connection.close()

def conversation(tcp_connection):

    cliente = Cliente()
    cliente.enviar_e_escutar_mensagem(tcp_connection)

    close_connection(tcp_connection)


if __name__ == "__main__":

    print("Conexão iniciada")
    tcp_connection = start_connection(ADDRESS)
    conversation(tcp_connection)

    try:
        close_connection(tcp_connection)
    except ConnectionError as error:
        print("Conexão encerrada\nErro:", error)
