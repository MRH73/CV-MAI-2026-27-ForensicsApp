from __future__ import annotations

import tkinter as tk
from PIL import Image
from skimage import exposure
import numpy as np

from forensics_app.core import ImageDocument
from .base import ForensicsTool, ToolResult

LOWER_PERCENTILE = 10
UPPER_PERCENTILE = 90


class ContrastStretchingTool(ForensicsTool):
    tool_id = "contrast_stretching"
    title = "Contrast stretching"
    category = "Intensity"
    description = "Stretches the image histogram between specified percentiles."

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult | None:
        assert document.current is not None

        image = np.asarray(document.current)

        pl, pu = np.percentile(image, (LOWER_PERCENTILE, UPPER_PERCENTILE))

        output = exposure.rescale_intensity(image, in_range=(pl, pu), out_range=(0, 255))
        output = Image.fromarray(output.astype(np.uint8))

        return ToolResult(
            image=output,
            message="Stretched the image contrast successfully.",
            details={"Output mode": output.mode,
                     "Lower percentile": f"{pl: .2f}",
                     "Upper percentile": f"{pu: .2f}"
                     },
        )
