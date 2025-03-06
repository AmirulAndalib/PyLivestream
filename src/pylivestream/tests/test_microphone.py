"""
timeout= parameter needs to be at least 10 seconds for audio stream to show in FFplay
"""

import sys
from pathlib import Path
import pylivestream as pls
import pytest
import subprocess
import os
import platform
import importlib.resources

TIMEOUT = 30
CI = os.environ.get("CI", None) in ("true", "True")
WSL = "Microsoft" in platform.uname().release
ini = Path(__file__).parents[1] / "data/pylivestream.json"


@pytest.mark.parametrize("site", ["facebook"])
def test_microphone_props(site):

    logo = importlib.resources.files("pylivestream.data").joinpath("logo.png")
    S = pls.Microphone(ini, websites=site, image=logo)

    assert "-re" not in S.stream.cmd
    assert S.stream.fps is None
    assert S.stream.res == [720, 540]

    assert S.stream.video_kbps == 800


@pytest.mark.parametrize("site", ["facebook"])
def test_microphone_image(site):

    img = importlib.resources.files("pylivestream.data").joinpath("check4k.png")
    S = pls.Microphone(ini, websites=site, image=img)

    assert "-re" not in S.stream.cmd
    assert S.stream.fps is None
    assert S.stream.res == [3840, 2160]

    assert S.stream.video_kbps == 4000


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.skipif(CI or WSL, reason="has no audio hardware typically")
def test_stream():
    S = pls.Microphone(ini, websites="localhost", image=None, timeout=10)

    S.stream.startlive()


@pytest.mark.skipif(CI or WSL, reason="has no audio hardware typically")
def test_script():
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pylivestream.microphone",
            "localhost",
            str(ini),
            "--yes",
            "--timeout",
            "10",
        ],
        timeout=TIMEOUT,
    )
