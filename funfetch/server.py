import aiohttp.web
import asyncio
import logging
from .model import Response
from .converter import Converter

log = logging.getLogger("FunFetch")


class Server:
    """Funfetch IPC Server.
    Receive requests from clients.

    Attributes
    ----------
    host: str
        Host on ipc server.

    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        password: str = "1234",
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
    ):
        self.password = password
        self.loop = loop

        self.host = host
        self.port = port

        self.ipc_server = None
        self.routes = {}

    def use(self, name=None):
        """Register the function with the ipc server

        Parameters
        ----------
        name: str
            route(endpoint) name.
        """

        def decorator(func):
            if not name:
                self.routes[func.__name__] = func
            else:
                self.routes[name] = func
            return func

        return decorator

    async def response(self, res: aiohttp.web.Request):
        """Handle aiohttp web response

        Parameters
        ----------
        res: aiohttp.web.Request
            The request made by the client, parsed by aiohttp.
        """
        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(res)

        async for msg in websocket:
            req = msg.json()

            route = req.get("route")
            headers = req.get("headers")

            if not headers or headers.get("Authorization") != self.password:
                response = {"error": "Invalid or no token provided.", "code": 403}
                log.info("Received unauthorized request (Invalid or no token provided).")
            else:
                if not route or route not in self.routes:
                    log.info("Received invalid request (Invalid or no endpoint given).")
                    response = {"error": "Invalid or no endpoint given.", "code": 400}
                else:
                    server_response = Response(req)
                    r = server_response.to_dict().get("data")
                    r = await Converter.return_dict(r)
                    log.info(f"Received request: {route}")

                    try:
                        ret = await self.routes[route](**r)
                        response = ret
                    except Exception as error:
                        log.info(f"Received request: {route}, return Error")
                        response = {
                            "error": "IPC route raised error of type {}".format(
                                type(error).__name__
                            ),
                            "message": str(error),
                            "code": 500,
                        }
            try:
                await websocket.send_json(response)
            except TypeError as error:
                if str(error).startswith("Object of type") and str(error).endswith(
                    "is not JSON serializable"
                ):
                    error_response = (
                        "IPC route returned values which are not able to be sent over sockets."
                        " If you are trying to send a discord.py object,"
                        " please only send the data you need."
                    )
                    log.error(error_response)
                    response = {"error": error_response, "code": 500}
                    await websocket.send_json(response)
                    raise TypeError(error_response)

    async def __start__(self, app, port: int):
        """Starting IPC Server"""
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()

        site = aiohttp.web.TCPSite(runner, self.host, port)
        await site.start()

    def start(self):
        self.ipc_server = aiohttp.web.Application()
        self.ipc_server.router.add_route("GET", "/", self.response)
        self.loop.run_until_complete(self.__start__(self.ipc_server, self.port))

    def run(self):
        self.ipc_server = aiohttp.web.Application()
        self.ipc_server.router.add_route("GET", "/", self.response)
        aiohttp.web.run_app(self.ipc_server, port=self.port)
