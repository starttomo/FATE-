# protocols/secure_cmp.py
from utils.crypto import PRECISION


def secure_comparison(private_key, encrypted_value1, encrypted_value2):
    """
    安全比较协议（支持浮点数）
    """
    diff = encrypted_value1 - encrypted_value2
    decrypted_diff = private_key.decrypt(diff) / PRECISION

    if decrypted_diff > 0:
        return 1
    elif decrypted_diff < 0:
        return -1
    else:
        return 0