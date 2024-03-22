import subprocess
import time
import os 
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from feature.ssh_manager import SSHManager

class TestIperf:  
    def __init__(self, ssh_manager):
        self.ssh_manager = ssh_manager

    def lan_to_wan(self, ssh_device1, ssh_host_device1):
        print("Running IPERF3.........")
        try:
            stdin, stdout, stderr = ssh_device1.exec_command('iperf3 -s')
            output1 = stdout.read().decode('utf-8')
            print(output1)
            time.sleep(2)
            with open('output.txt', 'w') as f:
                sys.stdout = f
                for i in range(3):
                    stdin, stdout, stderr = self.ssh_manager.ssh_device2.exec_command(f"iperf3 -c {ssh_device1} -t 30")
                    output2 = stdout.read().decode('utf-8')
                    print(output2)
                sys.stdout = sys.__stdout__
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def lan_to_lan(self, ssh_device1, ssh_host_device1):
        print("Running IPERF3.........")
        try:
            stdin, stdout, stderr = ssh_device1.exec_command('iperf3 -s')
            output1 = stdout.read().decode('utf-8')
            print(output1)
            time.sleep(2)
            with open('output.txt', 'w') as f:
                sys.stdout = f
                for i in range(3):
                    command = f"iperf3 -c {ssh_device1} -t 30"
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result.stdout if result.returncode == 0 else result.stderr)
                sys.stdout = sys.__stdout__
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    ssh_manager = SSHManager('host_device1', 'host_device2', 'username', 'password')
    if ssh_manager.connect_device():
        test_iperf = TestIperf(ssh_manager)
        test_iperf.lan_to_wan('ssh_device1', 'ssh_host_device1')
        test_iperf.lan_to_lan('ssh_device1', 'ssh_host_device1')
    else:
        print("Không thể kết nối đến thiết bị.")
