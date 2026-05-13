"""
模拟运行引擎

处理模拟运行的业务逻辑
"""

from typing import Any, Callable, Dict, Optional

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


class SimulationEngine:
    """模拟运行引擎"""

    def __init__(self):
        """初始化引擎"""
        self.config = None
        self.results = {}
        self.progress_callback = None

    def set_progress_callback(self, callback: Callable[[float, str], None]) -> None:
        """设置进度回调函数

        Args:
            callback: 回调函数，接收进度(0-1)和状态消息
        """
        self.progress_callback = callback

    def run_simulation(
        self, params: Dict[str, Any], schemes: list, exact_solution: bool = False
    ) -> Dict[str, Any]:
        """运行模拟

        Args:
            params: 物理参数
            schemes: 数值格式列表
            exact_solution: 是否计算精确解

        Returns:
            Dict[str, Any]: 模拟结果
        """
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import get_scheme

            # 创建配置
            self.config = DamBreakConfig(**params)

            results = {
                "config": self.config,
                "schemes": {},
                "exact": None,
                "success": True,
                "errors": {},
            }

            # 计算精确解
            if exact_solution:
                try:
                    from src.core.solvers.exact_riemann import ExactRiemann

                    exact_solver = ExactRiemann(self.config)
                    results["exact"] = exact_solver.solve(self.config)
                except ImportError:
                    pass

            # 运行各格式模拟
            for idx, scheme_name in enumerate(schemes):
                if self.progress_callback:
                    progress = (idx + 1) / len(schemes)
                    self.progress_callback(progress, f"计算 {scheme_name}...")

                try:
                    scheme = get_scheme(scheme_name)
                    result = _adapt_scheme_for_evolve(scheme, self.config)

                    if not result:
                        results["errors"][scheme_name] = {"error": "模拟结果为空"}
                        continue

                    results["schemes"][scheme_name] = result

                    # 计算误差
                    if results["exact"] is not None:
                        final_t = max(result.keys())
                        final_result = result[final_t]
                        if final_result.ndim >= 2 and final_result.shape[0] >= 1:
                            errors = self._compute_errors(
                                final_result[0, :], results["exact"][0, :]
                            )
                            results["errors"][scheme_name] = errors
                        else:
                            results["errors"][scheme_name] = {"error": "结果格式异常"}

                except Exception as e:
                    results["errors"][scheme_name] = {"error": str(e)}

            return results

        except ImportError as e:
            return {
                "success": False,
                "error": f"核心模块未实现: {e}",
                "config": None,
                "schemes": {},
                "exact": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "config": None,
                "schemes": {},
                "exact": None,
            }

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

    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要

        Returns:
            Dict[str, Any]: 配置摘要
        """
        if self.config is None:
            return {}

        return {
            "domain_length": self.config.domain_length,
            "grid_points": self.config.nx,
            "dam_position": self.config.x_dam,
            "left_depth": self.config.h_l,
            "right_depth": self.config.h_r,
            "gravity": self.config.g,
            "end_time": self.config.t_end,
            "cfl": self.config.cfl,
        }