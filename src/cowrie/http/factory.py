# Copyright (C) 2023 Your Name
"""
HTTP Proxy Factory
"""

from twisted.internet import protocol
from cowrie.http_proxy.simple_transport import SimpleHTTPTransport
from cowrie.pool_interface.handler import PoolHandler
from typing import TYPE_CHECKING
from twisted.plugin import IPlugin
from twisted.python import log

if TYPE_CHECKING:
    from twisted.cred import portal as tp
    
class HTTPProxyFactory(protocol.Factory):
    starttime: float
    tac: IPlugin
    def __init__(self, backend: str, pool_handler: PoolHandler):
        self.portal: tp.Portal | None = None  # gets set by Twisted plugin
        self.backend: str = backend
        self.pool_handler = pool_handler
        super().__init__()

    def startFactory(self):
        if self.backend == "proxy":
            log.msg(
                f"HTTPProxyFactory started in proxy mode"
            )
            self.protocol = lambda: SimpleHTTPTransport()
        else:
            raise ValueError(Exception(f"HTTP: unsupported backend type {self.backend}, only support proxy"))
        
        protocol.ServerFactory.startFactory(self)
        
    def stopFactory(self):
        protocol.ServerFactory.stopFactory(self)
