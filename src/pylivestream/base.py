from pathlib import Path
import os

from .stream import Stream
from .utils import run, check_device

__all__ = ["FileIn", "Microphone", "SaveDisk", "Screenshare", "Camera"]


class Livestream(Stream):
    def __init__(self, inifn: Path, site: str, **kwargs) -> None:
        super().__init__(inifn, site, **kwargs)

        self.site = site.lower()

        self.osparam(inifn)

        self.docheck = kwargs.get("docheck")

        self.video_bitrate()

        vidIn: list[str] = self.videoIn()
        vidOut: list[str] = self.videoOut()

        audIn: list[str] = self.audioIn()
        audOut: list[str] = self.audioOut()

        buf: list[str] = self.buffer()
        # %% begin to setup command line
        cmd: list[str] = []
        cmd.append(self.exe)

        cmd += self.loglevel
        cmd += self.yes

        #        cmd += self.timelimit  # terminate input after N seconds, IF specified

        cmd += self.queue

        cmd += vidIn + audIn

        if not self.movingimage:  # FIXME: need a different filter chain to caption moving images
            cmd += self.F.drawtext(self.caption)

        cmd += vidOut + audOut
        cmd += buf

        cmd.extend(self.timelimit)  # terminate output after N seconds, IF specified

        streamid = self.streamid if hasattr(self, "streamid") else ""
        # cannot have double quotes for Mac/Linux,
        #    but need double quotes for Windows
        sink: str = self.url + "/" + streamid
        if os.name == "nt":
            sink = '"' + sink + '"'

        self.sink = sink
        cmd.append(sink)

        self.cmd: list[str] = cmd
        # %% quick check command, to verify device exists
        # 0.1 seems OK, spurious buffer error on Windows that wasn't helped by any bigger size
        CHECKTIMEOUT = "0.1"

        self.checkcmd: list[str] = (
            [self.exe]
            + self.loglevel
            + ["-t", CHECKTIMEOUT]
            + self.videoIn(quick=True)
            + self.audioIn(quick=True)
            + ["-t", CHECKTIMEOUT]
            + ["-f", "null", "-"]  # camera needs at output
        )

    def startlive(self):
        """
        start the stream(s)
        """

        if self.docheck:
            self.check_device()

        proc = None
        # %% special cases for localhost tests
        if self.site == "localhost-test":
            pass
        elif self.site == "localhost":
            proc = self.F.listener()  # start own RTMP server

        if proc is not None and proc.poll() is not None:
            # listener stopped prematurely, probably due to error
            raise RuntimeError(f"listener stopped with code {proc.poll()}")
        # %% RUN STREAM
        run(self.cmd)

        # %% stop the listener before starting the next process, or upon final process closing.
        if proc is not None and proc.poll() is None:
            proc.terminate()
        yield

    def check_device(self, site: str | None = None) -> bool:
        """
        requires stream to have been configured first.
        does a quick test stream to "null" to verify device is actually accessible
        """
        if not site:
            try:
                site = self.site
            except AttributeError:
                site = list(self.streams.keys())[0]  # type: ignore

        try:
            checkcmd = self.checkcmd
        except AttributeError:
            checkcmd = self.streams[site].checkcmd  # type: ignore

        return check_device(checkcmd)


# %% operators
class Screenshare:
    def __init__(self, inifn: Path, websites: str, **kwargs) -> None:

        self.streams = Livestream(inifn, websites, vidsource="screen", **kwargs)

    def golive(self) -> None:

        self.streams.startlive()


class Camera:
    def __init__(self, inifn: Path, websites: str, **kwargs):

        self.streams = Livestream(inifn, websites, vidsource="camera", **kwargs)

    def golive(self) -> None:

        self.streams.startlive()


class Microphone:
    def __init__(self, inifn: Path, websites: str, **kwargs):

        self.streams = Livestream(inifn, websites, **kwargs)

    def golive(self) -> None:

        self.streams.startlive()


# %% File-based inputs
class FileIn:
    def __init__(self, inifn: Path, websites: str, **kwargs):

        self.streams = Livestream(inifn, websites, vidsource="file", **kwargs)

    def golive(self) -> None:

        self.streams.startlive()


class SaveDisk(Stream):
    def __init__(self, inifn: Path, outfn: Path | None = None, **kwargs):
        """
        records to disk screen capture with audio

        if not outfn, just cite command that would have run
        """
        super().__init__(inifn, site="file", vidsource="screen", **kwargs)

        self.outfn = Path(outfn).expanduser() if outfn else None

        self.osparam(inifn)

        vidIn: list[str] = self.videoIn()
        vidOut: list[str] = self.videoOut()

        audIn: list[str] = self.audioIn()
        audOut: list[str] = self.audioOut()

        self.cmd: list[str] = [str(self.exe)]
        self.cmd += vidIn + audIn
        self.cmd += vidOut + audOut

        # ffmpeg relies on suffix for container type, this is a fallback.
        if self.outfn and not self.outfn.suffix:
            self.cmd += ["-f", "flv"]

        self.cmd += [str(self.outfn)]

    #        if sys.platform == 'win32':  # doesn't seem to be needed.
    #            cmd += ['-copy_ts']

    def save(self):

        if self.outfn:
            run(self.cmd)

        else:
            print("specify filename to save screen capture w/ audio to disk.")
