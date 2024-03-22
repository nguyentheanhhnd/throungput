import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from feature.ssh_manager import SSHManager
from feature.routing.static import RoutingStatic


class RunTest():  
    def __init__(self):
        self.ssh_manager = SSHManager()

    def main(self, option, device1_ip, device2_ip):
        if option == "routing":
            self.routing_static(device1_ip, device2_ip)

    def routing_static(self, device1_ip, device2_ip):
        ssh_manager = SSHManager(host_device1=device1_ip, host_device2=device2_ip)
        static = RoutingStatic(ssh_manager)
        static.run_static()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 run_test.py <option> <device1_IP> <device2_IP>")
        sys.exit(1)
    
    option = sys.argv[1]
    device1_ip = sys.argv[2]
    device2_ip = sys.argv[3]

    tester = RunTest()
    tester.main(option, device1_ip, device2_ip)
