import streamlit as st
import pandas as pd
from analysis.analytics_service import AnalyticsService

st.set_page_config(
    page_title="E-Commerce Market Intelligence",
    page_icon="📈",
    layout="wide"
)

st.title("📈 E-Commerce Market Intelligence Dashboard")
st.markdown("Real-time competitor analytics, pricing trends, and inventory risk monitoring.")

#@st.cache_data(ttl=300)
def load_data():
    service = AnalyticsService()
    return service.run_all_analyses()

with st.spinner("Loading analytics data from pipeline..."):
    try:
        data = load_data()
        st.success("Analytics pipeline loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load analytics data: {e}")
        st.stop()

# Extract DataFrames and KPIs directly
price_df = data.get("price_changes", pd.DataFrame())
inventory_df = data.get("inventory_risk", pd.DataFrame())
competitor_df = data.get("competitor_ranking", pd.DataFrame())
discount_df = data.get("discount_opportunities", pd.DataFrame())
kpis = data.get("kpis", {})

# --- Top Key Metrics ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    val = kpis.get("total_price_records", len(price_df))
    st.metric(label="Price Changes Evaluated", value=val)

with col2:
    at_risk_count = len(inventory_df[inventory_df["days_out"] > 0]) if not inventory_df.empty and "days_out" in inventory_df.columns else len(inventory_df)
    val = kpis.get("inventory_alerts", at_risk_count)
    st.metric(label="Stockout Alerts", value=val)

with col3:
    val = kpis.get("total_competitors", len(competitor_df))
    st.metric(label="Tracked Competitors", value=val)

with col4:
    val = kpis.get("discount_opportunities", len(discount_df))
    st.metric(label="Discount Opportunities", value=val)

st.markdown("---")

# --- Tabs Layout ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Competitor Rankings", 
    "📦 Inventory Risk", 
    "📊 Price Changes", 
    "🏷️ Discount Opportunities"
])

with tab1:
    st.subheader("Competitor Price Rankings")
    if not competitor_df.empty:
        st.dataframe(competitor_df, use_container_width=True)
        # Attempt to plot chart if required columns exist
        name_col = "name" if "name" in competitor_df.columns else competitor_df.columns[0]
        price_col = "price" if "price" in competitor_df.columns else competitor_df.columns[-1]
        
        if name_col in competitor_df.columns:
            st.bar_chart(competitor_df.set_index(name_col)[price_col])
    else:
        st.info("No competitor ranking data available.")

with tab2:
    st.subheader("Inventory & Stockout Risk Analysis")
    if not inventory_df.empty:
        st.dataframe(inventory_df, use_container_width=True)
    else:
        st.info("No inventory risk data recorded.")

with tab3:
    st.subheader("Price Changes & History")
    if not price_df.empty:
        st.dataframe(price_df, use_container_width=True)
    else:
        st.info("No price change history available.")

with tab4:
    st.subheader("Discount Opportunities")
    if not discount_df.empty:
        st.dataframe(discount_df, use_container_width=True)
    else:
        st.info("No discount opportunity data available.")