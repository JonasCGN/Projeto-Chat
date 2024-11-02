#  Implementação de um chat básico:
#  ○ Deve ter no mínimo 3 clientes;
#  ○ Deverá ter dois códigos diferentes, o do servidor e do cliente;
#  ○ O Cliente terá um menu onde ele irá escolher o que ele deseja fazer:
# ■ Escutar até receber uma mensagem, depois ele volta para o menu;
#  ■ Apenas escutar mensagens e mostrar na tela;
#  ■ Sair.
#  ■ Mandar mensagem para 1 cliente informando a qual cliente que ele deseja mandar a
# mensagem;
#  ■ Enviar mensagem e escutar a resposta e depois voltar ao menu;
#  ○ O servidor deverá censurar mensagens indevidas (as palavras são definidas pelo grupo).
#  ○ Caso o cliente mande 3 mensagens indevidas no período de 1 minuto, ele deve ser banido e as
# mensagens dele não serão mais transmitidas.
import socket
import threading


class Servidor:
    palavras_banidas = ["buceta", "caralho", "pika", "rolão"]
    host = ""
    port = 9000

    def __init__(self):
        self.addr = (self.host, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []
        self.banidos = []

    def __call__(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(10)

        threading.Thread(target=self.thread_connect_users).start()

    def tread_msg_users(self, cliente_socket: socket.socket, client_addr):

        while True:
            try:
                data = cliente_socket.recv(1024)
                text_data = data.decode()
                print(f"{client_addr}: {text_data}")
                cliente_socket.send("Mensagem Recebida!".encode())
            except ConnectionAbortedError:
                print(f"{client_addr}: Desconectado (abort)")
                break
            except ConnectionResetError:
                print(f"{client_addr}: Desconectado (reset)")
                break

    def thread_connect_users(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            if len(self.clientes) < 10:
                self.clientes.append(client_socket)
                print(f"Cliente {client_addr} conectado.")
                threading.Thread(
                    target=self.tread_msg_users, args=(client_socket, client_addr)
                ).start()
            else:
                print(f"Cliente {client_addr} recusado. Limite de conexões atingido.")
                client_socket.close()


if __name__ == "__main__":
    Servidor()()
