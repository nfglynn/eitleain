import asyncio
import sys
import contextlib
import locale
from pathlib import Path


class Dump1090Protocol(asyncio.SubprocessProtocol):
    def __init__(self):
        self._exited = False
        self._closed_stdout = False
        self._closed_stderr = False

    @property
    def finished(self):
        return self._exited and self._closed_stdout and self._closed_stderr

    def signal_exit(self):
        if not self.finished:
            return
        #loop.stop() 

    def pipe_data_received(self, fd, data):
        if fd == 1:
            name = 'stdout'
        elif fd == 2:
            name = 'stderr'
        text = data.decode(locale.getpreferredencoding(False))
        print('Received from {}: {}'.format(name, text.strip()))

    def pipe_connection_lost(self, fd, exc):
        if fd == 1:
            self._closed_stdout = True
        elif fd == 2:
            self._closed_stderr = True
        self.signal_exit()

    def process_exited(self):
        self._exited = True
        self.signal_exit()


class Dump1090(object):
    @property
    def path(self) -> Path:
        return str(Path('/usr/local/bin/dump1090'))

    def watch(self) -> None:
        loop = asyncio.get_event_loop()
        with contextlib.closing(loop):
            import ipdb; ipdb.set_trace()
            proc = loop.subprocess_shell(Dump1090Protocol,
                                         self.path)
            transport, protocol = loop.run_until_complete(proc)
            loop.run_forever()
            print('Program exited with: {}'.format(transport.get_returncode()))

    def __exit__(self):
        pass


class Speir(object):
    def __init__(self):
        self.radar = Dump1090()

    def watch(self):
        self.radar.watch()


def main():
    speir = Speir()
    speir.watch()
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
