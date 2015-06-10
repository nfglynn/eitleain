import asyncio
import websockets

from eitleain import Eitleain


def server(websocket, path):
    eitleain = Eitleain()
    while True:
        data = yield from eitleain.watch()
        print(data)
        yield from websocket.send(data)


if __name__ == '__main__':
    run_server = websockets.serve(server, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(run_server)
    asyncio.get_event_loop().run_forever()
