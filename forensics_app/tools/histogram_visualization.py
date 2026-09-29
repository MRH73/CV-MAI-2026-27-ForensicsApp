"""Tool that displays a histogram of an image."""

from __future__ import annotations

import tkinter as tk

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from forensics_app.core import ImageDocument
from .base import ForensicsTool, ToolResult



class HistogramTool(ForensicsTool):
    tool_id = "histogram_visualization"
    title = "Show image histogram"
    category = "Visualization"
    description = "Display a continuous histogram of an image."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult:
        assert document.current is not None  # guarded by the main window

        image = document.current
        fig = plt.figure()

        if image.mode == "L":
            gray = np.array(image)
            gray_hist = np.bincount(gray.ravel(), minlength=256)

            plt.plot(gray_hist, color="tab:orange")

        else:
            image = image.convert("RGB")
            array = np.array(image)

            red_hist = np.bincount(array[:, :, 0].ravel(), minlength=256)
            green_hist = np.bincount(array[:, :, 1].ravel(), minlength=256)
            blue_hist = np.bincount(array[:, :, 2].ravel(), minlength=256)

            gray = np.array(image.convert("L"))
            gray_hist = np.bincount(gray.ravel(), minlength=256)

            plt.plot(red_hist, color="tab:red")
            plt.plot(green_hist, color="tab:green")
            plt.plot(blue_hist, color="tab:blue")
            plt.plot(gray_hist, color="tab:orange")

        fig.canvas.draw()
        array = np.asarray(fig.canvas.buffer_rgba())
        output = Image.fromarray(array).convert("RGB")

        plt.close(fig)

        return ToolResult(
            image=output,
            message="Displayed image histogram.",
            details={"Operation": "Histogram", "Output mode": output.mode},
        )
