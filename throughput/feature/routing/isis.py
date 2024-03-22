import time
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from feature.ssh_manager import SSHManager
from feature.iperf import test_iperf

class routing_static:  
    def __init__(self, ssh_manager):
        self.ssh_manager = ssh_manager

    def config_dv1(self, dst2, host_device2):
        with self.ssh_manager.ssh_device1.invoke_shell() as channel:
            try:
                channel.send("enable network\n")
                channel.send("config terminal\n")
                channel.send(f"ip route {dst2}/24 gateway {host_device2} interface wan\n")
                print("config1 done!!!")
            except Exception as e:
                print(f"Lỗi trong bài kiểm thử 1: {str(e)}")

    def config_dv2(self, dst1, host_device1):
        with self.ssh_manager.ssh_device2.invoke_shell() as channel:
            try:
                channel.send("enable network\n")
                channel.send("config terminal\n")
                channel.send(f"ip route {dst1}/24 gateway {host_device1} interface wan\n")
                print("config2 done!!!")
            except Exception as e:
                print(f"Lỗi : {str(e)}")

    def check_routing(self):
        time_limit = 30
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            with self.ssh_manager.ssh_device1.invoke_shell() as channel:
                channel.send("enable network\n")
                channel.send("show ip route statistics\n")
                time.sleep(5)
                check1 = channel.recv(10000).decode("utf-8")

                if "K>* " in check1:
                    print("config static done!!!")
                    return True
                else:
                    print("config device fail")

            if elapsed_time >= time_limit:
                print("Đã hết thời gian. Config STATICS fail.")
                return False
            
    def del_rule(self, dst1, dst2, host_device1, host_device2):
        try:
            confirm_delete = input("Bạn muốn xóa rule không? (yes/no): ").lower()
            if confirm_delete == 'yes':
                with self.ssh_manager.ssh_device1.invoke_shell() as channel:
                    channel.send("enable network\n")
                    channel.send("config terminal\n")
                    channel.send(f"no ip route {dst2}/24 gateway {host_device2} interface wan\n")
                    print("del config1 done!!!")
                time.sleep(2)
                with self.ssh_manager.ssh_device2.invoke_shell() as channel:
                    channel.send("enable network\n")
                    channel.send("config terminal\n")
                    channel.send(f"no ip route {dst1}/24 gateway {host_device1} interface wan\n")
                    print("del config2 done!!!")
            else:
                print(" Kết thúc chương trình.")
        except Exception as e:
            print(f"Lỗi trong hàm del_rule: {str(e)}")

def read_config_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            config_data = json.load(json_file)
        return config_data
    except FileNotFoundError:
        print(f'File {json_file_path} not found. Using default values.')
        return {}
    except json.JSONDecodeError:
        print(f'Error decoding JSON in {json_file_path}. Using default values.')
        return {}

def main():
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'data.json')
    config_data = read_config_from_json(json_file_path)

    ssh_manager = SSHManager(config_data.get('host_device1', ''),
                             config_data.get('host_device2', ''),
                             config_data.get('username', ''),
                             config_data.get('password', ''))

    dst1 = config_data.get('dst1', '')
    dst2 = config_data.get('dst2', '')
    host_device1 = config_data.get('host_device1', '')
    host_device2 = config_data.get('host_device2', '')
    
    static_router = routing_static(ssh_manager)

    static_router.config_dv1(dst2, host_device2)
    static_router.config_dv2(dst1, host_device1)
    
    if static_router.check_routing():
        test_iperf_instance = test_iperf(ssh_manager)
        test_iperf_instance.run_iperf('ssh_host_device1', 'ssh_host_device2')
    static_router.del_rule(dst1, dst2, host_device1, host_device2)

if __name__ == "__main__":
    main()
