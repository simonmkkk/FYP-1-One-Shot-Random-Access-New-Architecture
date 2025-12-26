# Input: 依赖theoretical.py提供theoretical_calculation函数
# Output: 导出theoretical_calculation函数供外部使用
# Position: theoretical子模块的导出接口，统一对外提供理论计算功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

from .theoretical import theoretical_calculation

__all__ = [
    'theoretical_calculation',
]

