# Figure Analysis 子模块架构说明

各图表解析计算子模块，负责生成Figure 1、2、3-5的解析数据。

**文件列表：**
- `__init__.py` - 子模块导出接口，导出所有图表分析函数
- `figure1_analysis.py` - Figure 1解析计算，计算NS,1/N和NC,1/N的精确公式与近似公式
- `figure2_analysis.py` - Figure 2解析计算，基于Figure 1结果计算近似误差分析
- `figure345_analysis.py` - Figure 3-5合并解析计算，同时计算P_S、T_a、P_C三个性能指标

**一旦我所属的文件夹有所变化，请更新我。**

