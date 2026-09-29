"""Tools that reorder the RGB channels of an image."""

# RGB -> BGR right now, according to the example in the slides.
from __future__ import annotations

import tkinter as tk

import numpy as np
from PIL import Image

from forensics_app.core import ImageDocument
from .base import ForensicsTool, ToolResult


class BGRChannelSwapTool(ForensicsTool):
    """Display the image with its red and blue channels exchanged."""

    tool_id = "channel_swap_bgr"
    title = "BGR"
    category = "Channel permutations"
    description = "Reorder the image channels from RGB to BGR."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        # MainWindow checks that an image is loaded before running this tool.
        assert document.original is not None

        # Work from the original image so future channel permutations remain independent
        rgb_image = np.array(document.original.convert("RGB"))

        # Extract each channel from the final RGB ()for this to work it has to be a numpy array.
        red = rgb_image[:, :, 0]
        green = rgb_image[:, :, 1]
        blue = rgb_image[:, :, 2]

        bgr_image = np.stack((blue, green, red), axis=2) # Combine the B, G, and R channels into a 3D image array
        output = Image.fromarray(bgr_image, mode="RGB")

        return ToolResult(
            image=output,
            message="Reordered image channels from RGB to BGR.",
            details={"Channel order": "BGR", "Output mode": output.mode},
        )
