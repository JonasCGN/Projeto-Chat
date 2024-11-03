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
import datetime

BUFFER = 1024
HOST = ""
PORT = 9000
PALAVRAS_BANIDA = [
    "buceta", "caralho", "pika", "rolao", "cachorra", "safada", "vagabunda",
    "pih da moiangaba", "puta", "tijolinho", "amigo de o3", "emilly"
                   ]
NMR_CLIENTES = 3

class Cliente:
    def __init__(self, client_addr, cliente_socket, user_name) -> None:
        self.client_addr = client_addr
        self.cliente_socket = cliente_socket
        self.user_name = user_name
        self.palavroes:list[datetime.datetime] = []
    
    def add_palavroes(self,message):
        if message.lower() in [i.lower() for i in PALAVRAS_BANIDA]:
            self.palavroes.append(datetime.datetime.now())
    
    def palavroes_falados(self):
        fim = datetime.datetime.now()
        inicio = fim - datetime.timedelta(minutes=1)
        
        retorno = False

        resultado = [i for i in self.palavroes[-3:] if i.date() == datetime.datetime.now().date()]
        resultado = [i for i in resultado if i.time().minute >= inicio.minute and i.time().minute <= fim.minute]
        
        if len(resultado) >= 3:
            retorno = True
            
        return retorno

class Servidor:

    def __init__(self):
        self.addr = (HOST, PORT)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes: dict[Cliente] = {}
        self.banidos = []

    def __call__(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(10)

        threading.Thread(target=self.thread_connect_users).start()

    def tratamento_msg(self, cliente_socket):
        data = cliente_socket.recv(BUFFER)
        text_data: str = data.decode()
        
        name, msg = text_data.split(", ")

        for cliente in self.clientes.values():
            if cliente.user_name == name:
                self.clientes[cliente_socket].add_palavroes(msg)
                cliente.cliente_socket.send(msg.encode())

    def tread_msg_users(self, cliente_socket: socket.socket, client_addr):
        while True:
            if self.clientes[cliente_socket].palavroes_falados():
                print(f"{client_addr}: Desconectado (banned)")
                self.banidos.append(client_addr)
                break
            
            try:
                self.tratamento_msg(cliente_socket)
            except ConnectionAbortedError:
                print(f"{client_addr}: Desconectado (abort)")
                break
            except ConnectionResetError:
                print(f"{client_addr}: Desconectado (reset)")
                break
            
        self.remove_cliente(cliente_socket)

    def thread_connect_users(self):
        while True:
            log = ""

            client_socket, client_addr = self.server_socket.accept()
            if len(self.clientes) < NMR_CLIENTES:
                name = client_socket.recv(BUFFER).decode()
                
                cliente_atual = Cliente(client_addr, client_socket, name)
                self.clientes[client_socket] = cliente_atual
                
                log = f"Cliente {client_addr} conectado."
                client_socket.send("accept".encode())
                
                threading.Thread(
                    target=self.tread_msg_users, args=(client_socket, client_addr)
                ).start()
            else:
                log = f"Cliente {client_addr} recusado. Limite de conexões atingido."
                client_socket.send("exit".encode())
                client_socket.close()

            print(log)

    def remove_cliente(self, cliente):
        self.clientes.pop(cliente)
        cliente.close()
        
if __name__ == "__main__":
    Servidor()()
