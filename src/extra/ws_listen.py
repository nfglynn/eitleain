#!/usr/bin/env python

import asyncio
import websockets


@asyncio.coroutine
def echo_ws():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    while True:
        data = yield from websocket.recv()
        if data is None:
            break
        print(data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(echo_ws())
    #asyncio.get_event_loop().run_forever()
