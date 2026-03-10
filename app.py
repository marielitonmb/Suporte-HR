import streamlit as st
from streamlit_echarts import st_echarts

from data.loader import load_data
from components.filters import render_sidebar_filters
from components.kpi_cards import render_kpi_cards
from utils.charts import (
    build_agents_chart,
    build_requests_by_user_chart,
    build_top_topics_chart,
    build_max_resolved_daily_chart,
    build_avg_resolution_time_chart,
    build_calls_per_month_chart,
    build_evolution_line_chart,
    get_wordcloud_data,
    build_treemap_chart
)

def main():
    st.set_page_config(page_title="Dashboard - Suporte HR", layout="wide")
    st.markdown("<h1 style='text-align: center'>📊 Dashboard - Suporte HR</h1>", unsafe_allow_html=True)

    # 1. Carregar dados
    df = load_data()
    if df.empty:
        st.stop()
        
    # 2. Sidebar de filtros
    filtered_df = render_sidebar_filters(df)
    
    # 3. Métricas
    render_kpi_cards(filtered_df)
    st.divider()

    # 4. Primeira Linha de Gráficos (Insights)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Top Agentes")
        fig1 = build_agents_chart(filtered_df)
        if fig1: st.plotly_chart(fig1, use_container_width=True)
        else: st.info("Dados insuficientes.")
            
    with c2:
        st.subheader("Principais Remetentes")
        fig2 = build_requests_by_user_chart(filtered_df)
        if fig2: st.plotly_chart(fig2, use_container_width=True)
        else: st.info("Dados insuficientes.")
            
    with c3:
        st.subheader("Top Tópicos de Ajuda")
        fig3 = build_top_topics_chart(filtered_df)
        if fig3: st.plotly_chart(fig3, use_container_width=True)
        else: st.info("Dados insuficientes.")

    st.divider()

    # 5. Segunda Linha: Análise de Agentes
    c4, c5 = st.columns(2)
    with c4:
        st.subheader("Maior Quantidade de Chamados Resolvidos por Agente Num Único Dia")
        fig_max_daily = build_max_resolved_daily_chart(filtered_df)
        if fig_max_daily:
            st.plotly_chart(fig_max_daily, use_container_width=True)
        else:
            st.info("Colunas insuficientes para este gráfico.")
            
    with c5:
        st.subheader("Tempo Médio de Resolução de Chamados")
        fig_avg = build_avg_resolution_time_chart(filtered_df)
        if fig_avg:
            st.plotly_chart(fig_avg, use_container_width=True)
        else:
            st.info("Colunas insuficientes para este gráfico.")
            
    st.divider()

    # 6. Quantidade de Chamados por Mês
    st.subheader("Quantidade de Chamados por mês")
    fig_months = build_calls_per_month_chart(filtered_df)
    if fig_months:
        st.plotly_chart(fig_months, use_container_width=True)
    else:
        st.info("Dados insuficientes.")
        
    st.divider()

    # 7. Evolução Line Chart
    st.subheader("📈 Total de Chamados Encerrados por Agente")
    fig_line = build_evolution_line_chart(filtered_df)
    if fig_line:
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Dados insuficientes para gerar o gráfico de linha.")
    st.divider()

    # 8. Bar Chart Race (Vídeo)
    st.subheader("📈 Evolução de Chamados Resolvidos por Agente")
    st.write("Dê Play no vídeo abaixo para visualizar a evolução ao longo do tempo (Bar Chart Race).")
    try:
        st.video("assets/chamados_bar_race.mp4")
    except Exception as e:
        st.info("Vídeo de evolução não encontrado na pasta assets.")
    st.divider()

    # 9. Análise de Termos (Assunto)
    st.subheader("🔍 Análise de Termos (Assunto)")
    cwc1, cwc2 = st.columns(2)
    
    with cwc1:
        st.write("☁️ **Nuvem de Palavras**")
        wc_data = get_wordcloud_data(filtered_df)
        if wc_data:
            option = {
                "backgroundColor": "#f8f9fa",
                "tooltip": {"show": True},
                "series": [{
                    "type": "wordCloud",
                    "shape": "circle",
                    "keepAspect": False,
                    "left": "center",
                    "top": "center",
                    "width": "100%",
                    "height": "100%",
                    "sizeRange": [15, 70],
                    "rotationRange": [-90, 90],
                    "rotationStep": 45,
                    "gridSize": 8,
                    "layoutAnimation": True,
                    "textStyle": {
                        "fontFamily": "sans-serif",
                        "fontWeight": "bold",
                        "color": "random-dark"
                    },
                    "emphasis": {
                        "focus": "self",
                        "textStyle": {
                            "textShadowBlur": 10,
                            "textShadowColor": "#333"
                        }
                    },
                    "data": wc_data
                }]
            }
            st_echarts(options=option, height="450px")
        else:
            st.info("Nenhum texto encontrado para gerar a wordcloud.")

    with cwc2:
        st.write("📊 **Proporção de Termos (Treemap)**")
        fig_treemap = build_treemap_chart(filtered_df)
        if fig_treemap:
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("Dados insuficientes para gerar o Treemap.")

if __name__ == "__main__":
    main()
