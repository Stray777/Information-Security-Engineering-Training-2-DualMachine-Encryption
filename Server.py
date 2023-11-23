import socket
from threading import Thread


class Server:
    def __init__(self):
        self.client_sockets = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 12345))
        self.server_socket.listen(5)
        print("Server listening on port 12345")

    def start(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print(f"Accepted connection from {client_addr}")
            self.client_sockets.append(client_socket)
            client_thread = Thread(target=self.handle_client, args=(client_socket, client_addr))
            client_thread.start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received message from {addr}: {message}")
                self.send_to_client(client_socket, message)
            except Exception as e:
                print(f"Error handling client {addr}: {str(e)}")
                break

        self.client_sockets.remove(client_socket)
        client_socket.close()

    @staticmethod
    def send_to_client(client_socket, message):
        try:
            client_socket.send(bytes(message, 'utf-8'))
        except Exception as e:
            print(f"Error sending message to client: {str(e)}")

    # def broadcast(self, message, sender_socket):
    #     for client in self.client_sockets:
    #         if client != sender_socket:
    #             try:
    #                 client.send(bytes(message, 'utf-8'))
    #             except Exception as e:
    #                 print(f"Error broadcasting message: {str(e)}")
    #                 self.client_sockets.remove(client)
    #                 client.close()
