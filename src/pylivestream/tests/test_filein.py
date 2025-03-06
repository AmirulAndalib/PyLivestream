import pytest
from pytest import approx
from pathlib import Path
import subprocess
import os
import sys
import importlib.resources

import pylivestream as pls

TIMEOUT = 30
CI = os.environ.get("CI", None) in ("true", "True")
ini = Path(__file__).parents[1] / "data/pylivestream.json"


@pytest.mark.parametrize("site", ["facebook"])
def test_props(site):

    vid = importlib.resources.files("pylivestream.data").joinpath("bunny.avi")
    S = pls.FileIn(ini, websites=site, infn=vid)

    assert "-re" in S.stream.cmd
    assert S.stream.fps == approx(24.0)

    if int(S.stream.res[1]) == 480:
        assert S.stream.video_kbps == 500
    elif int(S.stream.res[1]) == 720:
        assert S.stream.video_kbps == 1800


@pytest.mark.parametrize("site", ["facebook"])
def test_audio(site):

    logo = importlib.resources.files("pylivestream.data").joinpath("logo.png")
    snd = importlib.resources.files("pylivestream.data").joinpath("orch_short.ogg")

    S = pls.FileIn(ini, websites=site, infn=snd, image=logo)
    assert "-re" in S.stream.cmd
    assert S.stream.fps is None

    assert S.stream.video_kbps == 800


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.skipif(CI, reason="CI has no audio hardware typically")
def test_simple():
    """stream to localhost"""
    logo = importlib.resources.files("pylivestream.data").joinpath("logo.png")
    aud = importlib.resources.files("pylivestream.data").joinpath("orch_short.ogg")

    S = pls.FileIn(ini, websites="localhost", infn=aud, image=logo, yes=True, timeout=5)

    S.stream.startlive()


@pytest.mark.skipif(CI, reason="CI has no audio hardware typically")
def test_script():
    vid = importlib.resources.files("pylivestream.data").joinpath("bunny.avi")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pylivestream.fglob",
            str(vid),
            "localhost",
            str(ini),
            "--yes",
            "--timeout",
            "5",
        ],
        timeout=TIMEOUT,
    )
