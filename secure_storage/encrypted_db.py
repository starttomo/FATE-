import os
from Crypto.Cipher import AES
from utils.crypto import generate_paillier_keypair
from utils.serialization import serialize, deserialize

class EncryptedDB:
    def __init__(self):
        self.public_key, self.private_key = generate_paillier_keypair()
        self.storage = {}
        self.aes_key = os.urandom(16)

    def encrypt_and_store(self, key, value):
        encrypted_value = encrypt_value(self.public_key, value)
        serialized_value = serialize(encrypted_value)
        cipher = AES.new(self.aes_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(serialized_value)
        encrypted_data = cipher.nonce + tag + ciphertext
        self.storage[key] = encrypted_data

    def retrieve_and_decrypt(self, key):
        if key in self.storage:
            encrypted_data = self.storage[key]
            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
            cipher = AES.new(self.aes_key, AES.MODE_GCM, nonce=nonce)
            serialized_value = cipher.decrypt_and_verify(ciphertext, tag)
            encrypted_value = deserialize(serialized_value)
            return decrypt_value(self.private_key, encrypted_value)
        return None