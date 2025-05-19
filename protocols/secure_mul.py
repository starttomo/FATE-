# protocols/secure_mul.py
import numpy as np
from phe import paillier
from utils.crypto import PRECISION


def secure_multiplication(public_key, private_key, encrypted_a, encrypted_b):
    """
    使用同态加密实现安全乘法，支持浮点数
    使用公式: (a + r) * (b + s) - a*s - b*r - r*s
    其中 r 和 s 是随机数
    """
    # 解密输入值以检查范围
    a = private_key.decrypt(encrypted_a) / PRECISION
    b = private_key.decrypt(encrypted_b) / PRECISION

    # 检查数值范围，确保不会溢出
    if abs(a) > 1e6 or abs(b) > 1e6:
        raise ValueError("输入值过大，可能导致计算溢出")

    # 生成随机数，使用浮点数
    r = np.random.uniform(0.1, 1.0)
    s = np.random.uniform(0.1, 1.0)

    # 加密随机数
    encrypted_r = public_key.encrypt(int(r * PRECISION))
    encrypted_s = public_key.encrypt(int(s * PRECISION))

    # 计算 (a + r) 和 (b + s)
    encrypted_a_plus_r = encrypted_a + encrypted_r
    encrypted_b_plus_s = encrypted_b + encrypted_s

    # 解密 (a + r) 和 (b + s)
    a_plus_r = private_key.decrypt(encrypted_a_plus_r) / PRECISION
    b_plus_s = private_key.decrypt(encrypted_b_plus_s) / PRECISION

    # 计算 (a + r) * (b + s)
    product = a_plus_r * b_plus_s

    # 计算 a*s, b*r, r*s
    as_term = a * s
    br_term = b * r
    rs_term = r * s

    # 计算最终结果
    result = product - as_term - br_term - rs_term

    # 处理浮点数精度问题
    result = round(result, 10)  # 保留10位小数

    # 加密结果
    return public_key.encrypt(int(result * PRECISION))