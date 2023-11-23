import string


class KeywordCipher:
    def __init__(self, key: str):
        self.keyword = key

    def generate_alphabet(self):
        # 生成关键字字母表
        keyword = self.keyword.upper()
        alphabet = list(string.ascii_uppercase)
        keyword_set = set(keyword)
        keyword_alphabet = [char for char in keyword + ''.join(alphabet) if char not in keyword_set]
        return keyword_alphabet

    def keyword_cipher_encrypt(self, plaintext):
        # 生成关键字字母表
        keyword_alphabet = self.generate_alphabet()

        # 加密
        ciphertext = ''
        for char in plaintext.upper():
            if char in string.ascii_uppercase:
                index = string.ascii_uppercase.index(char)
                ciphertext += keyword_alphabet[index]
            else:
                ciphertext += char

        return ciphertext

    def keyword_cipher_decrypt(self, ciphertext):
        # 生成关键字字母表
        keyword_alphabet = self.generate_alphabet()

        # 解密
        plaintext = ''
        for char in ciphertext.upper():
            if char in string.ascii_uppercase:
                try:
                    index = keyword_alphabet.index(char)
                    plaintext += string.ascii_uppercase[index]
                except ValueError:
                    # 如果 char 不在关键字字母表中，直接添加到明文中
                    plaintext += char
            else:
                plaintext += char

        return plaintext
