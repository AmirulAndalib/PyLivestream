from pathlib import Path
import signal
import argparse

from .base import Screenshare


def stream_screen(
    ini_file: Path, websites: str, *, assume_yes: bool = False, timeout: float | None = None
):

    S = Screenshare(ini_file, websites, yes=assume_yes, timeout=timeout)

    print(" ".join(S.stream.cmd))


def cli():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    p = argparse.ArgumentParser(description="livestream screenshare")
    p.add_argument("websites", help="site to stream, e.g. localhost youtube facebook twitch")
    p.add_argument("json", help="JSON file with stream parameters such as key")
    p.add_argument("-y", "--yes", help="no confirmation dialog", action="store_true")
    p.add_argument("-t", "--timeout", help="stop streaming after --timeout seconds", type=int)
    P = p.parse_args()

    stream_screen(ini_file=P.json, websites=P.websites, assume_yes=P.yes, timeout=P.timeout)


if __name__ == "__main__":
    cli()
