import time
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from feature.ssh_manager import SSHManager
from feature.iperf import TestIperf

class RoutingStatic:  
    def __init__(self):
        self.ssh_manager = SSHManager()
        self.test_iperf = TestIperf()

    def config_dv1(self, dst2, host_device2):
        with self.ssh_manager.ssh_device1.invoke_shell() as channel:
            try:
                channel.send("enable network\n")
                channel.send("config terminal\n")
                channel.send(f"ip route {dst2}/24 gateway {host_device2} interface wan\n")
                print("config1 done!!!")
            except Exception as e:
                print(f"Lỗi config on device1: {str(e)}")

    def config_dv2(self, dst1, host_device1):
        with self.ssh_manager.ssh_device2.invoke_shell() as channel:
            try:
                channel.send("enable network\n")
                channel.send("config terminal\n")
                channel.send(f"ip route {dst1}/24 gateway {host_device1} interface wan\n")
                print("config2 done!!!")
            except Exception as e:
                print(f"Lỗi config on device2: {str(e)}")

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

    def load_config_from_json(json_file_path):
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

    def run_static(self):
        config_data = self.load_config_from_json('data.json')  

        dst1 = config_data.get('dst1', '')
        dst2 = config_data.get('dst2', '')
        host_device1 = config_data.get('host_device1', '')
        host_device2 = config_data.get('host_device2', '')

        self.config_dv1(dst2, host_device2)
        self.config_dv2(dst1, host_device1)

        if self.check_routing():
            self.test_iperf.lan_to_wan(host_device1, host_device2)
            self.test_iperf.lan_to_lan(host_device1, host_device2)
        self.del_rule(dst1, dst2, host_device1, host_device2)