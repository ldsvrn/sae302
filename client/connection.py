#!/usr/bin/env python3
import threading
import socket
import sys

HOST = ("127.0.0.1", int(sys.argv[1]))

class Connection:
    def __init__(self) -> None:
        self.client = socket.socket()
        try:
            self.client.connect(HOST)
        except PermissionError:
            print(f"Permissions insuffisantes pour utiliser le port {HOST[1]}")
            sys.exit(13) # EACCES Permission denied
        except ConnectionRefusedError:
            print(f"Impossible de ce connecter au serveur {HOST}")
            sys.exit(118) # EHOSTUNREACH Host is unreachable
        else:
            client_handler = threading.Thread(target=self.handle, args=[self.client])
            client_handler.start()

            msgcl = ""
            while msgcl != "disconnect" and msgcl != "kill":
                msgcl = input("Message:")
                self.client.send(msgcl.encode())
            self.client.close()

    
    def handle(self, conn) -> None:
        while True:
            msgsrv = conn.recv(1024)
            if not msgsrv: break # prevents infinite loop on disconnect
            msgsrv = msgsrv.decode()
            print(f"\nMessage du serveur: {msgsrv}")
            match msgsrv:
                case "kill":
                    break
        conn.close()

if __name__ == "__main__":
    conn= Connection()