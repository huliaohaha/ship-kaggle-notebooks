# 图表复现说明（含改进与对比实验）

本仓库脚本 `scripts/reproduce_electric_cars_figure.py` 用于复现
`electric-cars-extensive-eda-with-feature-engine.ipynb` 中“类别分布（饼图 + 柱状图）”风格图表，
并新增了一个改进模块与对比实验结果保存。

## 本次改进模块

改进点：**柱状图可读性模块（bar labeling）**

- 基线版本：柱状图仅显示缩写标签（`BEV` / `PHEV`）。
- 改进版本：
  - 显示完整类别名称；
  - 柱顶增加“计数 + 百分比”；
  - 增加 y 轴网格线；
  - 饼图中心显示总样本数。

## 使用方式

```bash
python scripts/reproduce_electric_cars_figure.py --output-repo ../paper-figures-repo
```

## 运行后输出

会在独立仓库（默认 `../paper-figures-repo`）中生成：

- `images/electric_vehicle_type_distribution_baseline.svg`
- `images/electric_vehicle_type_distribution_improved.svg`
- `comparison/report.md`（对比实验说明）
- `comparison/comparison_metrics.json`（对比实验指标）

> 说明：默认使用脚本内置示例数据，保证在无 Kaggle 数据和无第三方绘图库环境下也可稳定生成论文配图与对比结果。
