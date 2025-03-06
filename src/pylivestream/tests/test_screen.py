import pytest
from pytest import approx
from pathlib import Path
import subprocess
import os
import platform
import sys

import pylivestream as pls

TIMEOUT = 30
CI = os.environ.get("CI", None) in ("true", "True")
WSL = "Microsoft" in platform.uname().release
ini = Path(__file__).parents[1] / "data/pylivestream.json"


@pytest.mark.parametrize("site", ["facebook"])
def test_props(site):
    S = pls.Screenshare(ini, websites=site)

    assert "-re" not in S.streams.cmd
    assert S.streams.fps == approx(30.0)

    assert S.streams.video_kbps == 1250


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.skipif(CI or WSL, reason="has no GUI")
def test_stream():
    S = pls.Screenshare(ini, websites="localhost", timeout=5)

    S.golive()


@pytest.mark.skipif(CI or WSL, reason="no GUI typically")
def test_script():
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pylivestream.screen",
            "localhost",
            str(ini),
            "--yes",
            "--timeout",
            "5",
        ],
        timeout=TIMEOUT,
    )
