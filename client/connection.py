#!/usr/bin/env python3
import threading
import socket
import sys
import logging
import time
import json

logging.basicConfig(level=logging.DEBUG)

HOST = "127.0.0.1"


class Connection:
    def __init__(self, host: str, port: int) -> None:
        self.client = socket.socket()
        self.msgsrv = ""
        self.addr = (host, port)

        self.__connect()

    def __connect(self) -> None:
        # Handle errors in the GUI
        self.client.connect(self.addr)

        # Flag to kill the handle thread
        self.__killed = False
        # Starting handle thread for incoming messages
        client_handler = threading.Thread(
            target=self.__handle, args=[self.client])
        client_handler.start()

    """
    TODO: Le thread se ferme tout seul quand le serveur est fermé??? Essayer de
    comprendre pourquoi... Arpès ça m'arrange mais bon
    """

    def __handle(self, conn) -> None:
        while self.msgsrv != "kill" and self.msgsrv != "reset" and not self.__killed:
            self.msgsrv = conn.recv(1024)
            if not self.msgsrv:
                break  # prevents infinite loop on disconnect
            self.msgsrv = self.msgsrv.decode()
            logging.debug(f"Message from {self.addr}: {self.msgsrv}")
        logging.debug(f"Closing handle thread for {self.addr}")
        self.__killed = True

    def send(self, message: str) -> None:
        if not self.__killed:
            logging.debug(f"Sending message to {self.addr}: {message}")
            self.client.send(message.encode())

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


if __name__ == "__main__":
    conn = Connection(HOST, int(sys.argv[1]))
    conn2 = Connection(HOST, int(sys.argv[2]))
    conn.send("test")
    conn2.send("test2")

    time.sleep(5)
    conn2.send("test3")