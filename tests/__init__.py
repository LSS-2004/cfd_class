# Tests package
"""
测试代码包

结构：
- unit/: 单元测试
- integration/: 集成测试
- performance/: 性能基准测试
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
