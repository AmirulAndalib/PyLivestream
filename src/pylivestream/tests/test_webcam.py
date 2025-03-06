import pylivestream as pls
import pytest

from pathlib import Path
import sys
from pytest import approx
import subprocess
import os
import platform

TIMEOUT = 30
CI = os.environ.get("CI", None) in ("true", "True")
WSL = "Microsoft" in platform.uname().release
ini = Path(__file__).parents[1] / "data/pylivestream.json"


@pytest.mark.parametrize("site", ["localhost", "facebook"])
def test_props(site):
    S = pls.Camera(ini, websites=site)

    assert "-re" not in S.stream.cmd
    assert S.stream.fps == approx(30.0)

    if int(S.stream.res[1]) == 480:
        assert S.stream.video_kbps == 1250
    elif int(S.stream.res[1]) == 720:
        assert S.stream.video_kbps == 1800


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.skipif(CI or WSL, reason="has no camera typically")
def test_stream():
    S = pls.Camera(ini, websites="localhost", timeout=5)

    S.stream.startlive()


@pytest.mark.skipif(CI or WSL, reason="has no camera typically")
def test_script():
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pylivestream.camera",
            "localhost",
            str(ini),
            "--yes",
            "--timeout",
            "5",
        ],
        timeout=TIMEOUT,
    )
