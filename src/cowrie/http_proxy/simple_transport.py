# Copyright (C) 2023 Your Name
"""
HTTP Simple Transport for the Proxy
"""

from twisted.internet import protocol

from cowrie.core.config import CowrieConfig
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.python import log


class SimpleHTTPTransport(protocol.Protocol):
    backend_ip: str
    backend_port: int

    def __init__(self):
        super().__init__()
        self.backend_ip = CowrieConfig.get("proxy", "http_backend_host")
        self.backend_port = CowrieConfig.getint("proxy", "http_backend_port")

    def connectionMade(self):
        c = ClientCreator(reactor, Clienttransfer)
        c.connectTCP(self.backend_ip, self.backend_port).addCallback(self.set_protocol)
        self.transport.pauseProducing()

    def set_protocol(self, p):
        log.msg(f"SimpleHTTPTransport set_protocol {p}")
        self.server = p
        p.set_protocol(self)

    def dataReceived(self, data):
        self.server.transport.write(data)

    def connectionLost(self, reason):
        self.transport.loseConnection()
        self.server.transport.loseConnection()


class Clienttransfer(protocol.Protocol):
    def __init__(self):
        pass

    def set_protocol(self, p):
        self.server = p
        self.server.transport.resumeProducing()
        pass

    def dataReceived(self, data):
        self.server.transport.write(data)
        pass
