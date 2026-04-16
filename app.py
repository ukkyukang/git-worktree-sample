import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🌙 Sales Dashboard — Dark Theme",
    page_icon="🌙",
    layout="wide",
)

# ──────────────────────────────────────────────
# Dark Theme CSS
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

    /* ── Chart container ── */
    [data-testid="stVegaLiteChart"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(130, 100, 255, 0.2);
    }

    /* ── Toggle button ── */
    .stRadio > label {
        color: #c4b5fd !important;
    }
</style>
""", unsafe_allow_html=True)

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
st.sidebar.title("🌙 Dark Dashboard")
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
st.title("🌙 Sales Dashboard")
st.markdown(
    f'<p style="color:{accent}; font-size:1.1rem;">Dark Theme Edition — '
    f'<code style="color:{accent};">feature/dark-theme</code> branch</p>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# KPI Cards with Neon Glow
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
# Glow Status Bar
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
st.caption("Built with Streamlit · feature/dark-theme branch · v1.1-dark")
