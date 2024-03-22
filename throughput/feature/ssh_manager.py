import paramiko
import socket
import os
import sys


module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ssh_manager'))
sys.path.append(module_path)

class SSHManager:
    def __init__(self, host_device1, host_device2, username='root', password='lancs', port=22):
        self.host_device1 = host_device1
        self.host_device2 = host_device2
        self.port = port
        self.username = username
        self.password = password
        self.ssh_device1 = None
        self.ssh_device2 = None

    def connect_device(self):
        try:
            self.ssh_device1 = self._connect(self.host_device1)
            self.ssh_device2 = self._connect(self.host_device2)
            return True
        except paramiko.AuthenticationException:
            print("Xác thực thất bại. Vui lòng kiểm tra thông tin đăng nhập.")
        except paramiko.SSHException as e:
            print(f"Không thể thiết lập kết nối SSH: {str(e)}")
        except socket.error as e:
            print(f"Lỗi kết nối socket: {str(e)}")
        except Exception as e:
            print(f"Lỗi không mong muốn: {str(e)}")
        return False

    def _connect(self, host):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port=self.port, username=self.username, password=self.password)
        return ssh_client
    def execute_command1(self, command):
        stdin, stdout, stderr = self.ssh_device1.exec_command(command)
        return stdout.read().decode()
    def execute_command2(self, command):
        stdin, stdout, stderr = self.ssh_device2.exec_command(command)
        return stdout.read().decode()