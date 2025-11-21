import socket
import threading
from collections import deque
from commands import Commands
from utils import printc, bcolors

# Configurações
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024
HISTORY_SIZE = 100 # N mensagens no histórico 

# Estruturas globais
clients = {}  # Dicionário: {socket: nome_usuario}
message_history = deque(maxlen=HISTORY_SIZE) # Buffer circular para histórico

def broadcast(message, sender_socket=None):
    """Envia mensagem para todos, exceto o remetente (opcional)"""
    for client_sock in list(clients.keys()):
        if client_sock != sender_socket:
            try:
                client_sock.send(message.encode('utf-8'))
            except:
                # Se falhar ao enviar, assume que cliente caiu
                remove_client(client_sock)

def remove_client(client_socket):
    if client_socket in clients:
        name = clients[client_socket]
        del clients[client_socket]
        client_socket.close()
        printc(f"Client {name} desconectado.", bcolors.WARNING)
        broadcast(f"Servidor: {name} saiu do chat.")

def handle_client(client_socket, client_address):
    """Função executada em uma Thread separada para cada cliente"""
    printc(f"Nova conexão TCP de {client_address}", bcolors.OKCYAN)
    
    username = "Anônimo"
    
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            
            msg_decoded = data.decode('utf-8')
            
            # Lógica de comandos 
            parts = msg_decoded.split(' ', 1)
            command = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            if command == Commands.CONNECT:
                username = content
                clients[client_socket] = username
                printc(f"Usuário registrado: {username}", bcolors.OKGREEN)
                
                # 1. Enviar Histórico 
                if len(message_history) > 0:
                    hist_msg = "\n--- Histórico das últimas mensagens ---\n"
                    for m in message_history:
                        hist_msg += m + "\n"
                    hist_msg += "---------------------------------------"
                    client_socket.send(hist_msg.encode('utf-8'))
                
                # Avisar os outros
                broadcast(f"Servidor: {username} entrou na sala!", client_socket)

            elif command == Commands.SEND:
                # Formata a mensagem
                final_msg = f"{username}: {content}"
                
                # 2. Adicionar ao Buffer de Histórico 
                message_history.append(final_msg)
                
                # 3. Broadcast 
                broadcast(final_msg, client_socket)
                print(f"Broadcast de {username}: {content}")

            elif command == Commands.DISCONNECT:
                break
                
    except Exception as e:
        printc(f"Erro com cliente {client_address}: {e}", bcolors.FAIL)
    finally:
        remove_client(client_socket)

def start_server():
    # Cria socket TCP (SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    printc(f"Servidor TCP rodando em {HOST}:{PORT}", bcolors.HEADER)
    printc(f"Histórico configurado para {HISTORY_SIZE} mensagens.", bcolors.OKBLUE)

    while True:
        # Aceita novas conexões (bloqueante)
        client_sock, addr = server.accept()
        
        # Cria uma thread para cuidar desse cliente
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()
        print(f"Total de threads ativas: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()