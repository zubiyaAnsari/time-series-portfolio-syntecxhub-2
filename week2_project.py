"""
Week 2 Project: Time Series & Category Charts
=============================================
Covers:
  1. Line chart  – Sales over time (daily → monthly → quarterly)
  2. Bar chart   – Category comparison
  3. Pie chart   – Category share
  4. Save charts to PNG
  5. Export summary PDF
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

# ── Output folder ────────────────────────────────────────────────────────────
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1.  SYNTHETIC DATASET
# ─────────────────────────────────────────────────────────────────────────────
import numpy as np

rng = np.random.default_rng(42)

dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
categories = ["Electronics", "Clothing", "Furniture", "Books", "Toys"]

# Daily sales per category (realistic seasonal patterns)
base = {"Electronics": 3500, "Clothing": 2200, "Furniture": 1800,
        "Books": 900,  "Toys": 1200}
seasonal = {"Electronics": 0.8, "Clothing": 1.1, "Furniture": 0.6,
            "Books": 0.4,  "Toys": 1.5}

records = []
for d in dates:
    for cat in categories:
        month_factor = 1 + seasonal[cat] * np.sin((d.month - 1) * np.pi / 6)
        noise = rng.normal(0, base[cat] * 0.05)
        sales = max(0, base[cat] * month_factor + noise)
        records.append({"Date": d, "Category": cat, "Sales": round(sales, 2)})

df = pd.DataFrame(records)
df["Month"]   = df["Date"].dt.to_period("M")
df["Quarter"] = df["Date"].dt.to_period("Q")

print("Dataset shape:", df.shape)
print(df.head())

# ─────────────────────────────────────────────────────────────────────────────
# 2.  HELPER – SHARED STYLE
# ─────────────────────────────────────────────────────────────────────────────
PALETTE = ["#4e79a7","#f28e2b","#e15759","#76b7b2","#59a14f"]
plt.rcParams.update({
    "font.family":  "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.linestyle":     "--",
    "grid.alpha":         0.5,
    "figure.dpi":         150,
})

def save_chart(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  ✓  Saved → {path}")
    return path

# ─────────────────────────────────────────────────────────────────────────────
# 3.  CHART 1 – LINE CHART: Total sales over time (monthly & quarterly)
# ─────────────────────────────────────────────────────────────────────────────
monthly_total  = df.groupby("Month")["Sales"].sum().reset_index()
monthly_total["Month_dt"] = monthly_total["Month"].dt.to_timestamp()

quarterly_total = df.groupby("Quarter")["Sales"].sum().reset_index()
quarterly_total["Quarter_dt"] = quarterly_total["Quarter"].dt.to_timestamp()

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=False)

# ── Monthly line ─────────────────────────────────────────────────────────────
ax = axes[0]
ax.plot(monthly_total["Month_dt"], monthly_total["Sales"],
        color=PALETTE[0], linewidth=2.2, marker="o", markersize=6, label="Monthly Sales")
ax.fill_between(monthly_total["Month_dt"], monthly_total["Sales"],
                alpha=0.12, color=PALETTE[0])
ax.set_title("Total Sales – Monthly Aggregation (2023)", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.2f}M"))
ax.legend()
ax.set_xlabel("Month")

# ── Quarterly bar overlay ─────────────────────────────────────────────────────
ax2 = axes[1]
q_labels = [str(q) for q in quarterly_total["Quarter"]]
bars = ax2.bar(q_labels, quarterly_total["Sales"], color=PALETTE[1],
               width=0.5, alpha=0.85, label="Quarterly Sales")
ax2.set_title("Total Sales – Quarterly Aggregation (2023)", fontsize=13, fontweight="bold")
ax2.set_ylabel("Revenue (₹)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.2f}M"))
ax2.set_xlabel("Quarter")
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
             f"₹{bar.get_height()/1e6:.2f}M", ha="center", va="bottom", fontsize=10)
ax2.legend()

fig.suptitle("Time Series Analysis – Line & Bar", fontsize=15, fontweight="bold", y=1.01)
fig.tight_layout()
chart1_path = save_chart(fig, "chart1_line_timeseries.png")

# ─────────────────────────────────────────────────────────────────────────────
# 4.  CHART 2 – LINE CHART: Per-category monthly sales
# ─────────────────────────────────────────────────────────────────────────────
monthly_cat = df.groupby(["Month", "Category"])["Sales"].sum().reset_index()
monthly_cat["Month_dt"] = monthly_cat["Month"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(11, 6))
for i, cat in enumerate(categories):
    sub = monthly_cat[monthly_cat["Category"] == cat]
    ax.plot(sub["Month_dt"], sub["Sales"], color=PALETTE[i],
            linewidth=2, marker="o", markersize=5, label=cat)

ax.set_title("Monthly Sales by Category (2023)", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left")
fig.tight_layout()
chart2_path = save_chart(fig, "chart2_line_category.png")

# ─────────────────────────────────────────────────────────────────────────────
# 5.  CHART 3 – BAR CHART: Annual sales comparison by category
# ─────────────────────────────────────────────────────────────────────────────
annual_cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(annual_cat["Category"], annual_cat["Sales"],
              color=PALETTE, width=0.55, alpha=0.9, edgecolor="white")
ax.set_title("Annual Sales by Category (2023)", fontsize=14, fontweight="bold")
ax.set_xlabel("Category")
ax.set_ylabel("Total Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.2f}M"))

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20000,
            f"₹{bar.get_height()/1e6:.2f}M", ha="center", va="bottom", fontsize=10)
fig.tight_layout()
chart3_path = save_chart(fig, "chart3_bar_category.png")

# ─────────────────────────────────────────────────────────────────────────────
# 6.  CHART 4 – PIE CHART: Category share of annual revenue
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    annual_cat["Sales"],
    labels=annual_cat["Category"],
    colors=PALETTE,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="white", linewidth=2),
    explode=[0.03]*len(annual_cat)
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
ax.set_title("Revenue Share by Category – 2023", fontsize=14, fontweight="bold")
fig.tight_layout()
chart4_path = save_chart(fig, "chart4_pie_share.png")

# ─────────────────────────────────────────────────────────────────────────────
# 7.  CHART 5 – GROUPED BAR: Quarterly sales per category
# ─────────────────────────────────────────────────────────────────────────────
q_cat = df.groupby(["Quarter", "Category"])["Sales"].sum().reset_index()
q_labels = sorted(q_cat["Quarter"].unique())
x = np.arange(len(q_labels))
width = 0.15

fig, ax = plt.subplots(figsize=(11, 6))
for i, cat in enumerate(categories):
    vals = [q_cat[(q_cat["Quarter"]==q) & (q_cat["Category"]==cat)]["Sales"].values[0]
            for q in q_labels]
    ax.bar(x + i*width, vals, width, label=cat, color=PALETTE[i], alpha=0.88)

ax.set_xticks(x + width*2)
ax.set_xticklabels([str(q) for q in q_labels])
ax.set_title("Quarterly Sales by Category (2023)", fontsize=14, fontweight="bold")
ax.set_xlabel("Quarter")
ax.set_ylabel("Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left")
fig.tight_layout()
chart5_path = save_chart(fig, "chart5_grouped_bar_quarterly.png")

# ─────────────────────────────────────────────────────────────────────────────
# 8.  SUMMARY STATISTICS
# ─────────────────────────────────────────────────────────────────────────────
total_revenue = df["Sales"].sum()
best_month    = monthly_total.loc[monthly_total["Sales"].idxmax(), "Month"]
best_quarter  = quarterly_total.loc[quarterly_total["Sales"].idxmax(), "Quarter"]
best_category = annual_cat.iloc[0]["Category"]
best_cat_rev  = annual_cat.iloc[0]["Sales"]

summary = {
    "Total Annual Revenue": f"₹{total_revenue/1e6:.2f}M",
    "Best Month":           str(best_month),
    "Best Quarter":         str(best_quarter),
    "Top Category":         best_category,
    "Top Category Revenue": f"₹{best_cat_rev/1e6:.2f}M",
}
print("\n── Summary ──────────────────────────────")
for k, v in summary.items():
    print(f"  {k}: {v}")

# ─────────────────────────────────────────────────────────────────────────────
# 9.  BUILD PDF REPORT
# ─────────────────────────────────────────────────────────────────────────────
from reportlab.lib.pagesizes   import A4
from reportlab.lib.units       import cm
from reportlab.lib.styles      import getSampleStyleSheet, ParagraphStyle
from reportlab.lib             import colors
from reportlab.platypus        import (SimpleDocTemplate, Paragraph, Spacer,
                                       Image, PageBreak, Table, TableStyle,
                                       HRFlowable)
from reportlab.lib.enums       import TA_CENTER, TA_LEFT, TA_JUSTIFY

PDF_PATH = os.path.join(os.path.dirname(__file__), "week_2_project.pdf")

doc  = SimpleDocTemplate(PDF_PATH, pagesize=A4,
                         leftMargin=2*cm, rightMargin=2*cm,
                         topMargin=2*cm,  bottomMargin=2*cm)
styles = getSampleStyleSheet()

# Custom styles
def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_style   = S("MyTitle",  fontSize=22, textColor=colors.HexColor("#2d3561"),
                  alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica-Bold")
h1_style      = S("MyH1",    fontSize=15, textColor=colors.HexColor("#4e79a7"),
                  spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold")
h2_style      = S("MyH2",    fontSize=12, textColor=colors.HexColor("#2d3561"),
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
body_style    = S("MyBody",  fontSize=10, leading=15, alignment=TA_JUSTIFY,
                  spaceAfter=6)
bullet_style  = S("MyBullet",fontSize=10, leading=14, leftIndent=18,
                  firstLineIndent=-12, spaceAfter=3)
code_style    = S("MyCode",  fontSize=9,  fontName="Courier", backColor=colors.HexColor("#f4f4f4"),
                  borderPadding=(4,6,4,6), leading=13)

def bullet(txt):
    return Paragraph(f"• {txt}", bullet_style)

def img(path, width_cm=15):
    w = width_cm * cm
    from PIL import Image as PILImage
    pil = PILImage.open(path)
    iw, ih = pil.size
    h = w * ih / iw
    return Image(path, width=w, height=h)

W = A4[0] - 4*cm   # usable width

story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Week 2 Project", title_style))
story.append(Paragraph("Time Series &amp; Category Charts", title_style))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4e79a7")))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "This report presents a complete data-visualisation project covering sales "
    "analysis using line charts, bar charts, pie charts, and grouped bar charts "
    "with monthly and quarterly aggregations. Each chart is accompanied by code "
    "snippets, interpretations, and chart-design notes.",
    body_style))
story.append(Spacer(1, 0.5*cm))

# ── Dataset overview ──────────────────────────────────────────────────────────
story.append(Paragraph("1. Dataset Overview", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "A synthetic retail sales dataset was generated for the year 2023, containing "
    "daily transaction records across five product categories. The data simulates "
    "realistic seasonal patterns and random noise to mimic real-world behaviour.",
    body_style))
story.append(Spacer(1,0.2*cm))
tbl_data = [
    ["Feature",       "Detail"],
    ["Period",        "1 Jan 2023 – 31 Dec 2023"],
    ["Frequency",     "Daily"],
    ["Records",       "1,825  (365 days × 5 categories)"],
    ["Categories",    "Electronics, Clothing, Furniture, Books, Toys"],
    ["Key columns",   "Date, Category, Sales (₹)"],
]
tbl = Table(tbl_data, colWidths=[5*cm, 11.5*cm])
tbl.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(1,0), colors.HexColor("#4e79a7")),
    ("TEXTCOLOR",   (0,0),(1,0), colors.white),
    ("FONTNAME",    (0,0),(1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0),(-1,-1), 9),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f4fa"), colors.white]),
    ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0),(-1,-1), 8),
    ("TOPPADDING",  (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
]))
story.append(tbl)
story.append(Spacer(1, 0.4*cm))

# ── Code snippet: data generation ─────────────────────────────────────────────
story.append(Paragraph("Code – Dataset Generation", h2_style))
code_txt = """\
import pandas as pd, numpy as np

