import pandas as pd
import plotly.express as px
import collections
from wordcloud import STOPWORDS

def build_agents_chart(df: pd.DataFrame):
    """
    Constrói gráfico de barras com chamados por agente.
    """
    if 'Agente Atribuído' not in df.columns:
        return None
    ag_counts = df['Agente Atribuído'].value_counts().head(10).reset_index()
    ag_counts.columns = ['Agente', 'Quantidade']
    fig = px.bar(ag_counts, x='Quantidade', y='Agente', orientation='h', 
                    title="Chamados por Agente Atribuído", text='Quantidade')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(visible=False, showticklabels=False)
    return fig

def build_requests_by_user_chart(df: pd.DataFrame):
    """
    Constrói gráfico de requisições por usuário.
    """
    if 'De' not in df.columns:
        return None
    remet_counts = df['De'].value_counts().head(10).reset_index()
    remet_counts.columns = ['Remetente', 'Quantidade']
    fig = px.bar(remet_counts, x='Quantidade', y='Remetente', orientation='h', 
                    title="Requisições por Usuário", text='Quantidade')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(visible=False, showticklabels=False)
    return fig

def build_top_topics_chart(df: pd.DataFrame):
    """
    Constrói gráfico dos tópicos de ajuda mais frequentes.
    """
    if 'Tópico de ajuda' not in df.columns:
        return None
    top_counts = df['Tópico de ajuda'].value_counts().head(10).reset_index()
    top_counts.columns = ['Tópico', 'Quantidade']
    fig = px.bar(top_counts, x='Quantidade', y='Tópico', orientation='h', 
                    title="Tópicos mais frequentes", text='Quantidade')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(visible=False, showticklabels=False)
    return fig

def build_max_resolved_daily_chart(df: pd.DataFrame):
    """
    Constrói gráfico do maior número de chamados resolvidos por agente em um único dia.
    """
    if 'Data de conclusão' not in df.columns or 'Status Atual' not in df.columns:
        return None
        
    res_df = df[df['Status Atual'].isin(['Resolvido', 'Fechado'])].copy()
    if res_df.empty:
        return None
        
    res_df['DiaConclusao'] = res_df['Data de conclusão'].dt.date
    daily_counts = res_df.groupby(['Agente Atribuído', 'DiaConclusao']).size().reset_index(name='Chamados Resolvidos')
    
    # Encontrar a linha do valor máximo para cada agente (incluindo a data)
    idx = daily_counts.groupby(['Agente Atribuído'])['Chamados Resolvidos'].transform(max) == daily_counts['Chamados Resolvidos']
    max_daily = daily_counts[idx].drop_duplicates(['Agente Atribuído']) # Em caso de empate, pega a primeira data
    max_daily = max_daily.sort_values('Chamados Resolvidos', ascending=False)
    
    # Formatar a data para exibição
    max_daily['Data_Formatada'] = max_daily['DiaConclusao'].apply(lambda x: x.strftime('%d/%m/%Y'))
    
    fig = px.bar(max_daily, x='Agente Atribuído', y='Chamados Resolvidos',
                            text='Chamados Resolvidos', 
                            color='Agente Atribuído',
                            custom_data=['Data_Formatada'])
    
    fig.update_layout(showlegend=False, xaxis_title="Agente Atribuído", yaxis_title="Chamados Resolvidos")
    fig.update_traces(
        textposition='outside',
        hovertemplate="<b>Agente:</b> %{x}<br><b>Recorde:</b> %{y} chamados<br><b>Data:</b> %{customdata[0]}<extra></extra>"
    )
    return fig

def build_avg_resolution_time_chart(df: pd.DataFrame):
    """
    Constrói gráfico do tempo médio de resolução de chamados em horas.
    """
    if 'Data de conclusão' not in df.columns or 'Data de Criação' not in df.columns or 'Status Atual' not in df.columns:
        return None
        
    res_df = df[df['Status Atual'].isin(['Resolvido', 'Fechado'])].copy()
    if res_df.empty:
        return None
        
    res_df['Horas_Resolucao'] = (res_df['Data de conclusão'] - res_df['Data de Criação']).dt.total_seconds() / 3600
    
    avg_time = res_df.groupby('Agente Atribuído')['Horas_Resolucao'].mean().round(2).reset_index()
    avg_time.columns = ['Agente Atribuído', 'Média de Horas']
    avg_time = avg_time.sort_values('Média de Horas', ascending=True)
    
    fig = px.bar(avg_time, x='Média de Horas', y='Agente Atribuído', orientation='h', 
                            text='Média de Horas', color='Média de Horas', color_continuous_scale='viridis')
    fig.update_layout(showlegend=False, xaxis_title="Horas", yaxis_title="Agente Atribuído")
    fig.update_traces(textposition='outside', textfont_size=11)
    return fig

