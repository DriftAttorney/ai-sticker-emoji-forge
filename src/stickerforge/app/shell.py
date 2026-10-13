"""wxPython desktop shell. Windows-first, falls back gracefully on Linux."""
from __future__ import annotations

import logging

from stickerforge.config.loader import ForgeConfig

log = logging.getLogger("stickerforge.shell")


def launch_shell(*, cfg: ForgeConfig, preset: str) -> int:
    import wx  # imported lazily so headless CI never touches wxPython

    from stickerforge.app.ui.main_frame import MainFrame

    app = wx.App(redirect=False)
    frame = MainFrame(cfg=cfg, preset=preset)
    frame.Show()
    app.MainLoop()
    return 0