import socket
import threading
import logging
import argparse

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
    """Função para lidar com o cliente conectado ao servidor"""
    logging.info(f"Conexão estabelecida com {addr}")
    try:
        conn.sendall(b"Bem-vindo ao servidor! Digite sua mensagem.\n")
        while True:
            data = conn.recv(1024)
            if not data:
                logging.info(f"Cliente {addr} desconectado.")
                break
            logging.info(f"Mensagem recebida de {addr}: {data.decode()}")

            # Envia confirmação de recebimento ao cliente
            conn.sendall(b"Mensagem recebida. Envie outra ou digite 'sair' para encerrar.\n")

            if data.decode().strip().lower() == 'sair':
                logging.info(f"Cliente {addr} encerrou a conexão.")
                break
    except Exception as e:
        logging.error(f"Erro ao lidar com o cliente {addr}: {e}")
    finally:
        conn.close()

def send_message_to_server(host, port):
    """Função para enviar mensagens para outro servidor"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)  # Define um timeout de 10 segundos para as operações

    try:
        client.connect((host, port))  # Conecta ao outro servidor
        logging.info(f"Conectado ao servidor {host}:{port}")

        while True:
            message = input("Digite a mensagem para o outro servidor (ou 'sair' para encerrar): ")
            client.sendall(message.encode())
            
            if message.lower() == 'sair':
                logging.info("Encerrando conexão com o servidor remoto.")
                break
            
            # Recebe resposta do outro servidor
            data = client.recv(1024)
            logging.info(f"Resposta do servidor remoto: {data.decode()}")
            
    except socket.timeout:
        logging.error("Timeout ao tentar se conectar ao servidor remoto.")
    except ConnectionRefusedError:
        logging.error(f"Conexão recusada pelo servidor {host}:{port}")
    except Exception as e:
        logging.error(f"Erro ao se comunicar com o servidor remoto: {e}")
    finally:
        logging.info("Conexão com o servidor remoto encerrada.")
        client.close()

def start_server(host, port):
    """Função para inicializar o servidor TCP com suporte a múltiplos clientes"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    logging.info(f"Servidor iniciado e escutando em {host}:{port}")

    while True:
        try:
            conn, addr = server.accept()
            logging.info(f"Nova conexão de {addr}")

            # Cria uma nova thread para cada cliente conectado
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        except KeyboardInterrupt:
            logging.info("Servidor interrompido pelo usuário.")
            break
        except Exception as e:
            logging.error(f"Erro no servidor: {e}")
            continue

    server.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor TCP com comunicação bidirecional")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Endereço IP do servidor')
    parser.add_argument('--port', type=int, default=12345, help='Porta do servidor')
    parser.add_argument('--remote_host', type=str, help='Endereço IP do outro servidor')
    parser.add_argument('--remote_port', type=int, help='Porta do outro servidor')

    args = parser.parse_args()

    # Inicia o servidor
    server_thread = threading.Thread(target=start_server, args=(args.host, args.port))
    server_thread.start()

    # Se os parâmetros de outro servidor forem fornecidos, envia mensagem para ele
    if args.remote_host and args.remote_port:
        send_message_to_server(args.remote_host, args.remote_port)
