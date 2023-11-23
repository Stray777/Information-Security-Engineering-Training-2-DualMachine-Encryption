class CaesarCipher:
    def __init__(self, shift: int):
        self.shift = shift
        self.plain_text = ""
        self.cipher_text = ""

    def encrypt(self, text: str) -> str:
        """加密"""
        result = ""
        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                if is_upper:
                    encrypted_char = chr((ord(char) + self.shift - ord('A')) % 26 + ord('A'))
                else:
                    encrypted_char = chr((ord(char) + self.shift - ord('a')) % 26 + ord('a'))
                result += encrypted_char
            else:
                result += char
        self.cipher_text = result
        return result

    def decrypt(self, text: str):
        """解密"""
        self.shift = -self.shift
        self.plain_text = self.encrypt(text)
        self.shift = -self.shift

    def get_cipher_text(self):
        """获取秘文"""
        return self.cipher_text

    def get_plain_text(self):
        """获取明文"""
        return self.plain_text
