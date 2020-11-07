from enum import Enum

class ServerMessage(Enum):
    exit = 1
    nick_taken = 2
    nick_invalid = 3
    connection_established = 4

class ClientMessage(Enum):
    exit = 1