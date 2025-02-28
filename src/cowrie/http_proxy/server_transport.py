# Copyright (C) 2023 Your Name
"""
HTTP Frontend Transport for the Proxy
"""

from __future__ import annotations

from twisted.internet import reactor, protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.python import log

from cowrie.core.config import CowrieConfig
from cowrie.http_proxy import client_transport

class FrontendHTTPTransport(protocol.Protocol):
    def __init__(self):
        self.backend_connected = False
        self.backend_protocol = None
        self.delayed_data = []
        self.backend_ip = CowrieConfig.get("proxy", "http_backend_host")
        self.backend_port = CowrieConfig.getint("proxy", "http_backend_port")

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg(
            f"New HTTP connection from {peer.host}:{peer.port} -> Forwarding to {self.backend_ip}:{self.backend_port}"
        )
        # 立即建立后端连接
        self.connect_to_backend()

    def dataReceived(self, data: bytes) -> None:
        if self.backend_connected:
            self.backend_protocol.sendData(data)
        else:
            self.delayed_data.append(data)

    def connect_to_backend(self):
        factory = protocol.ClientFactory()
        factory.protocol = client_transport.BackendHTTPTransport
        factory.server = self  # 将前端实例传递给后端协议

        endpoint = TCP4ClientEndpoint(reactor, self.backend_ip, self.backend_port, timeout=10)
        d = endpoint.connect(factory)
        d.addCallback(self.backend_connection_success)
        d.addErrback(self.backend_connection_failed)

    def backend_connection_success(self, backend_protocol):
        self.backend_protocol = backend_protocol
        self.backend_connected = True
        # 发送缓存的数据
        for data in self.delayed_data:
            backend_protocol.sendData(data)
        self.delayed_data = []

    def backend_connection_failed(self, reason):
        log.msg(f"Failed to connect to HTTP backend: {reason.getErrorMessage()}")
        self.transport.loseConnection()

    def connectionLost(self, reason):
        if self.backend_protocol:
            self.backend_protocol.transport.loseConnection()