def build_calls_per_month_chart(df: pd.DataFrame):
    """
    Constrói o gráfico de quantidade de chamados por mês.
    """
    if 'Data de Criação' not in df.columns:
        return None
        
    meses_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    month_dist_df = df.copy()
    month_dist_df['Mes_Num'] = month_dist_df['Data de Criação'].dt.month
    month_counts = month_dist_df.groupby('Mes_Num').size().reset_index(name='Número de Chamados')
    month_counts['Mês'] = month_counts['Mes_Num'].map(meses_map)
    month_counts = month_counts.sort_values('Mes_Num')
    
    fig = px.bar(month_counts, x='Mês', y='Número de Chamados')
    fig.update_layout(xaxis_title="Mês", yaxis_title="Número de Chamados")
    return fig

def build_evolution_line_chart(df: pd.DataFrame):
    """
    Constrói gráfico de linha para evolução temporal.
    """
    if 'Status Atual' not in df.columns or 'AnoMes' not in df.columns:
        return None
        
    line_res_df = df[df['Status Atual'].isin(['Resolvido', 'Fechado'])]
    if line_res_df.empty:
        return None
        
    line_counts = line_res_df.groupby(['AnoMes', 'Agente Atribuído']).size().reset_index(name='Total Encerrados')
    fig = px.line(line_counts, 
                    x='AnoMes', 
                    y='Total Encerrados', 
                    color='Agente Atribuído',
                    markers=True,
                    text='Total Encerrados',
                    title="Evolução de Chamados Encerrados ao Longo do Tempo")
    
    fig.update_traces(textposition="top center")
    fig.update_layout(xaxis_title="Período", yaxis_title="Total de Chamados Encerrados")
    return fig



def get_wordcloud_data(df: pd.DataFrame):
    """
    Retorna os dados formatados para a Wordcloud ECharts.
    """
    if 'Assunto' not in df.columns:
        return None
        
    assunto_text = " ".join(str(v) for v in df['Assunto'].dropna())
    if not assunto_text:
        return None
        
    stopwords = set(STOPWORDS)
    stopwords.update([
        "da", "meu", "em", "você", "de", "ao", "os", "e", "para", "com", "no", "na", "o", "a", "do",
        "dos", "das", "um", "uma", "me", "se", "por", "mais", "suporte", "hr", "chamado"
    ])
    
    # Limpeza e Normalização
    words = assunto_text.replace("-", " ").split()
    words = [w.lower() for w in words if len(w) > 2]
    words = [w for w in words if w not in stopwords]
    
    word_counts = collections.Counter(words)
    
    # Retornar top 100 para evitar sobrecarga, mas manter diversidade
    data = [{"name": k.upper(), "value": v} for k, v in word_counts.most_common(100)]
    return data

def build_treemap_chart(df: pd.DataFrame):
    """
    Constrói um gráfico Treemap com a proporção dos termos mais usados no 'Assunto'.
    """
    wc_data = get_wordcloud_data(df)
    if not wc_data:
        return None
        
    df_words = pd.DataFrame(wc_data)
    # Filtrar top 40 para não poluir muito o treemap
    df_words = df_words.sort_values(by="value", ascending=False).head(40)
    
    # Calcular porcentagens
    total_filtered_val
    
    
    
    ue = df_words['value'].sum()
    df_words['percentage'] = (df_words['value'] / total_filtered_value * 100).round(1)
    # Criar coluna formatada para o label
    df_words['label_text'] = df_words['name'] + "<br>" + df_words['value'].astype(str) + " (" + df_words['percentage'].astype(str) + "%)"
    
    fig = px.treemap(df_words, 
                     path=['name'], 
                     values='value',
                     color='value', 
                     color_continuous_scale='viridis',
                     custom_data=['percentage'])
    
    # Melhorando os rótulos e o hover
    fig.update_traces(
        text=df_words['label_text'],
        textinfo="text",
        hovertemplate="<b>Termo:</b> %{label}<br><b>Quantidade:</b> %{value}<br><b>Frequência:</b> %{customdata[0]}%<extra></extra>",
        textfont=dict(size=14)
    )
    
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        coloraxis_showscale=False
    )
    return fig
