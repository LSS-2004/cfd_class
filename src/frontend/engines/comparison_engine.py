"""
格式对比引擎

处理格式对比分析的业务逻辑
"""

from typing import Any, Dict, List, Optional

import numpy as np
from numpy.typing import NDArray


class ComparisonEngine:
    """格式对比引擎"""

    def __init__(self):
        """初始化引擎"""
        self.results = {}
        self.config = None

    def run_comparison(
        self, params: Dict[str, Any], schemes: List[str], compute_exact: bool = True
    ) -> Dict[str, Any]:
        """运行格式对比（模拟后端计算）

        Args:
            params: 物理参数
            schemes: 格式列表
            compute_exact: 是否计算精确解

        Returns:
            Dict[str, Any]: 对比结果
        """
        try:
            L = params.get("L", params.get("domain_length", 10.0))
            nx = params.get("nx", 200)
            h_L = params.get("h_L", params.get("h_l", 2.0))
            h_R = params.get("h_R", params.get("h_r", 1.0))
            t_end = params.get("t_end", 1.0)
            
            x = np.linspace(0, L, nx)

            results = {
                "x": x,
                "params": params,
                "schemes": {},
                "exact": None,
                "errors": {},
                "performance": {},
                "success": True,
            }

            for scheme_name in schemes:
                try:
                    import time

                    start_time = time.time()

                    t_steps = 10
                    times = np.linspace(0, t_end, t_steps)
                    scheme_result = {}

                    for t in times:
                        sigma = 1.0 + t * 0.5
                        peak_factor = max(0.1, 1 - t / t_end * 0.3)
                        
                        h = h_R + (h_L - h_R) * (
                            0.5 * (1 + np.tanh((L/2 - x) / sigma)) * peak_factor +
                            0.2 * np.exp(-((x - L/2)**2) / (2 * sigma**2))
                        )
                        
                        if "Lax-Friedrichs" in scheme_name:
                            h += np.random.normal(0, 0.05, len(x)) * h * 0.05
                        elif "Lax-Wendroff" in scheme_name:
                            h += np.random.normal(0, 0.03, len(x)) * h * 0.03
                        elif "MacCormack" in scheme_name:
                            h += np.random.normal(0, 0.02, len(x)) * h * 0.02
                        elif "Godunov" in scheme_name:
                            h = np.maximum(h_R * 0.9, h)
                        elif "HLL" in scheme_name:
                            h = np.maximum(h_R * 0.85, h)
                        elif "MUSCL" in scheme_name:
                            h += np.random.normal(0, 0.01, len(x)) * h * 0.01
                        
                        h = np.maximum(h_R * 0.5, h)
                        scheme_result[round(t, 2)] = np.vstack([h, np.zeros_like(h)])

                    end_time = time.time()
                    computation_time = (end_time - start_time) * 1000

                    results["schemes"][scheme_name] = scheme_result
                    results["performance"][scheme_name] = {
                        "time_ms": computation_time,
                        "grid_points": nx,
                    }

                    l1 = np.sum(np.abs(h - h.mean())) / len(h) * 0.05
                    l2 = np.sqrt(np.sum((h - h.mean())**2) / len(h)) * 0.05
                    linf = np.max(np.abs(h - h.mean())) * 0.1
                    results["errors"][scheme_name] = {"l1": l1, "l2": l2, "linf": linf}

                except Exception as e:
                    results["errors"][scheme_name] = {"error": str(e)}

            return results

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _compute_errors(
        self, numerical: NDArray[np.float64], exact: NDArray[np.float64]
    ) -> Dict[str, float]:
        """计算误差

        Args:
            numerical: 数值解
            exact: 精确解

        Returns:
            Dict[str, float]: 误差字典
        """
        dx = 1.0

        l1 = np.sum(np.abs(numerical - exact)) / len(exact) * dx
        l2 = np.sqrt(np.sum((numerical - exact) ** 2) / len(exact)) * dx
        linf = np.max(np.abs(numerical - exact))

        return {"l1": l1, "l2": l2, "linf": linf}

    def get_comparison_summary(self) -> Dict[str, Any]:
        """获取对比摘要

        Returns:
            Dict[str, Any]: 对比摘要
        """
        if not self.results:
            return {}

        summary = {
            "schemes": list(self.results.get("schemes", {}).keys()),
            "has_exact": self.results.get("exact") is not None,
            "errors": {},
            "best_l1": None,
            "best_linf": None,
            "fastest": None,
        }

        errors = self.results.get("errors", {})
        if errors:
            valid_errors = {k: v for k, v in errors.items() if "error" not in v}

            if valid_errors:
                summary["best_l1"] = min(
                    valid_errors.items(), key=lambda x: x[1].get("l1", float("inf"))
                )
                summary["best_linf"] = min(
                    valid_errors.items(), key=lambda x: x[1].get("linf", float("inf"))
                )

        performance = self.results.get("performance", {})
        if performance:
            summary["fastest"] = min(
                performance.items(), key=lambda x: x[1].get("time_ms", float("inf"))
            )

        return summary