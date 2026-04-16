import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🚀 Sales Dashboard — Ultimate",
    page_icon="🚀",
    layout="wide",
)

# ──────────────────────────────────────────────
# Dark Theme CSS (from feature/dark-theme)
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global Dark Theme ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(130, 100, 255, 0.3);
    }

    /* ── Metric Cards with Neon Glow ── */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(130, 100, 255, 0.4);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(130, 100, 255, 0.15),
                    0 0 40px rgba(130, 100, 255, 0.05);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 0 30px rgba(130, 100, 255, 0.3),
                    0 0 60px rgba(130, 100, 255, 0.1);
        transform: translateY(-2px);
    }

    /* ── Metric Label ── */
    [data-testid="stMetricLabel"] {
        color: #a78bfa !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #a78bfa !important;
        font-weight: 600;
    }

    /* ── Metric Value ── */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
    }

    /* ── Headings ── */
    h1 {
        background: linear-gradient(90deg, #a78bfa, #6dd5ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    h2, h3 {
        color: #c4b5fd !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(130, 100, 255, 0.3) !important;
    }

    /* ── Caption ── */
    .stCaption p {
        color: #8b5cf6 !important;
    }

    /* ── Plotly charts dark bg ── */
    [data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(130, 100, 255, 0.2);
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(130, 100, 255, 0.2);
        border-radius: 12px;
    }

    /* ── Download button ── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton button:hover {
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Sample Data (from feature/analytics — enriched)
# ──────────────────────────────────────────────
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=90, freq="D")
sales_data = pd.DataFrame({
    "Date": dates,
    "Revenue": np.cumsum(np.random.randn(90) * 500 + 2000),
    "Orders": np.random.randint(50, 200, 90),
    "Customers": np.random.randint(30, 150, 90),
    "Category": np.random.choice(["Electronics", "Clothing", "Food", "Books"], 90),
    "Region": np.random.choice(["North", "South", "East", "West"], 90),
})

# ──────────────────────────────────────────────
# Sidebar (merged: theme toggle + analytics filters)
# ──────────────────────────────────────────────
st.sidebar.title("🚀 Ultimate Dashboard")
st.sidebar.markdown("---")

theme_mode = st.sidebar.radio(
    "🎨 Theme Accent",
    ["Purple Neon", "Cyber Blue", "Emerald Glow"],
    index=0,
)
accent_colors = {
    "Purple Neon": "#a78bfa",
    "Cyber Blue": "#6dd5ed",
    "Emerald Glow": "#34d399",
}
accent = accent_colors[theme_mode]

st.sidebar.markdown("---")
date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(dates[0], dates[-1]),
    min_value=dates[0],
    max_value=dates[-1],
)

selected_categories = st.sidebar.multiselect(
    "📂 Categories",
    options=sales_data["Category"].unique(),
    default=sales_data["Category"].unique(),
)

selected_regions = st.sidebar.multiselect(
    "🌍 Regions",
    options=sales_data["Region"].unique(),
    default=sales_data["Region"].unique(),
)

# Filter data
filtered = sales_data.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    mask = (filtered["Date"].dt.date >= date_range[0]) & (
        filtered["Date"].dt.date <= date_range[1]
    )
    filtered = filtered[mask]

filtered = filtered[
    filtered["Category"].isin(selected_categories)
    & filtered["Region"].isin(selected_regions)
]

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.title("🚀 Sales Dashboard — Ultimate Edition")
st.markdown(
    f'<p style="color:{accent}; font-size:1.1rem;">'
    f'Dark Theme + Analytics — merged from '
    f'<code style="color:{accent};">feature/dark-theme</code> &amp; '
    f'<code style="color:{accent};">feature/analytics</code></p>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# KPI Cards (4 columns like analytics, with neon glow from dark-theme)
# ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="💰 Total Revenue",
    value=f"${filtered['Revenue'].iloc[-1]:,.0f}" if len(filtered) > 0 else "$0",
    delta=f"{filtered['Revenue'].diff().iloc[-1]:+,.0f}" if len(filtered) > 1 else "N/A",
)
col2.metric(
    label="📦 Total Orders",
    value=f"{filtered['Orders'].sum():,}" if len(filtered) > 0 else "0",
)
col3.metric(
    label="👥 Avg Customers/Day",
    value=f"{filtered['Customers'].mean():.0f}" if len(filtered) > 0 else "0",
)
col4.metric(
    label="📊 Records Shown",
    value=f"{len(filtered)}",
    delta=f"{len(filtered) - len(sales_data)}",
)

# ──────────────────────────────────────────────
# Interactive Plotly Charts (from analytics, with dark template)
# ──────────────────────────────────────────────
st.subheader("📈 Revenue Trend (Interactive)")

fig_revenue = px.line(
    filtered,
    x="Date",
    y="Revenue",
    title="Daily Revenue",
    template="plotly_dark",
    color_discrete_sequence=[accent],
)
fig_revenue.update_traces(
    line=dict(width=3),
    fill="tozeroy",
    fillcolor=f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},0.1)",
)
fig_revenue.update_layout(
    hovermode="x unified",
    height=400,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_revenue, use_container_width=True)

# ── Two-column charts ──
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Orders by Category")
    category_data = filtered.groupby("Category")["Orders"].sum().reset_index()
    fig_bar = px.bar(
        category_data,
        x="Category",
        y="Orders",
        color="Category",
        template="plotly_dark",
        color_discrete_sequence=["#a78bfa", "#6dd5ed", "#34d399", "#f472b6"],
    )
    fig_bar.update_layout(
        showlegend=False, height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("🗺️ Customers by Region")
    region_data = filtered.groupby("Region")["Customers"].sum().reset_index()
    fig_pie = px.pie(
        region_data,
        values="Customers",
        names="Region",
        template="plotly_dark",
        color_discrete_sequence=["#a78bfa", "#6dd5ed", "#34d399", "#f472b6"],
        hole=0.4,
    )
    fig_pie.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ──────────────────────────────────────────────
# Statistics Summary
# ──────────────────────────────────────────────
st.subheader("📋 Statistical Summary")
if len(filtered) > 0:
    stats = filtered[["Revenue", "Orders", "Customers"]].describe().round(2)
    st.dataframe(stats, use_container_width=True)
else:
    st.warning("No data matches the current filters.")

# ──────────────────────────────────────────────
# Data Table + Download
# ──────────────────────────────────────────────
st.subheader("📄 Raw Data")
st.dataframe(
    filtered.style.format({
        "Revenue": "${:,.2f}",
        "Orders": "{:,}",
        "Customers": "{:,}",
    }),
    use_container_width=True,
    height=300,
)

csv_data = filtered.to_csv(index=False)
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="sales_data_filtered.csv",
    mime="text/csv",
)

# ──────────────────────────────────────────────
# Glow Status Bar (from dark-theme)
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="
    margin-top: 2rem;
    padding: 12px 24px;
    background: rgba(255,255,255,0.03);
    border: 1px solid {accent}40;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <span style="color:{accent};">● System Online</span>
    <span style="color:#666;">Theme: {theme_mode}</span>
    <span style="color:#666;">Records: {len(filtered)}</span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.divider()
st.caption(
    "Built with Streamlit + Plotly · main branch · "
    "v2.0 (merged: dark-theme + analytics)"
)
