import asyncio

import json
import webbrowser

from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol

class SofiEventProcessor(object):
    """Event handler providing hooks for callback functions"""

    handlers = { 'init': { '_': [] },
                 'load': { '_': [] },
                 'close': { '_': [] },
                 'click': { '_': [] },
                 'mousedown': { '_': [] },
                 'mouseup': { '_': [] },
                 'keydown': { '_': [] },
                 'keyup': { '_': [] },
                 'keypress': { '_': [] }
               }

    def register(self, event, callback, element='_'):
        if event in self.handlers:
            self.handlers[event][element].append(callback)

    def dispatch(self, command):
        self.protocol.sendMessage(bytes(json.dumps(command), 'utf-8'), False)

    @asyncio.coroutine
    def process(self, protocol, event):
        self.protocol = protocol
        eventtype = event['event']

        if eventtype in self.handlers:
            for handler in self.handlers[eventtype]['_']:
                if callable(handler):
                    command = yield from handler(self)

                    if command:
                        self.dispatch(command)


            if 'element' in event:
                element = event['element']

                if element in self.handlers[eventtype]:
                    for handler in self.handlers[eventtype][element]:
                        if callable(handler):
                            command = yield from handler(self)

                            if command:
                                self.dispatch(command)


class SofiEventProtocol(WebSocketServerProtocol):
    """Websocket event handler which dispatches events to SofiEventProcessor"""

    def onConnect(self, request):
        print("Client connecting: %s" % request.peer)

    def onOpen(self):
        print("WebSocket connection open")

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode('utf-8')))
            body = json.loads(payload.decode('utf-8'))

            if 'event' in body:
                yield from self.processor.process(self, body)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        exit(0)


class SofiEventServer(object):
    """Websocket event server"""

    def __init__(self, hostname=u"127.0.0.1", port=9000, processor=None):

        self.hostname = hostname
        self.port = port
        self.processor = processor

        factory = WebSocketServerFactory(u"ws://" + hostname + u":" + str(port))
        protocol = SofiEventProtocol
        protocol.processor = processor
        protocol.app = self

        factory.protocol = protocol

        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_server(factory, '0.0.0.0', port)

    def start(self):
        self.loop.run_until_complete(self.server)

        try:
            webbrowser.open('file:///Users/cabkarian/apps/sofi/main.html')
            self.loop.run_forever()

        except KeyboardInterrupt:
            pass

        finally:
            self.server.close()
            self.loop.close()

    def __repr__(self):
        return "<EventServer(%s, %s)>" % (self.hostname, self.port)

    def __str__(self):
        return repr(self)
