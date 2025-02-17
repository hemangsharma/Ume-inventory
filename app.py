import streamlit as st
import pandas as pd
import plotly.express as px

# 🖥️ Set Modern Page Config
st.set_page_config(page_title="🏠 Property Inventory", layout="wide")

# 🎨 Inject Custom CSS
st.markdown(
    """
    <style>
        body {
            background-color: #F5F5F5;
            color: #333333;
        }
        .stTextInput, .stSelectbox {
            border-radius: 8px !important;
            border: 1px solid #4CAF50 !important;
        }
        .stDataFrame {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
        }
        .metric-container {
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
            border-radius: 10px;
            color: white;
        }
        .key-card {
            background: linear-gradient(135deg, #FFC107, #FFD54F);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 20px;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏢 Property Dashboard Title
st.title('🏢 Ume Potts Point Property Inventory')

# 📂 Load Inventory Data
csv_file = 'sheet.csv'
try:
    df = pd.read_csv(csv_file)
    if not all(col in df.columns for col in ['Assest Name', 'Description', 'Qunatity', 'Floor']):
        st.error("CSV must contain columns: 'Assest Name', 'Description', 'Qunatity', and 'Floor'")
        st.stop()
    st.success(f"✅ Data loaded from {csv_file}!")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# 🔑 Load Key Data
key_file = 'key.csv'
try:
    key_df = pd.read_csv(key_file)
    if not all(col in key_df.columns for col in ['Room No', 'Room Key Quantity', 'Kitchen Cabinet Quantity']):
        st.error("Key CSV must contain 'Room No', 'Room Key Quantity', and 'Kitchen Cabinet Quantity'")
        st.stop()
    st.success(f"🔑 Key data loaded from {key_file}!")
except Exception as e:
    st.error(f"❌ Failed to load key data: {e}")
    st.stop()

# 🔐 **Key Locker UI**
st.subheader("🔐 Key Locker")
with st.container():
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_room = st.selectbox("🏠 Select a Room", options=key_df['Room No'].astype(str).unique())

    with col2:
        room_keys = key_df[key_df['Room No'].astype(str) == selected_room]

        if not room_keys.empty:
            room_key_qty = room_keys.iloc[0]['Room Key Quantity']
            kitchen_key_qty = room_keys.iloc[0]['Kitchen Cabinet Quantity']

            st.markdown(
                f"""
                <div class="key-card">
                    🔑 Room Keys: {room_key_qty} | 🚪 Kitchen Cabinet Keys: {kitchen_key_qty}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("No key data available for this room.")

# 🔍 **Inventory Search**
st.subheader("🔍 Search Inventory")
search_term = st.text_input("Enter asset name:")
filtered_df = df[df['Assest Name'].str.contains(search_term, case=False, na=False)] if search_term else df
st.dataframe(filtered_df, height=300)

# 📊 **Floor Selection & Inventory Table**
floor = st.selectbox('📊 Select Floor:', options=df['Floor'].dropna().unique())
st.subheader(f'🏢 Inventory for {floor}')
st.dataframe(df[df['Floor'] == floor])

# 📈 **Graphs & Visualizations**
col1, col2 = st.columns(2)
with col1:
    st.subheader('📈 Distribution by Floor')
    floor_dist = px.histogram(df, x='Floor', color_discrete_sequence=['#4CAF50'])
    st.plotly_chart(floor_dist, use_container_width=True)

with col2:
    st.subheader('📊 Asset Quantity')
    asset_dist = px.bar(df, x='Assest Name', y='Qunatity', color_discrete_sequence=['#FFC107'])
    st.plotly_chart(asset_dist, use_container_width=True)

# 🔢 **Summary Metrics**
st.subheader('📊 Inventory Summary')
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="metric-container"><h3>🛠️ Total Assets</h3><h1>{}</h1></div>'.format(df['Assest Name'].nunique()), unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container"><h3>📦 Total Quantity</h3><h1>{}</h1></div>'.format(df['Qunatity'].sum()), unsafe_allow_html=True)

# 🏆 **Top 5 Assets**
st.subheader('🏆 Top 5 Assets')
top_assets = df.sort_values(by='Qunatity', ascending=False).head(5)
st.dataframe(top_assets)