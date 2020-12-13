import socket
import logging

from threading import Thread
from typing import List

from ..common import datatypes

logging.debug('getting logger for', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Client:
    @staticmethod
    def create_socket(addr: str = '') -> socket.socket:
        s = socket.create_connection((addr, 15894))
        logger.debug(f'Socket created: {s}')
        return s

    def __init__(self, addr: str = '', on_message: List = []) -> None:
        self.on_message_receival = on_message
        self._socket = Client.create_socket(addr)
        Thread(target=self.handle, daemon=True).start()

    def send(self, msg: str) -> None:
        return self.sendbytes(msg.encode(datatypes.ENCODING))

    def sendbytes(self, msg: bytes) -> None:
        logger.info(f'Sending message: {msg}')
        self._socket.send(msg)

    def handle(self):
        while True:
            bytes = self._socket.recv(datatypes.BUF_SIZE)
            msg = bytes.decode(datatypes.ENCODING)
            logger.info(f'Received message: {msg}')
            self._on_message_receival(msg)

    def _on_message_receival(self, msg: str):
        for func in self.on_message_receival:
            try:
                func(msg)
            except Exception as E:
                logger.error(E)