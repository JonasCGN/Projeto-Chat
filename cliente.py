import socket
import sys

# ADDRESS = "0.tcp.sa.ngrok.io"
# SERVER_POST = 18622
SERVER_POST = 9000
BUFFER = 1024
ADDRESS = "127.0.0.1"

class Cliente:

    def __init__(self):
        self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""
        self.ativo = True
        
    def __call__(self):
        try:
            destination = (ADDRESS, SERVER_POST)
            self.tcp_connection.connect(destination)

            while True:
                self.name = input("Seu username: ")
                if self.name != "":
                    break

            self.tcp_connection.send(bytes(self.name, "utf-8"))
            self.escutar_mensagem(self.tcp_connection)
            
            self.menu()

        except ConnectionError as error:
            print("Conexão encerrada\nErro:", error)
            sys.exit()

    def enviar_mensagem(self, address):
        try:
            address.settimeout(2)
            msg_recebida: str = address.recv(BUFFER).decode()

            if msg_recebida == 'banned':
                self.ativo = False
                address.close()

        except (socket.timeout, OSError):
            while True:
                username = input("Username: ")
                if username != "":
                    mensagem = input("Voce: ")

                    if mensagem != "":
                        mensagem = f"{username}, {mensagem}"
                        address.send(bytes(mensagem, "utf-8"))
                        
                        break
                else:
                    print("Username inválido")

    def escutar_mensagem(self, address):
        try:
            address.settimeout(2)
            recv_msg = address.recv(BUFFER).decode("ascii")

            if recv_msg == 'banned':
                self.ativo = False
                address.close()

            else:
                if recv_msg != "":
                    if recv_msg == "exit":
                        print("Conexão encerrada")
                    else:
                        if recv_msg == "accept":
                            print("Conexão aceita")
                        else:
                            print(f"Server: {recv_msg}")
        except (socket.timeout, OSError):
            print("Tempo limite excedido")

    def enviar_e_escutar_mensagem(self, address):
        self.enviar_mensagem(address)
        self.escutar_mensagem(address)

    def close_connection(self, address):
        address.send(bytes(f"{self.name}, exit", "utf-8"))
        address.close()

    def menu(self):
        while True:
            if not self.ativo:
                print(f"Voce foi BANIDO!!!!")
                return
        
            print("1 - Enviar mensagem")
            print("2 - Escutar mensagem")
            print("3 - Enviar e Escutar mensagem")
            print("0 - Sair")

            option = input("Opção: ")

            if option == "0":
                self.close_connection(self.tcp_connection)
                break
            elif option == "1":
                self.enviar_mensagem(self.tcp_connection)
            elif option == "2":
                self.escutar_mensagem(self.tcp_connection)
            elif option == "3":
                self.enviar_e_escutar_mensagem(self.tcp_connection)
            else:
                print("Opção inválida")

if __name__ == "__main__":

    Cliente()()
