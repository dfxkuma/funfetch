import asyncio

from .errors import ConnectionError
from .converter import Converter
import aiohttp


class Client:
    """
    It is a client connecting to the ipc server.

    Parameters
    ----------
    host: str
        This is the host of the ipc server.
    port: int
        This is the port on the ipc server.
    password: Union[str, bytes]
        This is the password used to connect to the ipc server. The default server password is 1234.
    """

    def __init__(
        self, host: str = "localhost", port: int = 8000, password: str = "1234"
    ):
        self.host = host
        self.port = port

        self.password = password

        self.session = None
        self.websocket = None

    async def connect(self):
        """Attempts to connect to the server

        Returns
        -------
        :class:`~aiohttp.ClientWebSocketResponse`
            The websocket connection to the server
        """
        self.session = aiohttp.ClientSession()
        try:
            self.websocket = await self.session.ws_connect(
                self.url, autoping=False, autoclose=False
            )
            return self.websocket
        except Exception as e:
            raise ConnectionError(e)

    @property
    def url(self):
        return "ws://{0.host}:{1}".format(self, self.port)

    def __getattr__(self, item):
        def inner(**kwargs):
            return self.request(route=item, **kwargs)

        return inner

    def __getitem__(self, item):
        def inner(**kwargs):
            return self.request(route=item, **kwargs)

        return inner

    async def request(self, route: str, **kwargs):
        """Make a request to the IPC server process.

        Parameters
        ----------
        route: str
            he endpoint to request on the server
        **kwargs
            The data to send to the endpoint
        """
        if not self.session:
            await self.connect()
        payload_data = await Converter.converter_string(kwargs)

        payload = {
            "route": route,
            "data": payload_data,
            "headers": {"Authorization": self.password},
        }

        await self.websocket.send_json(payload)

        recv = await self.websocket.receive()

        if recv.type == aiohttp.WSMsgType.PING:
            await self.websocket.ping()

            return await self.request(route, payload_data)

        if recv.type == aiohttp.WSMsgType.PONG:
            return await self.request(route, payload_data)

        if recv.type == aiohttp.WSMsgType.CLOSED:
            await self.session.close()
            await asyncio.sleep(5)
            await self.connect()
            return self.request(route, payload_data)

        return recv.json()
