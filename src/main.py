import asyncio

from eitleain import Eitleain

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    eitleain = Eitleain()
    loop.run_until_complete(eitleain.watch())
