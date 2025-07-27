import os
from cryptography.fernet import Fernet

class StageManager:
    def __init__(self, data_path='data/stage.txt', key_path='data/key.key'):
        self.data_path = data_path
        self.key_path = key_path
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)

        if not os.path.exists(self.key_path):
            self.generate_key()
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_path, 'wb') as f:
            f.write(key)

    def load_key(self):
        with open(self.key_path, 'rb') as f:
            return f.read()

    def save_stage(self, stage: int):
        encrypted = self.cipher.encrypt(str(stage).encode())
        with open(self.data_path, 'wb') as f:
            f.write(encrypted)

    def load_stage(self) -> int:
        if not os.path.exists(self.data_path):
            return 1  # default stage

        with open(self.data_path, 'rb') as f:
            encrypted_data = f.read()

        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            return int(decrypted.decode())
        except Exception:
            return 1  # fallback if decryption fails (prob will)
