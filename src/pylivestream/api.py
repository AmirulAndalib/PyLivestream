"""
importable functions for use from other Python programs

Example:

import pylivestream.api as pls

pls.microphone('localhost')
pls.microphone('twitch')
"""

from pathlib import Path

from .base import FileIn, Microphone, SaveDisk, Camera
from .screen import stream_screen

__all__ = [
    "stream_file",
    "stream_microphone",
    "stream_camera",
    "stream_screen",
    "capture_screen",
]


def stream_file(
    ini_file: Path,
    websites: str,
    video_file: Path,
    loop: bool | None = None,
    assume_yes: bool = False,
    timeout: float | None = None,
):
    S = FileIn(ini_file, websites, infn=video_file, loop=loop, yes=assume_yes, timeout=timeout)

    print(" ".join(S.stream.cmd))


def stream_microphone(
    ini_file: Path,
    websites: str,
    *,
    still_image: Path | None = None,
    assume_yes: bool | None = False,
    timeout: float | None = None,
):
    """
    livestream audio, with still image background
    """

    S = Microphone(ini_file, websites, image=still_image, yes=assume_yes, timeout=timeout)

    print(" ".join(S.stream.cmd))


def capture_screen(
    ini_file: Path, *, out_file: Path, assume_yes: bool = False, timeout: float | None = None
):

    s = SaveDisk(ini_file, out_file, yes=assume_yes, timeout=timeout)
    # %%
    if assume_yes:
        print("saving screen capture to", s.outfn)
    else:
        input(f"Press Enter to screen capture to file {s.outfn}   Or Ctrl C to abort.")

    s.save()


def stream_camera(ini_file: Path, websites: str, *, assume_yes: bool, timeout: float):

    S = Camera(ini_file, websites, yes=assume_yes, timeout=timeout)

    print(" ".join(S.stream.cmd))
