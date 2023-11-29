from model import *
from tkinter import filedialog, messagebox
import tkinter as tk


class Controller:
    def __init__(self, view, server):
        self.server = server
        self.view = view
        self.view.set_button_file1(self.open_file)
        self.view.set_button_encrypt(self.encrypt_on_button_click)
        self.view.set_button_sharekey(self.share_click)
        self.view.set_button_send(self.send_click)

    def send_click(self):
        ciphertext = self.view.text_cipher.get("1.0", "end").strip('\n')
        self.server.send(ciphertext, 2)

    def share_click(self):
        key = self.view.entry_key1.get().strip('\n')
        self.server.send(key, 1)

    def encrypt_on_button_click(self):
        """加密按钮"""
        option = self.view.combobox_algorithm.get()
        key = self.view.entry_key1.get().strip('\n')
        if option == "Select an algorithm":
            messagebox.showerror("错误", "请选择具体算法后再点击")
        elif option == "CaesarCipher":
            try:
                key = int(key)
            except ValueError as e:
                messagebox.showerror("错误", f"CaesarCipher的key应为数字\n\n{e}")
                return None
            caesar_cipher = CaesarCipher(key)
            self.encrypt(caesar_cipher)
        elif option == "KeywordCipher":
            keyword_cipher = KeywordCipher(key)
            self.encrypt(keyword_cipher)
        elif option == "RSA":
            rsa = RSA(key)
            self.encrypt(rsa)
        elif option == "PlayfairCipher":
            playfair = PlayfairCipher(key)
            self.encrypt(playfair)
        elif option == "VigenereCipher":
            vigenere = VigenereCipher(key)
            self.encrypt(vigenere)
        elif option == "PermutationCipher":
            permutation = PermutationCipher(key)
            self.encrypt(permutation)
        elif option == "AutokeyCipher":
            autokey = AutokeyCipher(key)
            self.encrypt(autokey)
        elif option == "RC4":
            rc4 = RC4(key)
            self.encrypt(rc4)
        elif option == "DH":
            dh = DH(key)
            self.view.text_cipher.delete(1.0, tk.END)
            self.view.text_cipher.insert(tk.END, dh.kk)
        elif option == "ColumnPermutationCipher":
            column = ColumnPermutationCipher(key)
            self.encrypt(column)

    def open_file(self, button_id: int):
        """打开文本文件"""
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r') as file:
                content = file.read()
                if button_id == 1:
                    self.view.text_plaintext.delete(1.0, tk.END)
                    self.view.text_plaintext.insert(tk.END, content)
                elif button_id == 2:
                    self.view.text_ciphertext.delete(1.0, tk.END)
                    self.view.text_ciphertext.insert(tk.END, content)

    def run_view(self):
        self.view.root.mainloop()

    def encrypt(self, algorithm):
        plain_text = self.view.text_plaintext.get("1.0", "end").strip('\n')
        cipher_text = algorithm.encrypt(plain_text)
        if isinstance(algorithm, RSA):
            d = algorithm.key_d
            n = algorithm.key_n
            self.view.text_cipher.delete(1.0, tk.END)
            self.view.text_cipher.insert(tk.END, f"密钥d:{d}\n密钥n:{n}\n密文:{cipher_text}")
        else:
            self.view.text_cipher.delete(1.0, tk.END)
            self.view.text_cipher.insert(tk.END, cipher_text)
