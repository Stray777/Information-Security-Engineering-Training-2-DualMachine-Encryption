from sympy import totient
import math


class RSA:
    # 明文,写入即固定，其后加解密的结果都写入ciphertext
    plaintext = "plaintext"
    # 密文
    ciphertext = "ciphertext"
    # 以下为加密过程需要输入的数字，prime_p,prime_q为偶数，prime_p与prime_q相乘得到n，e与n互质。
    prime_p = 0
    prime_q = 0
    key_e = 0
    # 以下为解密过程需要输入的数字
    decrypt_key_n = 0
    decrypt_key_d = 0
    # 以下为加密完成后得到的两个密钥
    key_n = 0
    key_d = 0

    @staticmethod
    def _mod_inverse_(public_key_e, euler_n):  # 计算最小模反函数
        private_key_d = 1
        while 1:
            if (private_key_d * public_key_e - 1) % euler_n == 0:
                return private_key_d
            else:
                private_key_d += 1

    @staticmethod
    def _if_prime_(number):  # 判断数字是否为质数
        if number < 0:
            return 0
        counter = 0
        for i in range(1, number + 1):
            if number % i == 0:
                counter += 1
        if counter == 2:
            return 1
        else:
            return 0

    @staticmethod
    def _are_coprime_(euler_n, public_key_e):  # 判断两数是否互质
        return math.gcd(euler_n, public_key_e) == 1

    def _get_public_key_n_(self):  # 获取p，q，判断其是否为质数，获取其乘积，即公钥n
        if self._if_prime_(self.prime_p) == 1 & self._if_prime_(self.prime_q) == 1:  # 分别判断两数是否为质数
            public_key_n = self.prime_p * self.prime_q
            return public_key_n
        else:  # 如果存在非质数则抛出异常
            raise ValueError("One of these numbers is not a prime number")

    def _get_public_key_e_(self, public_key_n):  # 获取公钥e，并判断其是否与n的欧拉函数互质，参数为公钥n
        euler_n = totient(public_key_n)
        if self._are_coprime_(euler_n, self.key_e) and 1 < self.key_e < euler_n:  # 判断是否互质
            return self.key_e
        else:
            raise ValueError("ERROR:This number is not available")

    def _get_private_key_(self, euler_n):  # 获取私钥d，其为e关于n的欧拉函数的模反函数
        return self._mod_inverse_(self.key_e, euler_n)

    def _encrypt_char_(self, plain_char):  # 加密单个字符
        plain_char_num = ord(plain_char)
        self.key_n = self._get_public_key_n_()
        self.key_e = self._get_public_key_e_(self.key_n)
        self.key_d = self._get_private_key_(totient(self.key_n))
        cipher_char_num = (plain_char_num ** self.key_e) % self.key_n
        return chr(cipher_char_num)

    def _decrypt_char_(self, cipher_char):  # 解密单个字符
        cipher_char_num = ord(cipher_char)
        plain_char_num = (cipher_char_num ** self.decrypt_key_d) % self.decrypt_key_n
        return chr(plain_char_num)

    def encrypt(self):  # 加密字符串
        char = ''
        ciphertext = ""
        for char in self.plaintext:
            ciphertext += self._encrypt_char_(char)
        return ciphertext

    def decrypt(self):  # 解密字符串
        char = ''
        plaintext = ""
        for char in self.ciphertext:
            plaintext += self._decrypt_char_(char)
        return plaintext


def main():  # 测试
    rsa = RSA()
    # 密文
    rsa.plaintext = "plaintext"
    # 以下为加密过程需要输入的数字，prime_p,prime_q为偶数，prime_p与prime_q相乘得到n，e与n互质。
    rsa.prime_p = int(input("输入第一个质数\n"))
    rsa.prime_q = int(input("输入第二个质数\n"))
    rsa.key_e = int(input("输入与" + str(totient(rsa.prime_p * rsa.prime_q)) + "且大于1小于" + str(
        totient(rsa.prime_p * rsa.prime_q)) + "互质的数\n"))
    rsa.ciphertext = rsa.encrypt()
    print("密钥d是" + str(rsa.key_d) + "\n")
    print("密钥n是" + str(rsa.prime_p * rsa.prime_q) + "\n")
    print("密文是" + str(rsa.ciphertext) + "\n")
    # 以下为解密过程需要输入的数字
    rsa.decrypt_key_n = 6
    rsa.decrypt_key_d = int(input("输入密钥d\n"))
    rsa.decrypt_key_n = int(input("输入密钥n\n"))
    rsa.ciphertext = rsa.decrypt()
    print("明文是" + str(rsa.ciphertext) + "\n")
