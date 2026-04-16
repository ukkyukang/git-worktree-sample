import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🔬 Sales Dashboard — Analytics",
    page_icon="🔬",
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
    "Category": np.random.choice(["Electronics", "Clothing", "Food", "Books"], 90),
    "Region": np.random.choice(["North", "South", "East", "West"], 90),
})

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
st.sidebar.title("🔬 Analytics Controls")
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
st.title("🔬 Sales Dashboard — Analytics Edition")
st.markdown(
    "Advanced analytics with interactive charts — "
    "`feature/analytics` branch"
)

# ──────────────────────────────────────────────
# KPI Cards
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
# Interactive Plotly Charts
# ──────────────────────────────────────────────
st.subheader("📈 Revenue Trend (Interactive)")

fig_revenue = px.line(
    filtered,
    x="Date",
    y="Revenue",
    title="Daily Revenue",
    template="plotly_white",
    color_discrete_sequence=["#6366f1"],
)
fig_revenue.update_traces(
    line=dict(width=3),
    fill="tozeroy",
    fillcolor="rgba(99, 102, 241, 0.1)",
)
fig_revenue.update_layout(
    hovermode="x unified",
    height=400,
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
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_bar.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("🗺️ Customers by Region")
    region_data = filtered.groupby("Region")["Customers"].sum().reset_index()
    fig_pie = px.pie(
        region_data,
        values="Customers",
        names="Region",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4,
    )
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

# ──────────────────────────────────────────────
# Statistics Summary
# ──────────────────────────────────────────────
st.subheader("📋 Statistical Summary")

if len(filtered) > 0:
    stats = filtered[["Revenue", "Orders", "Customers"]].describe()
    stats = stats.round(2)
    st.dataframe(stats, use_container_width=True)
else:
    st.warning("No data matches the current filters.")

# ──────────────────────────────────────────────
# Data Table
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

# ──────────────────────────────────────────────
# Download CSV
# ──────────────────────────────────────────────
csv_data = filtered.to_csv(index=False)
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="sales_data_filtered.csv",
    mime="text/csv",
)

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit + Plotly · feature/analytics branch · v1.1-analytics")
