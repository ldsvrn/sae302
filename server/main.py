#!/usr/bin/env python3

import socket
import logging
import sys
import time
import actions
import json

logging.basicConfig(level=logging.DEBUG)

HOST = ("127.0.0.1", int(sys.argv[1]))


class Server:
    def __init__(self, host: tuple):
        self.host = host

    def start(self):
        # self.killed to allow killing the server outside the class
        self.killed = False

        while not self.killed:
            self.server = socket.socket()
            logging.debug("Created socket")

            # While True loop
            self.__bind(self.host)

            self.server.listen()

            message = ""
            while not self.killed and message != "reset":
                logging.debug("Waiting for a client")
                self.client, addr = self.server.accept()
                logging.info(f"Connected to {addr}")

                message = ""  # reset so we can reconnect
                while (
                    not self.killed and message != "reset" and message != "disconnect"
                ):
                    msgcl = self.client.recv(1024)
                    if not msgcl:
                        break  # prevents infinite loop on disconnect

                    message = msgcl.decode()
                    logging.info(f"Message from {addr}: {message}")

                    self.__handle(message, addr)

                logging.info(f"Client at {addr} disconnected.")
                self.client.close()

            logging.debug("Closing server.")
            self.server.close()

    """
    Handle function for readability
    """

    def __handle(self, message: str, addr: tuple):
        if message == "dostuff":
            print("didstuff")
            self.client.send("didstuff".encode())
        elif message == "kill":
            logging.info(f"Kill requested by {addr}...")
            self.killed = True  # avoid adding a condition to while loops
        elif message == "reset":
            logging.info(f"Client at {addr} requested a reset.")
        elif message == "info":
            logging.info(f"Client at {addr} system info.")
            self.client.send(json.dumps(actions.get_all()).encode())

    """
    Retries to bind the socked every 10 seconds.
    Allows the server to be reset.
    """

    def __bind(self, host: tuple):
        while True:
            try:
                self.server.bind(host)
                logging.debug(f"Socket bound to {host}")
            except OSError:
                logging.info(f"Port {host[1]} not available. Retrying...")
                time.sleep(10)
                continue
            else:
                break

    def kill(self):
        try:
            self.client.send("kill".encode())
            self.client.close()
            self.server.close()
            self.killed = True
        except Exception:
            # Do not care about errors here, we're making sure the server is killed
            pass


if __name__ == "__main__":
    server = Server(HOST)
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: killing server...")
        server.kill()
