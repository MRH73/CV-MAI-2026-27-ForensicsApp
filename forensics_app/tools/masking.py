from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk, messagebox

from PIL import Image, ImageChops

from forensics_app.core import ImageDocument
from forensics_app.ui.main_window import OPEN_TYPES
from .base import ForensicsTool, ToolResult


class _MaskingDialog(simpledialog.Dialog):
    def __init__(self, parent: tk.Misc) -> None:
        self.threshold: tk.StringVar
        self.target: tk.StringVar
        self.texture: tk.StringVar
        self.result: tuple[int, str, str | None] | None = None

        super().__init__(parent, title="Masking")

    def body(self, master: tk.Misc) -> tk.Widget:
        self.threshold = tk.StringVar(value="0")
        self.target = tk.StringVar(value="")
        self.texture = tk.StringVar(value="")
        frame = ttk.Frame(master, padding=10)
        frame.pack(fill="both", expand=True)

        # Threshold
        ttk.Label(frame, text="Threshold:").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 10)
        )
        ttk.Spinbox(frame, from_=0, to=255, textvariable=self.threshold, width=8).grid(
            row=0, column=1, sticky="w", pady=(0, 10)
        )

        # Target image
        ttk.Label(frame, text="Target image:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 10)
        )
        ttk.Entry(frame, textvariable=self.target, state="readonly", width=40).grid(
            row=1, column=1, sticky="ew", pady=(0, 10)
        )
        ttk.Button(frame, text="Open image", command=self._choose_target).grid(
            row=1, column=2, padx=(10, 0), pady=(0, 10)
        )

        # Texture image
        ttk.Label(frame, text="Texture (optional):").grid(
            row=2, column=0, sticky="w", padx=(0, 10)
        )
        ttk.Entry(frame, textvariable=self.texture, state="readonly", width=40).grid(
            row=2, column=1, sticky="ew"
        )
        ttk.Button(frame, text="Open image", command=self._choose_texture).grid(
            row=2, column=2, padx=(10, 0)
        )

        return frame

    def _choose_target(self) -> None:
        path = filedialog.askopenfilename(
            title="Select target image", filetypes=OPEN_TYPES
        )
        if path:
            self.target.set(path)

    def _choose_texture(self) -> None:
        path = filedialog.askopenfilename(
            title="Select texture image", filetypes=OPEN_TYPES
        )
        if path:
            self.texture.set(path)

    def validate(self) -> bool:
        try:
            threshold = int(self.threshold.get())
            if not 0 <= threshold <= 255:
                raise ValueError
        except ValueError:
            messagebox.showinfo(
                "Invalid input",
                "Threshold must be an integer between 0 and 255.",
                parent=self
            )
            return False

        if not self.target.get():
            messagebox.showinfo(
                "Missing target",
                "Select a target image.",
                parent=self
            )
            return False

        return True

    def apply(self) -> None:
        self.result = (int(self.threshold.get()), self.target.get(), self.texture.get() or None)


class MaskingTool(ForensicsTool):
    tool_id = "masking"
    title = "Masking"
    category = "Image processing"
    description = ("Create a mask from the working image "
                   "and apply it to a target image with an optional texture.")

    def run(self, parent: tk.Misc, document: ImageDocument) -> ToolResult | None:

        assert document.current is not None
        source = document.current

        dialog = _MaskingDialog(parent)

        if dialog.result is None:
            return None

        threshold, target_path, texture_path = dialog.result

        try:
            with Image.open(target_path) as target_image:
                target = target_image.convert("RGBA")

            if texture_path is not None:
                with Image.open(texture_path) as texture_image:
                    foreground = texture_image.convert("RGBA")
            else:
                foreground = source.convert("RGBA")
        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"Failed to load image: {e}",
                parent=parent,
            )
            return None

        if target.size != source.size or foreground.size != source.size:
            messagebox.showerror(
                "Size error",
                f"All images must have the same size {source.size}.",
                parent=parent
            )
            return None

        source_gray = source.convert("L")
        mask = source_gray.point(lambda p: 255 if p > threshold else 0)

        if "A" in source.getbands():
            alpha = source.getchannel("A")
            mask = ImageChops.multiply(mask, alpha)

        output = Image.composite(foreground, target, mask)

        return ToolResult(
            image=output,
            message="Applied threshold masking successfully",
            details={
                "Operation": "Masking",
                "Threshold": threshold,
                "Source": Path(document.path).name if document.path else "None",
                "Target": Path(target_path).name,
                "Texture": Path(texture_path).name if texture_path else "None",
                "Output mode": output.mode
            }
        )
