import socket
import argparse
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_client(host, port):
#inicia o cliente TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)

    try:
        client.connect((host, port))
        logging.info(f"Conectado ao servidor {host}:{port}")
        data = client.recv(1024)
        logging.info(f"Mensagem recebida do servidor: {data.decode()}")

        while True:
            message = input("Digite sua mensagem (ou 'sair' para encerrar): ")
            client.sendall(message.encode())
            
            if message.lower() == 'sair':
                logging.info("Encerrando conexão com o servidor.")
                break
            
            data = client.recv(1024)
            logging.info(f"Resposta do servidor: {data.decode()}")
            
    except socket.timeout:
        logging.error("Timeout ao tentar se conectar ao servidor.")
    except ConnectionRefusedError:
        logging.error(f"Conexão recusada pelo servidor {host}:{port}")
    except Exception as e:
        logging.error(f"Erro no cliente: {e}")
    finally:
        logging.info("Cliente encerrado.")
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente TCP")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Endereço IP do servidor')
    parser.add_argument('--port', type=int, default=12345, help='Porta para se conectar ao servidor')

    args = parser.parse_args()

    start_client(args.host, args.port)

# python client.py --host 192.168.0.100 --port 8080
