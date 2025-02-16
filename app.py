import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Enhanced Property Inventory Dashboard
st.title('🏢 Ume Potts Point Property Inventory Dashboard')

# Load CSV Automatically
csv_file = 'sheet.csv'
try:
    df = pd.read_csv(csv_file)
    if not all(col in df.columns for col in ['Assest Name', 'Description', 'Qunatity', 'Floor']):
        st.error("CSV must contain columns: 'Assest Name', 'Description', 'Qunatity', and 'Floor'")
        st.stop()
    st.success(f"✅ Data loaded successfully from {csv_file}!")
except Exception as e:
    st.error(f"❌ Failed to load data from {csv_file}: {e}")
    st.stop()

# Full Inventory Overview with Search
search_term = st.text_input("🔍 Search Inventory (by Asset Name):")
filtered_df = df[df['Assest Name'].str.contains(search_term, case=False, na=False)] if search_term else df
st.subheader('📜 Complete Inventory Overview')
st.dataframe(filtered_df)

# Floor Filter
floor = st.selectbox('📊 Select Floor:', options=df['Floor'].dropna().unique())
st.subheader(f'🏢 Inventory for {floor}')
st.dataframe(df[df['Floor'] == floor])

# Visualizations
col1, col2 = st.columns(2)
with col1:
    st.subheader('📈 Inventory Distribution by Floor')
    floor_dist = px.histogram(df, x='Floor', color='Floor', title='Item Count by Floor')
    st.plotly_chart(floor_dist)

with col2:
    st.subheader('📊 Quantity Distribution by Asset')
    asset_dist = px.bar(df, x='Assest Name', y='Qunatity', title='Quantity per Asset', color='Floor')
    asset_dist.update_layout(xaxis_title='Asset Name', yaxis_title='Quantity')
    st.plotly_chart(asset_dist)

# Summary Metrics
st.subheader('📊 Inventory Summary')
col3, col4 = st.columns(2)
with col3:
    st.metric(label="Total Unique Assets", value=df['Assest Name'].nunique())
with col4:
    st.metric(label="Total Inventory Quantity", value=df['Qunatity'].sum())

# Top 5 Assets by Quantity
st.subheader('🏆 Top 5 Assets by Quantity')
top_assets = df.sort_values(by='Qunatity', ascending=False).head(5)
st.dataframe(top_assets)