import socket
import threading
from tkinter import messagebox


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 12345))
        self.server_socket.listen(2)
        print("Server listening on port 12345")

    def server_close(self):
        self.server_socket.close()

    def receive(self):
        recv_thread = threading.Thread(target=self.recv_from_client, daemon=True)
        recv_thread.start()

    def send(self, message):
        send_thread = threading.Thread(target=self.send_to_client, daemon=True, args=(message,))
        send_thread.start()

    def recv_from_client(self):
        message = ""
        while True:
            client_socket, client_addr = self.server_socket.accept()
            try:
                message += client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received message from {client_addr}: {message}")
            except Exception as e:
                print(f"Error handling client {client_addr}: {str(e)}")
                break

        client_socket.close()
        return message

    def send_to_client(self, message):
        while True:
            messagebox.showinfo("分享密钥", "发送中，请关闭此窗口以等待...")
            client_socket, client_addr = self.server_socket.accept()
            try:
                client_socket.send(bytes(message, 'utf-8'))
                messagebox.showinfo("成功", "分享密钥成功")
                break
            except Exception as e:
                print(f"Error sending message to client: {str(e)}")
                break

        client_socket.close()
