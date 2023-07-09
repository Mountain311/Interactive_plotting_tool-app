import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf


st.set_page_config(
    page_title="INTERACTIVE DATAPLOT DASHBOARD",
    layout="wide"
)

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel File", 
    ['csv', 'xlsx','xls']
)

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)  
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        # Show sheet selection
        sheet_name = st.selectbox('Select Sheet', pd.ExcelFile(uploaded_file).sheet_names)
        # Read specific sheet
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)


    with st.sidebar:
        plot_type = st.radio("Plot Type", ("Scatter", "Bar",
                            "Pie", "Correlation","Line"))

    # Define shared inputs
    selected_x = st.selectbox('X axis', df.columns)
    selected_y = st.selectbox('Y axis', df.columns)

    if plot_type == "Scatter":
        selected_hue = st.selectbox('Hue', df.columns)
        fig = px.scatter(df, x=selected_x, y=selected_y, color=selected_hue)

    if plot_type == "Bar":
        fig = px.bar(df, x=selected_x, y=df.index)

    if plot_type == "Pie":
        fig = px.pie(df, values=selected_x, names=df.index)

    if plot_type == "Correlation":
        corr = df.corr()
        fig = go.Figure(data=go.Heatmap(z=corr.values))
        
    if plot_type == "Line":
       
        selected_hue = st.selectbox("Group", df.columns)
        fig = px.line(df, x=selected_x, y=selected_y, color=selected_hue)


    fig.update_layout(
        width=1500,
        height=1000,
        margin=dict(l=100, r=10, t=40, b=10)  # left margin = 50, right = 10
    )

    st.plotly_chart(fig)
