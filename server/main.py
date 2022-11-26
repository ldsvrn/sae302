#!/usr/bin/env python3

import socket
import logging
import sys
import time

logging.basicConfig(level=logging.DEBUG)

HOST = ("127.0.0.1", int(sys.argv[1]))


class Server():
    def __init__(self, host: tuple):
        self.host = host

    def start(self):
        # self.killed to allow killing the server outside the class
        self.killed = False

        while not self.killed:
            self.server = socket.socket()
            logging.debug("Created socket")
            while True:
                try:
                    self.server.bind(self.host)
                    logging.debug(f"Socket bound to {self.host}")
                except OSError:
                    logging.info(
                        f"Port {self.host[1]} not available. Retrying...")
                    time.sleep(1)
                    continue
                else:
                    break

            self.server.listen()

            message = ""
            while not self.killed or message != "reset":
                logging.debug("Waiting for a client")
                self.client, addr = self.server.accept()
                logging.info(f"Connected to {addr}")

                while message != "reset" or message != "disconnect" or not self.killed:
                    msgcl = self.client.recv(1024)
                    if not msgcl: break  # prevents infinite loop on disconnect
                    
                    message = msgcl.decode()
                    logging.info(f"Message from {addr}: {message}")

                    self.__handle(message, addr)
                    # Handle function for readability

                logging.info(f"Client at {addr} disconnected.")
                self.client.close()
            self.__close()
        self.__close()

    def __handle(self, message: str, addr: tuple):
        match message:
            case "dostuff":
                print("didstuff")
                self.client.send("didstuff".encode())

            case "kill":
                logging.info(f"Kill requested by {addr}...")
                self.killed = True  # avoid adding a condition to while loops

            case "reset":
                logging.info(
                    f"Client at {addr} requested a reset.")

    def __close(self):
        try:
            self.client.send("kill".encode())
            self.client.close()
        except AttributeError:
            pass  # client not
        self.server.close()

    def kill(self):
        self.killed = True


if __name__ == "__main__":
    server = Server(HOST)
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: killing server...")
        server.kill()
