import pandas as pd
import streamlit as st

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Carrega os dados dos chamados e realiza as transformações iniciais.
    
    Returns:
        pd.DataFrame: DataFrame contendo os chamados processados.
    """
    try:
        df = pd.read_csv('Closed Tickets - 20260102.csv', sep=';')
        
        # Process dates
        if 'Data de Criação' in df.columns:
            df['Data de Criação'] = pd.to_datetime(df['Data de Criação'], errors='coerce')
            df['AnoMes'] = df['Data de Criação'].dt.to_period('M').astype(str)
        
        # Keep only important columns
        cols = ['Número do Ticket', 'Data de Criação', 'AnoMes', 'Assunto', 'De', 
               'Departamento', 'Tópico de ajuda', 'Status Atual', 'Agente Atribuído', 'Data de conclusão']
        df = df[[c for c in cols if c in df.columns]]
        
        # Process "Data de conclusão" for new charts
        if 'Data de conclusão' in df.columns:
            df['Data de conclusão'] = pd.to_datetime(df['Data de conclusão'], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()
