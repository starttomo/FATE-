# utils/crypto.py
from phe import paillier

# 定义精度因子
PRECISION = 1e6

def generate_paillier_keypair():
    return paillier.generate_paillier_keypair()

def encrypt_value(public_key, value):
    # 将浮点数转换为整数（乘以精度因子）
    scaled_value = int(value * PRECISION)
    return public_key.encrypt(scaled_value)

def decrypt_value(private_key, encrypted_value):
    # 解密后除以精度因子得到原始浮点数
    decrypted_value = private_key.decrypt(encrypted_value)
    return decrypted_value / PRECISION