"""Local developer entry point."""

from __future__ import annotations

from .web import create_app


def main() -> None:
    create_app().run(host="127.0.0.1", port=8790, debug=False)
