import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import base64
from Algorithm.CaesarCipher import CaesarCipher
from Algorithm.KeywordCipher import KeywordCipher
from Algorithm.RSA import RSA


class UI:
    def __init__(self, root):
        self.root = root
        # 主界面标题
        self.root.title("加解密实践-加密端")
        # 设置窗口大小和居中
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"400x400+{(self.screen_width - 400) // 2}+{(self.screen_height - 400) // 2}")

        # 创建容器
        self.frame1 = tk.Frame(self.root, bd=2, relief=tk.GROOVE, padx=15, pady=15)
        self.frame1.pack(pady=20)

        # 容器1
        self.label_encrypt = tk.Label(self.frame1, text="加密", font=("Helvetica", 20, "bold"))
        self.label_encrypt.grid(row=0, column=0, padx=10)
        self.label_plaintext = tk.Label(self.frame1, text="Plaintext")
        self.label_plaintext.grid(row=1, column=0)
        self.text_plaintext = tk.Text(self.frame1, height=10, width=30)
        self.text_plaintext.grid(row=1, column=1)
        self.label_file = tk.Label(self.frame1, text="File")
        self.label_file.grid(row=2, column=0)
        self.button_file = tk.Button(self.frame1, text="Select File", command=self.open_file)
        self.button_file.grid(row=2, column=1, pady=10)
        self.label_key = tk.Label(self.frame1, text="KEY")
        self.label_key.grid(row=3, column=0)
        self.entry_key1 = tk.Entry(self.frame1)
        self.entry_key1.grid(row=3, column=1)
        self.label_encrypt_algorithm = tk.Label(self.frame1, text="Encrypt Algorithm")
        self.label_encrypt_algorithm.grid(row=4, column=0, pady=10)
        self.encrypt_options_algorithm = ["CaesarCipher", "KeywordCipher", "RSA"]
        self.encrypt_selected_algorithm = None
        self.combobox_algorithm = ttk.Combobox(self.frame1, values=self.encrypt_options_algorithm, state="readonly")
        self.combobox_algorithm.bind("<<ComboboxSelected>>", self.encrypt_algorithm_select)
        self.combobox_algorithm.set("Select an algorithm")
        self.combobox_algorithm.grid(row=4, column=1)
        self.button_algorithm = tk.Button(self.frame1, text="Encrypt", command=self.encrypt_on_button_algorithm_click)
        self.button_algorithm.grid(row=5, column=1)

    def pop_up_window(self, title='', label_text='', content='', button_text='') -> None:
        """弹窗"""
        # 弹窗主窗口
        toplevel = tk.Toplevel(self.root)
        toplevel.title(title)
        toplevel.geometry(f"400x250+{(self.screen_width - 400) // 2}+{(self.screen_height - 250) // 2}")

        # 组件
        label = tk.Label(toplevel, text=label_text)
        label.pack(pady='5')
        text = tk.Text(toplevel, height=10, width=30)
        text.delete(1.0, tk.END)
        text.insert(tk.END, content)
        text.pack()
        button = tk.Button(toplevel, text=button_text, command=toplevel.destroy)
        button.pack(pady='5')

    def encrypt_on_button_algorithm_click(self):
        """加密按钮"""
        key = self.entry_key1.get()
        try:
            self.encrypt_selected_algorithm(key)
        except TypeError as e:
            messagebox.showerror("错误", f"请选择具体算法后再点击\n\n{e}")

    def open_file(self):
        """打开文本文件"""
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r') as file:
                content = file.read()
                self.text_plaintext.delete(1.0, tk.END)
                self.text_plaintext.insert(tk.END, content)
        else:
            messagebox.showerror("打开文件错误", "文件类型需要为txt文件")

    def encrypt_algorithm_select(self, event):
        if event:
            selected_item = self.combobox_algorithm.get()
            if selected_item == "RSA":
                messagebox.showinfo("RSA提醒", "每个值需要以分号( ; )隔开\n如: 23;19;17")
            algorithm_options = {
                "CaesarCipher": self.caesar_cipher_encrypt,
                "KeywordCipher": self.keyword_cipher_encrypt,
                "RSA": self.rsa_encrypt
            }
            self.encrypt_selected_algorithm = algorithm_options.get(selected_item)

    def caesar_cipher_encrypt(self, key):
        """凯撒密码加密"""
        try:
            key = int(key)
            algorithm = CaesarCipher(key)
            algorithm.plain_text = self.text_plaintext.get("1.0", "end")
            algorithm.encrypt(algorithm.plain_text)
            self.pop_up_window("结果", "密文", algorithm.cipher_text, "关闭")
        except ValueError as e:
            messagebox.showerror("错误", f"CaesarCipher的key应为数字\n\n{e}")

    def keyword_cipher_encrypt(self, key: str):
        """关键词密码加密"""
        algorithm = KeywordCipher(key)
        cipher_text = algorithm.keyword_cipher_encrypt(self.text_plaintext.get("1.0", "end"))
        self.pop_up_window("结果", "密文", cipher_text, "关闭")

    def rsa_encrypt(self, key: str):
        """RSA加密"""
        key_list = key.split(";")
        try:
            prime_p = int(key_list[0])
            prime_q = int(key_list[1])
            key_e = int(key_list[2])
        except ValueError as e:
            messagebox.showerror("错误", f"key应该为数字\n\n{e}")
            return None
        except IndexError as e:
            messagebox.showerror("错误", f"Key应该传入三个值\n{e}")
            return None

        rsa = RSA()

        rsa.plaintext = self.text_plaintext.get("1.0", "end")
        # 以下为加密过程需要输入的数字，prime_p,prime_q为质数，prime_p与prime_q相乘得到n，e与n互质。
        rsa.prime_p = prime_p
        rsa.prime_q = prime_q
        rsa.key_e = key_e
        try:
            rsa.ciphertext = rsa.encrypt()
        except ValueError as e:
            messagebox.showerror("错误", f"{e}")
            return None
        base64_encoded = base64.b64encode(rsa.ciphertext.encode("utf-8")).decode('utf-8')
        key_n = rsa.prime_p * rsa.prime_q
        self.pop_up_window("结果", "密文", f"密钥d:{rsa.key_d}\n密钥n:{key_n}\n密文:{base64_encoded}", "关闭")