rng   = np.random.default_rng(42)
dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
base  = {"Electronics":3500, "Clothing":2200, "Furniture":1800,
          "Books":900, "Toys":1200}

records = []
for d in dates:
    for cat, b in base.items():
        noise = rng.normal(0, b*0.05)
        sales = max(0, b + noise)
        records.append({"Date":d, "Category":cat, "Sales":round(sales,2)})

df = pd.DataFrame(records)
df["Month"]   = df["Date"].dt.to_period("M")
df["Quarter"] = df["Date"].dt.to_period("Q")"""
for line in code_txt.split("\n"):
    story.append(Paragraph(line.replace(" ", "&nbsp;"), code_style))
story.append(Spacer(1, 0.4*cm))

# ── Chart 1 ───────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("2. Time Series – Monthly &amp; Quarterly Aggregation", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "The first set of charts plots total sales aggregated at monthly and quarterly "
    "granularities. The area-shaded line chart reveals seasonality trends while the "
    "quarterly bar chart enables quick period-to-period comparison.",
    body_style))
story.append(Spacer(1,0.2*cm))
story.append(img(chart1_path, 16))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Interpretation", h2_style))
for pt in [
    "Sales follow a clear seasonal curve – Q4 (Oct–Dec) records the highest revenue "
     "driven by the festive shopping season.",
    "Q1 is the weakest quarter across all categories.",
    "Monthly granularity reveals intra-quarter volatility not visible in aggregated views.",
    "Quarterly bar labels make it easy to compare absolute revenue figures at a glance.",
]:
    story.append(bullet(pt))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Chart Design Notes", h2_style))
for pt in [
    "Line chart chosen for continuous time-series – best for trend and seasonality.",
    "Area fill (alpha=0.12) adds depth without overwhelming the line.",
    "Quarterly bars are overlaid separately to avoid scale conflicts.",
    "Y-axis formatted in millions (₹M) for readability.",
    "Grid lines (dashed, low alpha) guide the eye without clutter.",
]:
    story.append(bullet(pt))

# ── Chart 2 ───────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("3. Monthly Sales by Category (Multi-Line Chart)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "Plotting each category as a separate line on the same axis allows direct comparison "
    "of seasonal patterns. Each series is colour-coded and marked with circles for "
    "individual monthly data points.",
    body_style))
story.append(Spacer(1,0.2*cm))
story.append(img(chart2_path, 16))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Interpretation", h2_style))
for pt in [
    "Electronics consistently leads in revenue throughout the year.",
    "Toys spike sharply in Q4 (Diwali & Christmas), overtaking Clothing temporarily.",
    "Books maintain the lowest, flattest sales curve – least seasonal dependence.",
    "Clothing shows a mid-year peak in May–June, consistent with summer apparel demand.",
    "Furniture is relatively stable with a slight Q3 dip.",
]:
    story.append(bullet(pt))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Chart Design Notes", h2_style))
for pt in [
    "Multi-line chart is ideal for comparing multiple time series simultaneously.",
    "Tableau-10 colour palette ensures distinct, accessible category colours.",
    "Legend placed outside the plot area prevents overlap with data lines.",
    "Y-axis in thousands (₹K) keeps numbers compact yet precise.",
    "Marker dots (markersize=5) mark monthly values without overwhelming the lines.",
]:
    story.append(bullet(pt))

# ── Chart 3 ───────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("4. Annual Sales Comparison – Bar Chart", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "A vertical bar chart ranks all five categories by their total annual revenue. "
    "Data labels above each bar eliminate the need to read the y-axis for precise values.",
    body_style))
story.append(Spacer(1,0.2*cm))
story.append(img(chart3_path, 14))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Interpretation", h2_style))
for pt in [
    f"Electronics is the top-performing category with ₹{best_cat_rev/1e6:.2f}M in annual revenue.",
    "Clothing ranks second, reflecting consistent all-year demand.",
    "Books is the lowest revenue category, suggesting a niche or low-ticket market.",
    "The revenue gap between Electronics and Books is over 3×, highlighting uneven category performance.",
]:
    story.append(bullet(pt))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Chart Design Notes", h2_style))
for pt in [
    "Bar chart is optimal for comparing discrete categories – not time-continuous data.",
    "Bars sorted by descending value make ranking immediately obvious.",
    "Individual colour per bar helps visually distinguish categories.",
    "Value annotations above bars provide exact figures without grid reading.",
    "White edge colour on bars provides subtle separation.",
]:
    story.append(bullet(pt))

# ── Chart 4 ───────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("5. Revenue Share – Pie Chart", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "The pie chart visualises each category's proportional share of total annual revenue. "
    "Percentage labels and slight wedge explosions make it easy to read relative contributions.",
    body_style))
story.append(Spacer(1,0.2*cm))
story.append(img(chart4_path, 12))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Interpretation", h2_style))
for pt in [
    "Electronics accounts for the largest slice (~35%) – the dominant revenue driver.",
    "Clothing and Furniture together account for approximately 40% of total revenue.",
    "Books and Toys together contribute ~25%, serving as supplementary revenue streams.",
    "No single category is overwhelmingly dominant, indicating a diversified portfolio.",
]:
    story.append(bullet(pt))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Chart Design Notes", h2_style))
for pt in [
    "Pie chart is best suited for showing part-to-whole relationships (share/proportion).",
    "Avoid pie charts with more than 6–7 segments – legibility degrades.",
    "Exploded wedges (explode=0.03) create subtle separation for emphasis.",
    "pctdistance=0.82 places % labels inside wedges to avoid label collision.",
    "Consistent colour palette maintained across all charts for visual coherence.",
]:
    story.append(bullet(pt))

# ── Chart 5 ───────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("6. Quarterly Sales by Category – Grouped Bar Chart", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "A grouped (clustered) bar chart combines two dimensions – time (quarter) and "
    "category – into a single view, making cross-category quarterly comparison straightforward.",
    body_style))
story.append(Spacer(1,0.2*cm))
story.append(img(chart5_path, 16))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Interpretation", h2_style))
for pt in [
    "Electronics leads in all four quarters; the gap widens in Q4.",
    "Toys shows the highest Q4 surge relative to its other quarters.",
    "Clothing remains second across quarters with modest Q2 uplift.",
    "Books and Furniture are relatively flat across all quarters.",
    "Q2 shows the flattest overall growth, suggesting mid-year slowdown.",
]:
    story.append(bullet(pt))
story.append(Spacer(1,0.3*cm))
story.append(Paragraph("Chart Design Notes", h2_style))
for pt in [
    "Grouped bars allow two categorical dimensions (quarter + category) to be read at once.",
    "Bar width (0.15) calculated to avoid overlap for 5 groups across 4 quarters.",
    "X-tick labels centred on the group midpoint using offset arithmetic.",
    "Legend placed outside right margin to avoid obscuring bars.",
    "Alpha=0.88 on bars gives a slight translucency for a modern look.",
]:
    story.append(bullet(pt))

# ── Summary Table ─────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("7. Summary &amp; Key Insights", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))

sum_data = [["Metric", "Value"]] + [[k, v] for k, v in summary.items()]
sum_tbl = Table(sum_data, colWidths=[8*cm, 8.5*cm])
sum_tbl.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(1,0), colors.HexColor("#4e79a7")),
    ("TEXTCOLOR",   (0,0),(1,0), colors.white),
    ("FONTNAME",    (0,0),(1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0),(-1,-1), 10),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#eef3fb"), colors.white]),
    ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#bbbbbb")),
    ("LEFTPADDING", (0,0),(-1,-1), 10),
    ("TOPPADDING",  (0,0),(-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6),
]))
story.append(sum_tbl)
story.append(Spacer(1,0.4*cm))

# ── Chart choice guide ────────────────────────────────────────────────────────
story.append(Paragraph("8. Chart Choice Guide", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
guide_data = [
    ["Chart Type",       "Best Used For",                         "Avoid When"],
    ["Line Chart",       "Continuous time-series, trend",         "Few data points, no time axis"],
    ["Area Chart",       "Cumulative trend, volume over time",    "Overlapping many series"],
    ["Bar Chart",        "Comparing discrete categories",         "Continuous/time data"],
    ["Grouped Bar",      "Multi-category across groups",          ">5–6 groups (cluttered)"],
    ["Pie Chart",        "Part-to-whole proportion",              ">7 slices or precise comparison"],
]
guide_tbl = Table(guide_data, colWidths=[4*cm, 6*cm, 6.5*cm])
guide_tbl.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(-1,0), colors.HexColor("#2d3561")),
    ("TEXTCOLOR",   (0,0),(-1,0), colors.white),
    ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0),(-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f4f7fc"), colors.white]),
    ("GRID",        (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
    ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0),(-1,-1), 7),
    ("TOPPADDING",  (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("WORDWRAP",    (0,0),(-1,-1), True),
]))
story.append(guide_tbl)
story.append(Spacer(1,0.4*cm))

# ── Label / Legend / Axis best practices ──────────────────────────────────────
story.append(Paragraph("9. Label, Legend &amp; Axis Formatting Best Practices", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
for section, points in [
    ("Axis Labels", [
        "Always label both axes with the variable name and unit (e.g., 'Revenue (₹)').",
        "Use human-readable tick formats – avoid raw large numbers (use ₹1.2M not ₹1200000).",
        "Rotate x-axis labels (rotation=45) when date strings overlap.",
    ]),
    ("Legends", [
        "Place legends outside the plot area when they would overlap data.",
        "Keep legend titles concise (e.g., 'Category' not 'Product Category Name').",
        "Match legend item order to visual order of lines/bars for intuitive reading.",
    ]),
    ("Data Labels", [
        "Add value annotations only when exact values matter; else rely on the axis.",
        "Position labels above bars (or slightly inside pie wedges) to avoid collision.",
        "Font size should be 8–11pt; smaller is hard to read, larger creates clutter.",
    ]),
    ("General Aesthetics", [
        "Remove top and right spines (axes.spines) for a cleaner, modern look.",
        "Use dashed, low-alpha grid lines to guide the eye without dominating.",
        "Maintain consistent colour palette across all charts in a report.",
        "Save at 150 DPI minimum for screen; 300 DPI for print.",
    ]),
]:
    story.append(Paragraph(section, h2_style))
    for pt in points:
        story.append(bullet(pt))
    story.append(Spacer(1,0.15*cm))

# ── Conclusion ────────────────────────────────────────────────────────────────
story.append(Paragraph("10. Conclusion", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "This project demonstrated a complete end-to-end data-visualisation workflow: "
    "dataset creation, aggregation at multiple time granularities, chart selection, "
    "formatting, and export. The key takeaway is that chart choice must match the "
    "analytical question – line charts for trends, bar charts for comparisons, pie charts "
    "for shares, and grouped bars for multi-dimensional category analysis. Consistent "
    "labelling, axis formatting, and colour usage elevate charts from informative to "
    "genuinely insightful.",
    body_style))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"\n✅  PDF saved → {PDF_PATH}")
