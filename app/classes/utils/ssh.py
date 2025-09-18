from paramiko import AutoAddPolicy
from paramiko import SSHClient
import time


class ShellSSh:
    RECEIVE_SIZE = 64

    def __init__(self, host: str, username: str, password: str, port: int = 22) -> None:
        self.ssh: SSHClient = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(
            hostname=host,
            username=username,
            password=password,
            port=port,
            allow_agent=False,
            look_for_keys=False
        )

        self.bash = self.ssh.invoke_shell()

    def __enter__(self):
        # Return the object itself when entering context
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always close connection when leaving context
        self.close()

    def send(self, buffer: str):
        self.bash.send((buffer + '\n').encode('ascii'))
        time.sleep(0.1)

        while not self.bash.recv_ready():
            time.sleep(0.05)

        result: bytes = b''
        recvd: bytes = self.bash.recv(ShellSSh.RECEIVE_SIZE)
        while len(recvd) > 0 and self.bash.recv_ready():
            result += recvd
            recvd = self.bash.recv(ShellSSh.RECEIVE_SIZE)

        return result.decode('ascii')

    def close(self):
        self.ssh.close()
