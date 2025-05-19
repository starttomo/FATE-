# federated/coordinator.py
import matplotlib.pyplot as plt
import numpy as np
from utils.crypto import decrypt_value
from protocols.secure_mul import secure_multiplication
from protocols.secure_cmp import secure_comparison


class Coordinator:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)
        print(f"[Coordinator] 添加参与方: {len(self.participants)}")

    def perform_secure_multiplication(self):
        values = [p.get_encrypted_value() for p in self.participants]
        if len(values) < 2:
            raise ValueError("至少需要两个参与方才能执行安全乘法")

        print(f"[Coordinator] 执行安全乘法: 参与方数量={len(self.participants)}")
        encrypted_result = secure_multiplication(
            self.public_key,
            self.private_key,
            values[0],
            values[1]
        )
        result = decrypt_value(self.private_key, encrypted_result)
        print(f"[Coordinator] 安全乘法结果: {result}")
        return result

    def perform_secure_comparison(self):
        values = [p.get_encrypted_value() for p in self.participants]
        if len(values) < 2:
            raise ValueError("至少需要两个参与方才能执行安全比较")

        print(f"[Coordinator] 执行安全比较: 参与方数量={len(self.participants)}")
        result = secure_comparison(self.private_key, values[0], values[1])

        comparison_text = {
            1: "大于",
            -1: "小于",
            0: "等于"
        }

        print(f"[Coordinator] 安全比较结果: 参与方1 {comparison_text[result]} 参与方2")
        return result

    def visualize_training(self):
        """显示参与方的输入值"""
        plt.figure(figsize=(10, 6))

        # 获取参与方的值
        values = [p.value for p in self.participants]
        labels = [f'参与方{i + 1}' for i in range(len(self.participants))]

        # 创建柱状图
        bars = plt.bar(labels, values, color='skyblue')
        plt.ylabel('数值')
        plt.title('参与方输入值')

        # 在柱子上显示具体数值
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}',
                     ha='center', va='bottom')

        # 显示图表
        plt.show()
        plt.close()  # 确保图表被关闭