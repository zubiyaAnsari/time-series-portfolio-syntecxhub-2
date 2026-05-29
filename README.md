# 📊 Time Series & Category Charts — Week 2 Project
### SyntecxHub Data Analytics Portfolio

A complete data visualisation project built with **Python** and **Matplotlib**, covering time series analysis and category comparisons using synthetic retail sales data.

---

## 📁 Project Structure

```
├── week2_project.py          # Full Python code — data generation + all 5 charts
├── week_2_project.pdf        # Complete project report with code, charts & interpretation
└── charts/
    ├── chart1_line_timeseries.png   # Monthly & quarterly aggregation
    ├── chart2_line_category.png     # Per-category monthly lines
    ├── chart3_bar_category.png      # Annual category comparison
    ├── chart4_pie_share.png         # Revenue share pie chart
    └── chart5_grouped_bar_quarterly.png  # Grouped quarterly bars
```

---

## 📈 Charts Covered

| # | Chart Type | What It Shows |
|---|-----------|---------------|
| 1 | Line + Bar | Total sales monthly & quarterly aggregation |
| 2 | Multi-Line | Monthly sales broken down by category |
| 3 | Bar Chart  | Annual revenue comparison across categories |
| 4 | Pie Chart  | Each category's share of total revenue |
| 5 | Grouped Bar | Quarterly sales per category side-by-side |

---

## 🛠️ Libraries Used

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from reportlab.platypus import ...   # PDF generation
```

Install with:
```bash
pip install pandas numpy matplotlib reportlab pillow
```

---

## 🚀 How to Run

```bash
python week2_project.py
```

All 5 charts will be saved to the `charts/` folder and a PDF report will be generated.

---

## 📌 Key Findings

- **Electronics** is the top revenue category at ~36% of total annual sales
- **Toys** shows the sharpest seasonal spike in Q4 (festive season)
- **Q2** was the strongest quarter overall
- **Books** has the flattest, least seasonal sales curve

---

*Part of the SyntecxHub Data Analytics Portfolio — Week 2*
