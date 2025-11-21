import socket
import threading
import sys
from commands import Commands
from utils import printc, bcolors

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

def receive_messages(sock):
    """
    Thread que fica ouvindo mensagens do servidor.
    """
    while True:
        try:
            msg = sock.recv(BUFFER_SIZE)
            if not msg:
                # Se receber vazio, o servidor fechou a conexão
                printc("\nConexão encerrada pelo servidor.", bcolors.FAIL)
                sock.close()
                # Encerra o programa forçadamente pois a thread principal está presa no input()
                import os
                os._exit(0)
            
            # Imprime a mensagem exatamente como chegou
            print(msg.decode('utf-8'))
            
        except OSError:
            break
        except Exception as e:
            printc(f"Erro ao receber: {e}", bcolors.FAIL)
            break

def main():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_sock.connect((HOST, PORT))
    except:
        printc(f"Não foi possível conectar a {HOST}:{PORT}", bcolors.FAIL)
        return

    printc("Conectado ao servidor!", bcolors.OKGREEN)
    printc("Use os comandos do protocolo:", bcolors.HEADER)
    printc(" - CONNECT <nome>", bcolors.OKCYAN)
    printc(" - SEND <mensagem>", bcolors.OKCYAN)
    printc(" - DISCONNECT", bcolors.OKCYAN)

    # Inicia thread para receber mensagens
    recv_thread = threading.Thread(target=receive_messages, args=(client_sock,))
    recv_thread.daemon = True 
    recv_thread.start()

    while True:
        try:
            # Agora o cliente envia EXATAMENTE o que você digitar
            msg = input()
            
            if not msg:
                continue

            client_sock.send(msg.encode('utf-8'))

            # Se o usuário digitar o comando de sair, encerra o cliente localmente também
            if msg.strip() == Commands.DISCONNECT:
                client_sock.close()
                sys.exit()
                
        except KeyboardInterrupt:
            client_sock.close()
            break
        except Exception as e:
            printc(f"Erro: {e}", bcolors.FAIL)
            client_sock.close()
            break

if __name__ == "__main__":
    main()