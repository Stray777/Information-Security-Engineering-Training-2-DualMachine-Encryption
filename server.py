import socket
import threading
from tkinter import messagebox


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 12344))
        self.server_socket.listen(2)
        print("Server listening on port 12345")
        self.send_thread = None
        self.client_socket = None
        self.client_addr = None
        self.separator = '|'
        self.recv_thread = threading.Thread(target=self.recv_from_client, daemon=True)
        self.recv_thread.start()

    def server_close(self):
        self.server_socket.close()

    def send(self, message, file_id):
        self.send_thread = threading.Thread(target=self.send_to_client, daemon=True, args=(message, file_id))
        self.send_thread.start()

    def recv_from_client(self):
        while True:
            if self.client_socket is None:
                self.client_socket, self.client_addr = self.server_socket.accept()
            try:
                message1 = self.client_socket.recv(1024).decode('utf-8').split(f"{self.separator}")
                message1 = message1[0]
                message2 = self.client_socket.recv(1024).decode('utf-8').split(f"{self.separator}")
                message2 = message2[0]
                if not message1:
                    self.client_socket.close()
                    self.client_socket = None
                    self.client_addr = None
                    break
                with open(message1, 'w') as file:
                    file.write(message2)
                messagebox.showinfo("接收", f"已接收客户端传来的文件:{message1}")
            except Exception as e:
                print(f"Error handling client {self.client_addr}: {str(e)}")
                self.client_socket = None
                self.client_addr = None

    def send_to_client(self, message, file_id):
        messagebox.showinfo("发送", "发送中，请关闭此窗口以等待...")
        if self.client_socket is None:
            self.client_socket, self.client_addr = self.server_socket.accept()
        try:
            if file_id == 1:
                self.client_socket.sendall(bytes(f"key.txt{self.separator}", 'utf-8'))
            elif file_id == 2:
                self.client_socket.sendall(bytes(f"ciphertext.txt{self.separator}", 'utf-8'))
            self.client_socket.sendall(bytes(message+f"{self.separator}", 'utf-8'))
            messagebox.showinfo("成功", "发送成功")
        except Exception as e:
            print(f"Error sending message to client: {str(e)}")
