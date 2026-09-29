"""Tools that display the red, green, or blue channel of an image."""

from __future__ import annotations

import tkinter as tk

from forensics_app.core import ImageDocument
from .base import ForensicsTool, ToolResult


class RedChannelTool(ForensicsTool):
    """Display the red channel as a grayscale image."""

    tool_id = "red_channel"
    title = "Show red channel"
    category = "Color channels"
    description = "Display the red channel as a grayscale image."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        # MainWindow checks that an image is loaded before running this tool.
        assert document.original is not None

        # Use the image as it was opened. This way, selecting another channel
        # afterwards still reads its values from the original color image.
        rgb_image = document.original.convert("RGB")

        # split() returns (red, green, blue), in that order. Each channel is a
        # grayscale image
        red_channel, _green_channel, _blue_channel = rgb_image.split()

        return ToolResult(
            image=red_channel,
            message="Displayed the red channel.",
            details={"Channel": "Red", "Output mode": red_channel.mode},
        )


class GreenChannelTool(ForensicsTool):
    """Display the green channel as a grayscale image."""

    tool_id = "green_channel"
    title = "Show green channel"
    category = "Color channels"
    description = "Display the green channel as a grayscale image."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        # MainWindow checks that an image is loaded before running this tool.
        assert document.original is not None

        # Use the original image so channel buttons work independently of
        # which channel was displayed most recently.
        rgb_image = document.original.convert("RGB")

        # split() returns the channels in red, green, blue order.
        _red_channel, green_channel, _blue_channel = rgb_image.split()

        return ToolResult(
            image=green_channel,
            message="Displayed the green channel.",
            details={"Channel": "Green", "Output mode": green_channel.mode},
        )


class BlueChannelTool(ForensicsTool):
    """Display the blue channel as a grayscale image."""

    tool_id = "blue_channel"
    title = "Show blue channel"
    category = "Color channels" #this determines the heading under which button appears
    description = "Display the blue channel as a grayscale image."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        # MainWindow checks that an image is loaded before running this tool.
        assert document.original is not None

        # Convert to RGB first so split() always gives exactly three channels,
        rgb_image = document.original.convert("RGB")

        # The third image returned by split() is the blue channel.
        _red_channel, _green_channel, blue_channel = rgb_image.split()

        return ToolResult(
            image=blue_channel,
            message="Displayed the blue channel.",
            details={"Channel": "Blue", "Output mode": blue_channel.mode},
        )
