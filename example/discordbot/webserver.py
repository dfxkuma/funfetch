from quart import Quart
from funfetch import Client


app = Quart(__name__)
ipc_client = Client()


@app.route("/")
async def index():
    member_count = ipc_client.get_member_count(guild_id=12345678)
    return str(member_count)


if __name__ == "__main__":
    app.run()
