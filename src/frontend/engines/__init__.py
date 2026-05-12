"""
CFD-Class Frontend Engines Module

业务逻辑引擎模块

引擎列表:
- simulation_engine: 模拟运行引擎
- comparison_engine: 格式对比引擎
- report_engine: 报告生成引擎
"""

__version__ = "0.1.0"
__author__ = "CFD-Team"

from .comparison_engine import ComparisonEngine
from .report_engine import ReportEngine
from .simulation_engine import SimulationEngine

__all__ = [
    "SimulationEngine",
    "ComparisonEngine",
    "ReportEngine",
]
