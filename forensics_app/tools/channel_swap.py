"""Tools that reorder the RGB channels of an image."""
from __future__ import annotations

import tkinter as tk

import numpy as np
from PIL import Image

from forensics_app.core import ImageDocument
from .base import ForensicsTool, ToolResult


class ChannelSwapTool(ForensicsTool):
    """Display the image with channels arranged in a selected order."""

    category = "Channel permutations"

    def __init__(self, order: str) -> None:
        # This constructs the class based on the selected channel order.
        order = order.upper()

        if len(order) != 3 or set(order) != {"R", "G", "B"}:
            raise ValueError("The order must be an RGB permutation, such as 'BGR'.")

        self.order = order
        self.tool_id = f"channel_swap_{order.lower()}"
        self.title = order
        self.description = f"Swap image channels to {order}."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        # MainWindow checks that an image is loaded before running this tool.
        assert document.original is not None

        # Work from the original image.
        rgb_image = np.array(document.original.convert("RGB"))

        # channel_index translates each channel letter to its position in the RGB array at the beginning
        channel_index = {"R": 0, "G": 1, "B": 2}

        # indices stores the source-array positions in the exact selected output order.
        indices = []

        for channel in self.order:
            indices.append(channel_index[channel])

        # indexing builds a new image array by selecting channels in indices order.
        output_array = rgb_image[:, :, indices]
        output = Image.fromarray(output_array, mode="RGB")

        return ToolResult(
            image=output,
            message=f"Swapped image channels to {self.order}.",
            details={"Channel order": self.order, "Output mode": output.mode},
        )
