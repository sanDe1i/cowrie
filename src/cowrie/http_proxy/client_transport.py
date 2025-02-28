# Copyright (C) 2023 Your Name
"""
HTTP Backend Transport for the Proxy
"""

from twisted.internet import protocol
from twisted.python import log

from twisted.conch.telnet import HTTP, TelnetTransport

class BackendHTTPTransport(protocol.Protocol):
    def __init__(self):
        self.server = None

    def connectionMade(self):
        log.msg(f"Connected to HTTP backend at {self.transport.getPeer().host}")
        self.server.backend_protocol = self  # 将后端实例绑定到前端

    def sendData(self, data: bytes) -> None:
        """接收前端数据并发送到后端"""
        self.transport.write(data)
        log.msg(f"Forwarded {len(data)} bytes to backend")

    def dataReceived(self, data: bytes) -> None:
        """忽略后端响应（不转发给攻击者）"""
        log.msg(f"Received {len(data)} bytes from backend (ignored)")

    def connectionLost(self, reason):
        log.msg("Backend HTTP connection closed")