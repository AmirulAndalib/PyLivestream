import signal
import argparse

from .api import stream_camera


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    p = argparse.ArgumentParser(description="livestream camera")
    p.add_argument("websites", help="site to stream, e.g. localhost youtube facebook twitch")
    p.add_argument("json", help="JSON file with stream parameters such as key")
    p.add_argument("-y", "--yes", help="no confirmation dialog", action="store_true")
    p.add_argument("-t", "--timeout", help="stop streaming after --timeout seconds", type=int)
    P = p.parse_args()

    stream_camera(ini_file=P.json, websites=P.websites, assume_yes=P.yes, timeout=P.timeout)
