#!/usr/bin/env python3

import threading
import socket
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

# TODO: Detect IP?
HOST = ("127.0.0.1", int(sys.argv[1]))


class Server:
    def __init__(self, host: tuple) -> None:
        self.server = socket.socket()
        self.server.bind(host)
        self.server.listen()

        self.clients = []

        while True:
            conn, addr = self.server.accept()
            logging.info(f"Connected to {addr}")

            thread = threading.Thread(target=self.handle, args=(conn, addr))
            # keeping sockets and threads in a list of tuples
            self.clients.append((addr, conn, thread))

            thread.start()

    def handle(self, client: socket.socket, addr: tuple) -> None:
        # TODO: remove while true maybe
        while True:
            message = client.recv(1024)
            if not message:
                break  # prevents infinite loop on disconnect
            message = message.decode()
            logging.info(f"Message from {addr}: {message}")

            match message:
                case "dostuff":
                    print("didstuff")
                    client.send("didstuff".encode())

                case "kill":
                    logging.info(f"Kill requested by {addr}...")
                    for i in self.clients:
                        logging.info(f"Diconnecting {i[0]}...")
                        i[1].close()

                    logging.info("Closing server...")
                    self.server.close()

                case "disconnect":
                    logging.info(f"Client at {addr} disconnected.")
                    client.close()
                    break


if __name__ == "__main__":
    Server(HOST)
