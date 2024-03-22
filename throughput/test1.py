import sys
import os

# Thêm đường dẫn đến thư mục chứa module 'ssh_manager'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from feature.ssh_manager import SSHManager

def main():
    if len(sys.argv) != 3:
        print("Sử dụng: python test.py <IP_device1> <IP_device2> ")
        return

    # Nhận địa chỉ IP của thiết bị 1 và thiết bị 2 từ đối số dòng lệnh
    ip_device1 = sys.argv[1]
    ip_device2 = sys.argv[2]

    # Tạo một đối tượng SSHManager
    ssh_manager = SSHManager(host_device1=ip_device1, host_device2=ip_device2, password="lancs")

    # Kết nối đến thiết bị
    if ssh_manager.connect_device():
        print("connected")
        ifconfig_output = ssh_manager.execute_command1('ifconfig')
        print("Output của lệnh ifconfig:")
        print(ifconfig_output)
    else:
        print("Không thể kết nối đến thiết bị.")

if __name__ == "__main__":
    main()
