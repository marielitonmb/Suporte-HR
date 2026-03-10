# 📊 Dashboard - Suporte HR

Este projeto consiste em um dashboard executivo e operacional de alta performance para a análise de chamados de suporte do departamento de Recursos Humanos (HR). Ele foi desenvolvido com foco em qualidade de dados, performance, visualizações intuitivas e de alto nível, além de um desenvolvimento escalável, utilizando tecnologias e design patterns modernos de engenharia voltada para Analytics.

## 🚀 Funcionalidades Principais

- **Visão Geral de KPIs:** Métricas de acompanhamento em tempo real (Total de Tickets, Tickets Resolvidos, Agentes Ativos e Tópicos de Ajuda).
- **Análise de Agentes e Requisições:** Gráficos que mapeiam os agentes líderes em resoluções e os principais usuários que demandam suporte.
- **Tópicos de Ajuda:** Identificação quantitativa dos tópicos e assuntos que mais geram tickets.
- **Performance e SLA de Agentes:**
  - Gráfico que identifica o recorde diário de chamados resolvidos por agente.
  - Métrica de Tempo Médio de Resolução de Chamados (em horas) por agente.
- **Evolução Temporal:**
  - Histórico do volume de chamados de entrada mensal.
  - Acompanhamento evolutivo em linha temporal para demonstrar as entregas/resoluções por atendente mês a mês.
- **Visualizações Dinâmicas de Alta Performance:** 
  - Animação de Barra (*Bar Chart Race*) demonstrando a evolução acumulada histórica de atendimentos dos agentes ao longo dos meses.
- **Nuvem de Palavras:** Wordcloud interativa (usando Apache ECharts) contendo a mineração de texto nos assuntos dos tickets.

## 🏗️ Arquitetura do Projeto

O projeto foi construído seguindo os rigorosos padrões definidos nas diretrizes do projeto, com forte separação de responsabilidades (princípios SOLID e Clean Code) aplicados a um projeto analítico:

```
project_root/
├── app.py                  # Orquestrador da Interface Streamlit (Controller)
├── components/             # Componentes de interface que isolam UI de regra de negócios
│   ├── filters.py          # Gerenciamento dinâmico da Sidebar (Filtros de data e agente)
│   └── kpi_cards.py        # Widgets de visualização de alto nível (Métricas no Head)
├── data/                   # Regras de Transformação e I/O de dados 
│   └── loader.py           # Ingestão de fonte de dados, checagem e transformação inicial (Dates)
├── services/               # Lógica de Negócios e Agregadores
│   └── kpi_service.py      # Cálculos matriciais analíticos (Soma, contagem, lógicas)
├── utils/                  # Utilitários Globais
│   └── charts.py           # Funções construtoras isoladas de gráficos (Retornam estâncias formatadas do Plotly e Echarts)
├── assets/, config/, database/, etl/, exemplos/, pages/, tests/ # Camadas preparatórias para escalar o projeto
├── requirements.txt        # Manifesto de dependências do Python
└── README.md               # Documentação inicial 
```

### Tecnologias Utilizadas
- Linguagem Base: Python 3.11+
- Aplicação Web / UI: **Streamlit** 
- Visualização de Dados: **Plotly**, **Streamlit-Echarts** (Apache Echarts)
- Manipulação e Modelagem: **Pandas** e NumPy
- Text Mining Básica: **WordCloud** 

## 💻 Como Executar o Projeto

Siga as instruções abaixo para preparar o ambiente e rodar o Dashboard na sua máquina:

**1. Clone ou acesse o repositório:**
Acesse o diretório raiz do projeto no seu terminal (Prompt de Comando, PowerShell ou VSCode Terminal).
```bash
cd "d:\Documents\Meus-Projetos\Suporte HR"
```

**2. Crie um ambiente virtual (Recomendado):**
Isolar as dependências garante que outras instâncias do Python não entrem em conflito.
```bash
# Criação do Ambiente (Windows)
python -m venv venv

# Ativação do Ambiente Virtual (Windows)
venv\Scripts\activate
```

**3. Instale os pacotes e dependências:**
Execute a instalação através do pip:
```bash
pip install -r requirements.txt
```

**4. Execute o Streamlit:**
Agora basta criar a instância do servidor da aplicação apontando para o arquivo raiz:
```bash
streamlit run app.py
```
*Assim que executado, o terminal entregará uma URL (geralmente `http://localhost:8501`) e seu navegador padrão deverá abrir a página automaticamente.*

## 🔄 Controle de Versão e Git

O projeto está configurado para o uso do **Git**. Um arquivo `.gitignore` foi adicionado na raiz para garantir que arquivos temporários, ambientes virtuais e dados sensíveis ou volumosos não sejam enviados para o repositório.

### Como usar o Git neste projeto:

1. **Inicializar o Repositório (se necessário):**
   ```bash
   git init
   ```

2. **Verificar o status dos arquivos:**
   ```bash
   git status
   ```
   *Note que arquivos como `venv/`, `__pycache__/` e arquivos `.csv` estarão ocultos graças ao `.gitignore`.*

3. **Adicionar arquivos:**
   ```bash
   git add .
   ```

4. **Criar um commit:**
   ```bash
   git commit -m "feat: configurando gitignore e estruturando projeto"
   ```

### O que o `.gitignore` está ignorando?
- **Ambientes Virtuais:** `venv/`, `.env` (onde ficam as chaves secretas).
- **Cache de Python:** `__pycache__/`, `*.pyc`.
- **Arquivos de Dados Sensíveis:** Ignorando especificamente os arquivos de tickets originais (`Closed Tickets - 20240912.csv` e `Closed Tickets - 20250818.csv`).
- **Configurações de IDE:** `.vscode/`, `.idea/`.

## 🔄 Principais Modificações (Changelog de Refatoração Arquitetural)
- O repositório transitou de um esquema de Script Simples (Monolítico) para um Padrão MVC em Analytics. O antigo `app.py` possuía acoplamento total das engrenagens lógicas, dados e visual.
- As responsabilidades de conversão do dataset base de *tickets resolutos* foram movidas para `data/loader.py`, garantindo pureza de código ao tratar dados (DateTimes).
- Todos os gráficos gerados com `.update_layout()` foram encapsulados em singletons retornáveis em `utils/charts.py`.
- O código do dashboard exibe um perfil corporativo maduro usando decorators base do Streamlit e modularidade de layout.
