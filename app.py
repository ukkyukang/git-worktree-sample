import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="📊 Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

# ──────────────────────────────────────────────
# Sample Data
# ──────────────────────────────────────────────
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=90, freq="D")
sales_data = pd.DataFrame({
    "Date": dates,
    "Revenue": np.cumsum(np.random.randn(90) * 500 + 2000),
    "Orders": np.random.randint(50, 200, 90),
    "Customers": np.random.randint(30, 150, 90),
})

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
st.sidebar.title("🔧 Filters")
date_range = st.sidebar.date_input(
    "Date Range",
    value=(dates[0], dates[-1]),
    min_value=dates[0],
    max_value=dates[-1],
)

# Filter data
if isinstance(date_range, tuple) and len(date_range) == 2:
    mask = (sales_data["Date"].dt.date >= date_range[0]) & (
        sales_data["Date"].dt.date <= date_range[1]
    )
    filtered = sales_data[mask]
else:
    filtered = sales_data

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.title("📊 Sales Dashboard")
st.markdown("A simple sales overview dashboard — **main branch** (baseline)")

# ──────────────────────────────────────────────
# KPI Cards
# ──────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

col1.metric(
    label="💰 Total Revenue",
    value=f"${filtered['Revenue'].iloc[-1]:,.0f}",
    delta=f"{filtered['Revenue'].diff().iloc[-1]:+,.0f}",
)
col2.metric(
    label="📦 Total Orders",
    value=f"{filtered['Orders'].sum():,}",
    delta=f"{filtered['Orders'].iloc[-1] - filtered['Orders'].iloc[-2]:+d}",
)
col3.metric(
    label="👥 Avg Customers/Day",
    value=f"{filtered['Customers'].mean():.0f}",
    delta=f"{filtered['Customers'].iloc[-1] - filtered['Customers'].mean():+.0f}",
)

# ──────────────────────────────────────────────
# Chart
# ──────────────────────────────────────────────
st.subheader("📈 Revenue Over Time")
st.line_chart(filtered.set_index("Date")["Revenue"])

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · main branch · v1.0")
