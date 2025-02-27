# Copyright (C) 2023 Your Name
"""
HTTP Proxy Factory
"""

from twisted.internet import protocol
from twisted.python import log

class HTTPProxyFactory(protocol.Factory):
    def __init__(self):
        self.protocol = FrontendHTTPTransport

    def startFactory(self):
        log.msg("HTTP proxy started on port 8080 (forwarding to backend)")

    def stopFactory(self):
        log.msg("HTTP proxy stopped")