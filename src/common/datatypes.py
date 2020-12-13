########################################################################
#
#   Constants file
#
#   Constants used by both the client and the server applications
#
########################################################################

import logging

from socket import AF_INET, SOCK_STREAM


BUF_SIZE = 1024

SOCK_TYPE = (AF_INET, SOCK_STREAM)

ENCODING = 'utf-8'

def configure_logger(name: str) -> logging.Logger:
    logging.basicConfig(filename=f'logger.log', level=logging.DEBUG, filemode='w')
    return logging.getLogger(name)