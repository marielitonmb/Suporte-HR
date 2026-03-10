import streamlit as st
import pandas as pd
from services.kpi_service import (
    calculate_total_tickets,
    calculate_resolved_tickets,
    calculate_active_agents,
    calculate_help_topics
)

def render_kpi_cards(df: pd.DataFrame):
    """
    Renderiza os cards de KPI na parte superior do Dashboard.
    """
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Tickets", calculate_total_tickets(df))
        col2.metric("Tickets Resolvidos", calculate_resolved_tickets(df))
        col3.metric("Agentes Ativos", calculate_active_agents(df))
        col4.metric("Tópicos de Ajuda", calculate_help_topics(df))
