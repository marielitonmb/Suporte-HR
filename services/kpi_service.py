import pandas as pd

def calculate_total_tickets(df: pd.DataFrame) -> int:
    """Calcula o total de tickets no período filtrado."""
    return len(df)

def calculate_resolved_tickets(df: pd.DataFrame) -> int:
    """Calcula a quantidade de tickets resolvidos (Status = Resolvido ou Fechado)."""
    if 'Status Atual' not in df.columns:
        return 0
    return len(df[df['Status Atual'].isin(['Resolvido', 'Fechado'])])

def calculate_active_agents(df: pd.DataFrame) -> int:
    """Calcula a quantidade de agentes distintos que atuaram nos chamados."""
    if 'Agente Atribuído' not in df.columns:
        return 0
    return df['Agente Atribuído'].nunique()

def calculate_help_topics(df: pd.DataFrame) -> int:
    """Calcula a quantidade de tópicos de ajuda distintos."""
    if 'Tópico de ajuda' not in df.columns:
        return 0
    return df['Tópico de ajuda'].nunique()
