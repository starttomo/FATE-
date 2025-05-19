# federated/participant.py
from utils.crypto import encrypt_value

class Participant:
    def __init__(self, public_key):
        self.public_key = public_key
        self.value = None

    def set_value(self, value):
        self.value = value

    def get_encrypted_value(self):
        return encrypt_value(self.public_key, self.value)