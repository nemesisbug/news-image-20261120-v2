"""Renewal entrypoint: hand the rendered front page to the grader.

The repository carries entry.png, a 1024x1024 PNG drawn by build_image.py.
This module copies it into the directory named by MAKEFUN_OUTPUT_DIR (or
/output when the variable is absent) and confirms the copy is identical.
It touches no network and keeps no state between runs."""
from os import environ, makedirs
from pathlib import Path
from shutil import copyfile

_IMAGE = Path(__file__).resolve().parent / "entry.png"
_OUTPUT = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"

_PAYLOAD = _IMAGE.read_bytes()
if _PAYLOAD[:4] != b"\x89PNG":
    raise SystemExit("entry.png failed the PNG signature check")
makedirs(_OUTPUT.parent, exist_ok=True)
copyfile(_IMAGE, _OUTPUT)
if _OUTPUT.read_bytes() != _PAYLOAD:
    raise SystemExit("copied bytes differ from the repository image")
print(f"wrote {_OUTPUT} ({len(_PAYLOAD)} bytes)")
