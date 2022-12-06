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
        # Starting handle thread for incoming messages
        client_handler = threading.Thread(target=self.__handle, args=[self.client])
        client_handler.start()

    """
    TODO: Le thread se ferme tout seul quand le serveur est fermé??? Essayer de
    comprendre pourquoi... Arpès ça m'arrange mais bon
    """

    def __handle(self, conn) -> None:
        while self.msgsrv != "kill" and self.msgsrv != "reset" and not self.__killed:
            self.msgsrv = conn.recv(2048)
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
        """

    def send(self, message: str) -> None:
        if not self.__killed:
            logging.debug(f"Sending message to {self.addr}: {message}")
            self.client.send(message.encode())
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
