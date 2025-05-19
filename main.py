# main.py
from utils.crypto import generate_paillier_keypair
from federated.participant import Participant
from federated.coordinator import Coordinator
import matplotlib.pyplot as plt

# 确保中文显示正常
plt.rcParams["font.family"] = ["SimHei"]


def main():
    # 生成密钥对
    public_key, private_key = generate_paillier_keypair()

    # 创建参与方
    participant1 = Participant(public_key)
    participant2 = Participant(public_key)

    # 设置参与方值
    x=float(input("请输入第一个数: "))
    y=float(input("请输入第二个数: "))
    participant1.set_value(x)
    participant2.set_value(y)

    # 创建协调者
    coordinator = Coordinator(public_key, private_key)
    coordinator.add_participant(participant1)
    coordinator.add_participant(participant2)

    # 执行安全计算
    try:
        # 执行安全乘法
        mul_result = coordinator.perform_secure_multiplication()
        print(f"最终安全乘法结果: {mul_result}")

        # 执行安全比较
        cmp_result = coordinator.perform_secure_comparison()
        print(f"最终安全比较结果: {cmp_result}")

        # 可视化监控
        coordinator.visualize_training()

    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("[系统] 联邦学习会话结束")


if __name__ == "__main__":
    main()