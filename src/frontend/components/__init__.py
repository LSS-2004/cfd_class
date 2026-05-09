"""
CFD-Class Frontend Components Module

可复用的 Streamlit UI 组件

组件列表:
- navigation: 导航组件
- parameter_panel: 参数面板组件
- plot_display: 绑图显示组件
- scheme_selector: 格式选择器组件
"""

__version__ = "0.1.0"
__author__ = "CFD-Team"

from .navigation import render_navigation
from .parameter_panel import render_parameter_panel
from .plot_display import render_plot
from .scheme_selector import render_scheme_selector

__all__ = [
    "render_navigation",
    "render_parameter_panel",
    "render_plot",
    "render_scheme_selector",
]
