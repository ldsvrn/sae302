#!/usr/bin/env python3
import threading
import socket
import logging
import time
import json
from PyQt5.QtWidgets import QLabel, QTextBrowser


class Connection:
    def __init__(
        self, host: str, port: int, label_info: QLabel, label_command: QTextBrowser
    ) -> None:
        self.client = socket.socket()
        self.msgsrv = ""
        self.addr = (host, port)
        self.info = {}

        self.label_info = label_info
        self.label_command = label_command

        self.__connect()
        self.send("info")

    def __connect(self) -> None:
        # Handle errors in the GUI
        self.client.connect(self.addr)

        # Flag to kill the handle thread
        self.__killed = False
        self.msgsrv = ""
        # Starting handle thread for incoming messages
        print(self.__killed)
        client_handler = threading.Thread(target=self.__handle, args=[self.client])
        client_handler.start()


    def __handle(self, conn) -> None:
        while self.msgsrv != "kill" and self.msgsrv != "reset" and not self.__killed:
            self.msgsrv = conn.recv(4096)
            logging.debug(f"Size of the recieved message is {len(self.msgsrv)}")
            if not self.msgsrv:
                break  # prevents infinite loop on disconnect, auto disconnect clients
            self.msgsrv = self.msgsrv.decode()
            logging.debug(f"Message from {self.addr}: {self.msgsrv}")

            if self.msgsrv[:4] == "info":
                self.info = json.loads(self.msgsrv[4:])
                logging.debug("Got the server information.")
                self.label_info.setText(self._info_string())
            elif self.msgsrv[:4] == "cmmd":
                logging.debug("Got a command output from the server.")
                self.label_command.append(self.msgsrv[4:])

        logging.debug(f"Closing handle thread for {self.addr}")
        self.__killed = True
    
    def _info_string(self) -> str:
        ip = '\n'.join([str(x) for x in self.info["ip"]])
        return f"""
- Nom: {self.info['os']['node']}
- OS: {self.info['os']['system']}
- Version: {self.info['os']['release']}
- IPs:
{ip}
- CPU: {self.info['cpu']}%
- RAM: {self.info["mem"]["used"]}GB/{self.info["mem"]["total"]}GB ({self.info["mem"]["percent"]}%) 
- Disk: {self.info["disk"]["used"]}GB/{self.info["disk"]["total"]}GB ({round(100 - self.info["mem"]["percent"], 2)}%) 
        """

    def send(self, message: str) -> None:
        if not self.__killed:
            try:
                logging.debug(f"Sending message to {self.addr}: {message}")
                self.client.send(message.encode())
            except Exception as e:
                logging.error(f"Sending failed! ({e})")
                self.__killed = True
        else:
            logging.error(
                f"Tried to send '{message}' to {self.addr} while the connection is killed."
            )

    def reset(self) -> None:
        logging.debug(f"Resetting {self.addr}")
        self.client.send("reset".encode())
        self.__killed = True

    def disconnect(self) -> None:
        logging.debug(f"Disconnecting from {self.addr}")
        self.client.send("disconnect".encode())
        self.__killed = True

    def kill(self) -> None:
        logging.debug(f"Killing {self.addr}")
        self.client.send("kill".encode())
        self.__killed = True
        self.client.close()

    def isKilled(self) -> bool:
        return self.__killed

    def execute_command(self, command: str, shell: str = "osef"):
        com = {"com": command, "shell": shell}
        self.send("command" + json.dumps(com))

    def reconnect(self):
        if self.__killed:
            self.client = socket.socket()
            self.__connect()

    # maybe i'll find another way but this is the easiest method i could think of 
    @classmethod
    def is_server_up(cls, ip: str, port: int) -> str:
        sock = socket.socket()
        try:
            sock.connect((ip, port))
        except Exception as e:
            ret = str(e)
        else:
            ret = "ok"
        sock.close()
        del sock
        return ret

if __name__ == "__main__":
    import sys
    HOST = "127.0.0.1"

    conn = Connection(HOST, int(sys.argv[1]), "pass", "pass")
    # conn2 = Connection(HOST, int(sys.argv[2]))
    for i in sys.argv[2:]:
        # Let the server answer
        time.sleep(1)
        conn.send(i)
    conn.execute_command("ls -lah", "linux")
    time.sleep(1)
    conn.execute_command("ls", "test")
    # conn.disconnect()
    # conn2.send("test2")

    # time.sleep(5)
    # conn2.send("test3")
