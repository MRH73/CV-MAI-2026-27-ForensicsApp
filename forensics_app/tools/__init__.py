"""Register course functionality here so it appears in the sidebar."""

from .grayscale import GrayscaleTool
from .image_info import ImageInfoTool
from .masking import MaskingTool
from .registry import ToolRegistry
from .channel_split import RedChannelTool, GreenChannelTool, BlueChannelTool
from .histogram_visualization import HistogramTool
from .channel_swap import ChannelSwapTool


def build_tool_registry() -> ToolRegistry:
    return ToolRegistry(
        [
            ImageInfoTool(),
            GrayscaleTool(),
            # Tools for each channel.
            RedChannelTool(),
            GreenChannelTool(),
            BlueChannelTool(),
            HistogramTool(),
            ChannelSwapTool("RGB"),
            ChannelSwapTool("RBG"),
            ChannelSwapTool("GRB"),
            ChannelSwapTool("GBR"),
            ChannelSwapTool("BRG"),
            ChannelSwapTool("BGR"),
            MaskingTool(),
        ]
    )


__all__ = ["ToolRegistry", "build_tool_registry"]
