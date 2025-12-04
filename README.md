# 🏡 House & Browse - Housing Affordability Dashboard

一个交互式的美国住房可负担性数据可视化仪表板，包含两个不同的设计。

## 📋 项目结构

```
DATA511 project/
├── app.py                    # 主应用入口（包含导航）
├── pages/
│   ├── intro.py             # 介绍页面
│   ├── design1.py           # Design 1: 交互式地图探索器
│   └── design2.py           # Design 2: 时间序列对比
├── desgin1/                 # Design 1 的源代码和数据
│   ├── app.py
│   ├── charts.py
│   ├── config_data.py
│   ├── geo_utils.py
│   ├── events.py
│   └── data/
│       ├── house_ts_agg.csv
│       ├── cbsa_shapes.zip
│       └── zcta_shapes.zip
├── design2/                  # Design 2 的源代码和数据
│   ├── design2.py
│   ├── home.py
│   └── HouseTS.csv
└── requirements.txt         # 项目依赖
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中打开，默认地址为 `http://localhost:8501`

## 🎯 功能说明

### 🏠 Intro 页面
- 项目介绍
- 两个设计的说明
- 价格收入比（PTI）的计算方法
- 参考文献

### 🗺️ Design 1: 交互式地图探索器
**主要功能：**
- **Metro 级别可视化**：交互式 choropleth 地图
- **钻取功能**：从 Metro 区域钻取到 ZIP 代码
- **多种指标**：价格收入比（PTI）和中位数售价
- **历史趋势**：单个 ZIP 代码的时间序列分析
- **地理探索**：可点击的地图

**使用方法：**
1. 使用顶部的控制面板选择年份和指标
2. 在地图上点击 Metro 区域查看 ZIP 代码详情
3. 点击 ZIP 代码查看详细指标和历史趋势

### 📊 Design 2: 时间序列对比
**主要功能：**
- **多城市对比**：价格收入比的时间序列对比
- **可负担性等级可视化**：带颜色编码的等级带
- **交互式选择**：可选择多个大都市区
- **年度分析**：2012-2023 年的年度变化

**使用方法：**
1. 在左侧面板选择要对比的大都市区
2. 图表会自动更新显示选中的城市
3. 悬停查看详细数据

## 📊 数据说明

### 数据源
- **HouseTS Dataset**: 来自 Kaggle，包含 30 个主要美国大都市区 2012-2023 年的数据
- **Shapefiles**: CBSA 和 ZCTA 边界数据用于地图可视化

### 指标定义

**价格收入比（PTI）**
```
PTI = median_sale_price / (per_capita_income × 2.51)
```
其中 2.51 是美国家庭中位数规模。

**可负担性等级：**
- **0.0-3.0**: 可负担 🟢
- **3.1-4.0**: 中等不可负担 🟡
- **4.1-5.0**: 严重不可负担 🟠
- **5.1-8.9**: 极度不可负担 🔴
- **9.0+**: 不可能负担 ⚫

## 🛠️ 技术栈

- **Streamlit**: Web 应用框架
- **Plotly**: 交互式图表和地图
- **GeoPandas**: 地理空间数据处理
- **Pandas**: 数据处理
- **NumPy**: 数值计算

## 📚 参考文献

- **数据集**: shengkunwang. (2025). *HouseTS Dataset*. Kaggle
- **可负担性等级**: Cox, Wendell (2025). *Demographia International Housing Affordability, 2025 Edition*. Center for Demographics and Policy

## 🔧 故障排除

### Design 1 无法加载数据
- 确保 `desgin1/data/house_ts_agg.csv` 文件存在
- 检查 shapefile ZIP 文件是否完整

### Design 2 无法加载数据
- 确保 `design2/HouseTS.csv` 文件存在
- 检查文件路径是否正确

### 地图不显示
- 确保已安装所有依赖（特别是 geopandas 和 shapely）
- 检查 shapefile 文件是否完整

## 📝 注意事项

- Design 1 需要较大的内存来处理地理数据
- 首次加载地图可能需要一些时间
- 建议使用现代浏览器以获得最佳体验

