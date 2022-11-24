#!/usr/bin/env python3

import threading
import socket
import logging

logging.basicConfig(level=logging.DEBUG)

# TODO: Detect IP?
HOST = ("127.0.0.1", 1000)


class Server:
    def __init__(self, host: tuple) -> None:
        server = socket.socket()
        server.bind(host)
        server.listen()

        self.clients = []

        while True:
            conn, addr = server.accept()
            logging.info(f"Connected to {addr}")

            thread = threading.Thread(target=self.handle, args=(conn, addr))
            # keeping sockets and threads in a list of tuples
            self.clients.append(zip(addr, conn, thread))

            thread.start()

    def handle(client: socket.socket, addr: tuple) -> None:
        # TODO: remove while true maybe
        while True:
            message = client.recv(1024)
            logging.info(f"Message from {addr}: {message}")

            match message:
                case "dostuff":
                    pass


if __name__ == "__main__":
    Server(HOST)
