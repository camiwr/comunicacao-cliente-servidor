import socket
import threading
import logging
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
# cada cliente em uma thread separada
    logging.info(f"Conexão estabelecida com {addr}")
    try:
        conn.sendall(b"Bem-vindo ao servidor! Digite sua mensagem.\n")
        while True:
            data = conn.recv(1024)
            if not data:
                logging.info(f"Cliente {addr} desconectado.")
                break
            logging.info(f"Mensagem recebida de {addr}: {data.decode()}")
            conn.sendall(b"Mensagem recebida. Envie outra ou digite 'sair' para encerrar.\n")

            if data.decode().strip().lower() == 'sair':
                logging.info(f"Cliente {addr} encerrou a conexão.")
                break

    except Exception as e:
        logging.error(f"Erro ao lidar com o cliente {addr}: {e}")
    finally:
        conn.close()

# servidor TCP
def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    logging.info(f"Servidor iniciado e escutando em {host}:{port}")

    while True:
        try:
            conn, addr = server.accept()
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
    parser = argparse.ArgumentParser(description="Servidor TCP")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Endereço IP do servidor')
    parser.add_argument('--port', type=int, default=12345, help='Porta para o servidor escutar')

    args = parser.parse_args()

    start_server(args.host, args.port)

# python server.py --host 127.0.0.1 --port 12345
