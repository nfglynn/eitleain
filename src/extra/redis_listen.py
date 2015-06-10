import sys
import time
import pprint
import json
import asyncio
import asyncio_redis


@asyncio.coroutine
def listen(channel):
    connection = yield from asyncio_redis.Connection.create()
    subscriber = yield from connection.start_subscribe()
    yield from subscriber.subscribe([channel])

    while True:
        msg = yield from subscriber.next_published()
        try:
            decoded = pprint.pformat(json.loads(msg.value))
        except Exception:
            decoded = msg.value
        print("{}:\n{}\n".format(time.asctime(), decoded))

    connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen(sys.argv[1]))
