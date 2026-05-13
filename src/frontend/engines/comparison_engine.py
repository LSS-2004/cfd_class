"""
格式对比引擎

处理格式对比分析的业务逻辑
"""

from typing import Any, Dict, List, Optional

import numpy as np
from numpy.typing import NDArray


def _adapt_scheme_for_evolve(scheme, config):
    """适配层：为scheme添加evolve方法兼容

    Args:
        scheme: 数值格式实例
        config: DamBreakConfig配置对象

    Returns:
        模拟结果字典
    """
    if hasattr(scheme, 'evolve'):
        return scheme.evolve(config)
    
    h0, u0 = config.initial_condition()
    dx = config.dx
    result = scheme.run_simulation(
        h0=h0, u0=u0, cfl=config.cfl, dx=dx, t_end=config.t_end
    )
    
    output = {}
    for i, t in enumerate(result.t):
        h = result.h[i]
        u = result.u[i]
        output[round(float(t), 6)] = np.vstack([h, u])
    return output


class ComparisonEngine:
    """格式对比引擎"""

    def __init__(self):
        """初始化引擎"""
        self.results = {}
        self.config = None

    def run_comparison(
        self, params: Dict[str, Any], schemes: List[str], compute_exact: bool = True
    ) -> Dict[str, Any]:
        """运行格式对比

        Args:
            params: 物理参数
            schemes: 格式列表
            compute_exact: 是否计算精确解

        Returns:
            Dict[str, Any]: 对比结果
        """
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import get_scheme

            self.config = DamBreakConfig(**params)

            results = {
                "config": self.config,
                "schemes": {},
                "exact": None,
                "errors": {},
                "performance": {},
                "success": True,
            }

            # 计算精确解
            if compute_exact:
                try:
                    from src.core.solvers.exact_riemann import ExactRiemann

                    exact_solver = ExactRiemann(self.config)
                    results["exact"] = exact_solver.solve(self.config)
                except ImportError:
                    pass

            # 运行各格式
            for scheme_name in schemes:
                try:
                    import time

                    start_time = time.time()

                    scheme = get_scheme(scheme_name)
                    result = _adapt_scheme_for_evolve(scheme, self.config)

                    end_time = time.time()
                    computation_time = (end_time - start_time) * 1000  # ms

                    if not result:
                        results["errors"][scheme_name] = {"error": "模拟结果为空"}
                        continue

                    results["schemes"][scheme_name] = result
                    results["performance"][scheme_name] = {
                        "time_ms": computation_time,
                        "grid_points": self.config.nx,
                    }

                    # 计算误差
                    if results["exact"] is not None:
                        final_t = max(result.keys())
                        final_result = result[final_t]
                        if final_result.ndim >= 2 and final_result.shape[0] >= 1:
                            numerical = final_result[0, :]
                            exact = results["exact"][0, :]

                            errors = self._compute_errors(numerical, exact)
                            results["errors"][scheme_name] = errors
                        else:
                            results["errors"][scheme_name] = {"error": "结果格式异常"}

                except Exception as e:
                    results["errors"][scheme_name] = {"error": str(e)}

            return results

        except ImportError as e:
            return {"success": False, "error": f"核心模块未实现: {e}"}
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
        dx = self.config.dx if self.config else 1.0

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

        # 找出最佳结果
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

        # 找出最快格式
        performance = self.results.get("performance", {})
        if performance:
            summary["fastest"] = min(
                performance.items(), key=lambda x: x[1].get("time_ms", float("inf"))
            )

        return summary
