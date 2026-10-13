"""Main window: prompt box, style picker, live preview grid, export button."""
from __future__ import annotations

import logging

import wx

from stickerforge.config.loader import ForgeConfig
from stickerforge.handlers.prompt_handler import PromptHandler
from stickerforge.services.pipeline import ForgePipeline

log = logging.getLogger("stickerforge.ui.main_frame")


class MainFrame(wx.Frame):
    def __init__(self, *, cfg: ForgeConfig, preset: str) -> None:
        super().__init__(None, title="ai-sticker-emoji-forge", size=(960, 640))
        self._cfg = cfg
        self._pipeline = ForgePipeline(cfg=cfg, preset_name=preset)
        self._handler = PromptHandler(pipeline=self._pipeline)
        self._build_ui()

    def _build_ui(self) -> None:
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.prompt_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 80))
        self.prompt_box.SetHint("a chonky cat wearing sunglasses, sticker, thick outline")
        sizer.Add(self.prompt_box, 0, wx.EXPAND | wx.ALL, 8)

        self.style_picker = wx.Choice(panel, choices=["sticker", "emoji", "kawaii", "pixel", "flat"])
        self.style_picker.SetSelection(0)
        sizer.Add(self.style_picker, 0, wx.ALL, 8)

        self.forge_btn = wx.Button(panel, label="Forge")
        self.forge_btn.Bind(wx.EVT_BUTTON, self._on_forge)
        sizer.Add(self.forge_btn, 0, wx.ALL, 8)

        self.preview = wx.ListCtrl(panel, style=wx.LC_ICON | wx.LC_AUTOARRANGE)
        sizer.Add(self.preview, 1, wx.EXPAND | wx.ALL, 8)

        panel.SetSizer(sizer)

    def _on_forge(self, _evt: wx.CommandEvent) -> None:
        prompt = self.prompt_box.GetValue().strip()
        if not prompt:
            return
        style = self.style_picker.GetString(self.style_picker.GetSelection())
        log.info("forge requested: style=%s", style)
        try:
            result = self._handler.run(prompt=prompt, style=style)
            log.info("forged -> %s", result.path)
        except Exception as exc:
            wx.MessageBox(str(exc), "Forge failed", wx.ICON_ERROR)