import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class EncryptionHandler(object):
    initialized = False

    KEY = ""
    BS = 0

    def __init__(self, key: str): 
        EncryptionHandler.BS = AES.block_size
        EncryptionHandler.KEY = hashlib.sha256(key.encode()).digest()

        EncryptionHandler.initialized = True

    @staticmethod
    def encrypt(message_raw):
        message_raw = EncryptionHandler._pad(message_raw)

        iv = Random.new().read(AES.block_size)

        cipher = AES.new(EncryptionHandler.KEY, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(message_raw.encode()))

    @staticmethod
    def decrypt(message_enc):
        message_enc = base64.b64decode(message_enc)

        iv = message_enc[:AES.block_size]
        cipher = AES.new(EncryptionHandler.KEY, AES.MODE_CBC, iv)

        return EncryptionHandler._unpad(cipher.decrypt(message_enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def _pad(text):
        _margin = EncryptionHandler.BS - len(text) % EncryptionHandler.BS
        return text + (_margin) * chr(_margin)

    @staticmethod
    def _unpad(text):
        return text[:-ord(text[len(text)-1:])]
