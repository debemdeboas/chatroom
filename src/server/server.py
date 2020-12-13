import socket
import logging

from threading import Thread
from typing import Set

from ..common import datatypes

logging.debug('getting logger for', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Client:
    def __init__(self, socket: socket.socket, broadcast) -> None:
        self.socket = socket
        self.name = 'guest'
        self.disconnect_after = 5 # 5 empty messages
        self.broadcast = broadcast

    def handle(self):
        while True:
            bytes = self.socket.recv(datatypes.BUF_SIZE)
            msg = bytes.decode(datatypes.ENCODING)
            if msg == '':
                self.disconnect_counter = self.disconnect_counter - 1
            elif '[name]' in msg:
                self.name = msg[6:]
            if self.disconnect_after <= 0:
                self.socket.close()
                break
            logger.debug(f'Received message: {msg}')
            self.broadcast(self, msg)
        logger.info(f'Client {self.socket} disconnected')


class Server:
    ADDRESS = ('', 15894) # all interfaces

    @staticmethod
    def create_socket() -> socket.socket:
        if socket.has_dualstack_ipv6():
            s = socket.create_server(Server.ADDRESS, family=socket.AF_INET6, dualstack_ipv6=True, backlog=3)
        else:
            s = socket.create_server(Server.ADDRESS, backlog=3)
        logger.debug(f'Socket created: {s}')
        return s

    def __init__(self) -> None:
        self._socket: socket.socket = Server.create_socket()
        self._clients: Set[Client] = set()

    def run(self):
        while True:
            client_socket, client_addr = self._socket.accept()
            client = Client(client_socket, self.broadcast)
            self._clients.add(client)
            logger.info(f'Client {client_addr} connected')
            logger.debug(f'Clients: {self._clients}')
            Thread(target=client.handle, daemon=True).start()

    def broadcast(self, sender: Client, message: str):
        for client in self._clients:
            client.socket.sendall(f'{sender.name}: {message}'.encode())
