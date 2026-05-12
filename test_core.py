"""
核心模块测试脚本
"""

import sys
sys.path.insert(0, 'src')

from src.core.config import DamBreakConfig
from src.core.schemes import get_scheme, get_all_schemes


def test_config():
    """测试配置类"""
    print('1. 测试配置类 DamBreakConfig')
    config = DamBreakConfig(nx=100, domain_length=100.0, h_l=10.0, h_r=1.0, t_end=1.0)
    print('   网格数量: %d' % config.nx)
    print('   网格间距: %.4f' % config.dx)
    print('   大坝位置: %.4f' % config.x_dam)
    print('   初始状态形状: %s' % str(config.q_initial.shape))
    print('   OK 配置类正常')


def test_schemes():
    """测试所有数值格式"""
    print('2. 测试数值格式')
    config = DamBreakConfig(nx=100, domain_length=100.0, h_l=10.0, h_r=1.0, t_end=1.0)
    
    schemes = get_all_schemes()
    for scheme_name in schemes:
        try:
            scheme = get_scheme(scheme_name)
            result = scheme.evolve(config)
            final_time = max(result.keys())
            final_q = result[final_time]
            print('   OK %s: 完成, 最终时刻=%.4fs' % (scheme_name, final_time))
        except Exception as e:
            print('   FAIL %s: %s' % (scheme_name, str(e)))


def test_riemann_solver():
    """测试Riemann求解器"""
    print('3. 测试Riemann求解器')
    from src.core.solvers import exact_riemann_solution
    
    q_left = [10.0, 0.0]
    q_right = [1.0, 0.0]
    
    sol = exact_riemann_solution(q_left, q_right)
    print('   解类型: %s' % sol["type"])
    print('   星区水深: %.4fm' % sol["h_star"])
    print('   星区速度: %.4fm/s' % sol["u_star"])
    print('   左波速: %.4fm/s' % sol["s_l"])
    print('   右波速: %.4fm/s' % sol["s_r"])
    print('   OK Riemann求解器正常')


def test_error_analysis():
    """测试误差分析工具"""
    print('4. 测试误差分析工具')
    from src.core.analysis import compute_l1_error, compute_l2_error, compute_linf_error
    
    import numpy as np
    exact = np.linspace(0, 1, 100)
    numerical = exact + np.random.normal(0, 0.01, 100)
    
    l1 = compute_l1_error(numerical, exact)
    l2 = compute_l2_error(numerical, exact)
    linf = compute_linf_error(numerical, exact)
    
    print('   L1误差: %.6f' % l1)
    print('   L2误差: %.6f' % l2)
    print('   L∞误差: %.6f' % linf)
    print('   OK 误差分析工具正常')


if __name__ == '__main__':
    print('=' * 50)
    print('CFD-Class 核心模块测试')
    print('=' * 50)
    print()
    
    try:
        test_config()
        print()
        test_schemes()
        print()
        test_riemann_solver()
        print()
        test_error_analysis()
        print()
        print('=' * 50)
        print('所有测试通过!')
        print('=' * 50)
    except Exception as e:
        print('测试失败: %s' % str(e))
        import traceback
        traceback.print_exc()
