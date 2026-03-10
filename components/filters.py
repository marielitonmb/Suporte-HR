import streamlit as st
import pandas as pd

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza os filtros na sidebar e retorna o DataFrame filtrado.
    """
    st.sidebar.header("Filtros")

    # Year/Month filter
    if 'AnoMes' in df.columns:
        month_options = ["Todos"] + list(sorted(df['AnoMes'].dropna().unique()))
        selected_month = st.sidebar.selectbox("Mês/Ano", month_options, index=0)
    else:
        selected_month = "Todos"

    # Agent Filter
    if 'Agente Atribuído' in df.columns:
        agent_options = ["Todos"] + list(sorted(df['Agente Atribuído'].dropna().unique()))
        selected_agent = st.sidebar.selectbox("Agente", agent_options, index=0)
    else:
        selected_agent = "Todos"

    # Apply filters
    filtered_df = df.copy()
    if selected_month != "Todos":
        filtered_df = filtered_df[filtered_df['AnoMes'] == selected_month]
    if selected_agent != "Todos":
        filtered_df = filtered_df[filtered_df['Agente Atribuído'] == selected_agent]

    return filtered_df
