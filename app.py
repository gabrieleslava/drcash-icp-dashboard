import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Configuração da Página e Custom CSS para Visual Premium (Glassmorphism & Dark Mode)
st.set_page_config(
    page_title="Dr.Cash | ICP Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom premium CSS injection
st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"], .stApp {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Cards container */
        .metric-container {
            display: flex;
            gap: 1.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        
        /* Metric card styling */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
            flex: 1;
            min-width: 220px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: rgba(13, 148, 136, 0.4);
            box-shadow: 0 20px 25px -5px rgba(13, 148, 136, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
        }
        
        .metric-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #0D9488 0%, #10B981 100%);
        }
        
        .metric-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.075em;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 2.1rem;
            font-weight: 700;
            background: linear-gradient(90deg, #F8FAFC 0%, #E2E8F0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }
        
        .metric-sub {
            font-size: 0.8rem;
            color: #10B981;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Glass card panels */
        .glass-panel {
            background-color: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 1.5rem;
        }
        
        /* Adjust default Streamlit element spacings */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)


# 2. Carregamento e Preparação dos Dados (Seguro e Otimizado)
@st.cache_data
def load_data():
    # Carregamento seguro dos arquivos locais
    df_metrics = pd.read_csv("cohort_drcash.csv")
    df_clinicas = pd.read_csv("cohort_clinicas_drcash.csv")
    
    # Limpeza e Padronização
    df_metrics['Indicador'] = df_metrics['Indicador'].str.strip()
    df_metrics['Categoria'] = df_metrics['Categoria'].str.strip()
    
    df_clinicas['Segmento'] = df_clinicas['Segmento'].str.replace('\r', '').str.strip()
    # Tratando segmentos vazios ou mal formatados
    df_clinicas['Segmento'] = df_clinicas['Segmento'].fillna('Outros')
    df_clinicas['Segmento'] = df_clinicas['Segmento'].replace({
        'DENTISTRY': 'Odontologia', 
        'GENERAL_CLINIC': 'Clínica geral',
        'DERMATOLOGY': 'Estética geral'
    })
    
    # Flag de Rede (Avulsas vs Redes/Parceiros)
    df_clinicas['Tipo de Rede'] = np.where(df_clinicas['Rede'] == 'Clinicas Avulsas', 'Avulsas', 'Redes/Parceiros')
    
    # Melt/Pivot de meses para formato longo (tidy format)
    meses = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05']
    df_melt = pd.melt(
        df_metrics, 
        id_vars=['Safra (Cohort)', 'Categoria', 'Indicador'], 
        value_vars=meses, 
        var_name='Mês Referência', 
        value_name='Valor'
    )
    df_melt = df_melt.dropna(subset=['Valor'])
    
    return df_metrics, df_clinicas, df_melt

try:
    df_metrics, df_clinicas, df_melt = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.info("Certifique-se de que os arquivos 'cohort_drcash.csv' e 'cohort_clinicas_drcash.csv' estão na mesma pasta.")
    st.stop()


# 3. Barra Lateral de Filtros Avançados
st.sidebar.image("https://drcash.com.br/wp-content/uploads/2021/05/logo-dr-cash.png", width=160)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.title("🎛️ Filtros de Análise")

# Filtro 1: Safra (Cohort)
todas_safras = sorted(df_clinicas['Safra (Cohort)'].unique())
safra_selecionada = st.sidebar.multiselect(
    "Selecione as Safras (Cohorts):", 
    options=todas_safras, 
    default=todas_safras
)

if not safra_selecionada:
    st.warning("⚠️ Selecione pelo menos uma safra na barra lateral para carregar os dados.")
    st.stop()

# Filtrando os DataFrames primários com base nas Safras
df_clinicas_filtered = df_clinicas[df_clinicas['Safra (Cohort)'].isin(safra_selecionada)]
df_melt_filtered = df_melt[df_melt['Safra (Cohort)'].isin(safra_selecionada)]

# Filtros Demográficos adicionais para análise de Clínicas
st.sidebar.markdown("---")
st.sidebar.subheader("Segmentação Cadastral")

estados_disponiveis = sorted(df_clinicas_filtered['Estado'].dropna().unique())
estados_selecionados = st.sidebar.multiselect("Filtrar por Estado (UF):", options=estados_disponiveis, default=estados_disponiveis)

segmentos_disponiveis = sorted(df_clinicas_filtered['Segmento'].dropna().unique())
segmentos_selecionados = st.sidebar.multiselect("Filtrar por Especialidade:", options=segmentos_disponiveis, default=segmentos_disponiveis)

# Aplicando os filtros demográficos extras (apenas afeta os visuais das clínicas)
df_clinicas_demog = df_clinicas_filtered[
    (df_clinicas_filtered['Estado'].isin(estados_selecionados)) &
    (df_clinicas_filtered['Segmento'].isin(segmentos_selecionados))
]


# Header do Dashboard
st.markdown("<h1>🎯 Dr.Cash <span style='font-weight:300; font-size:1.8rem; color:#0D9488;'>| ICP & Retenção de Clínicas</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94A3B8; margin-top:-10px; font-size:1.1rem; margin-bottom:25px;'>Análise de comportamento das safras de clínicas, métricas de engajamento e perfil do ICP corporativo.</p>", unsafe_allow_html=True)


# 4. KPIs Principais com CSS Customizado e Ícones
receita_total = df_melt_filtered[df_melt_filtered['Indicador'] == 'Receita']['Valor'].sum()
clinicas_adquiridas = len(df_clinicas_demog)

# Percentual de redes
if clinicas_adquiridas > 0:
    redes_pct = (len(df_clinicas_demog[df_clinicas_demog['Tipo de Rede'] == 'Redes/Parceiros']) / clinicas_adquiridas) * 100
else:
    redes_pct = 0.0

# Especialidade dominante
esp_mode = df_clinicas_demog['Segmento'].mode()
esp_dominante = esp_mode[0] if not esp_mode.empty else "N/A"

st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">Clínicas Adquiridas</div>
            <div class="metric-value">{clinicas_adquiridas:,}</div>
            <div class="metric-sub">🏥 Ativas no cadastro filtrado</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Receita Acumulada</div>
            <div class="metric-value">R$ {receita_total:,.2f}</div>
            <div class="metric-sub">💳 Faturamento total gerado</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Penetração de Redes</div>
            <div class="metric-value">{redes_pct:.1f}%</div>
            <div class="metric-sub">🔗 Clínicas associadas a redes</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Especialidade Dominante</div>
            <div class="metric-value" style="font-size: 1.8rem; padding-top:4px; padding-bottom:4px;">{esp_dominante}</div>
            <div class="metric-sub">⭐ Maior volume cadastrado</div>
        </div>
    </div>
""", unsafe_allow_html=True)


# 5. Organização em Tabs (Estrutura de Aplicação Profissional)
tab_overview, tab_cohort = st.tabs(["📊 Visão Geral & ICP", "🎯 Matriz de Cohort & Retenção"])

# ================= TAB 1: VISÃO GERAL & ICP =================
with tab_overview:
    
    colA, colB = st.columns(2)
    
    # Gráfico A: Evolução da Receita
    with colA:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("📈 Receita por Safra ao Longo do Tempo")
        
        df_receita = df_melt_filtered[df_melt_filtered['Indicador'] == 'Receita']
        
        fig_receita = px.line(
            df_receita, 
            x='Mês Referência', 
            y='Valor', 
            color='Safra (Cohort)', 
            markers=True,
            labels={'Valor': 'Receita (R$)', 'Mês Referência': 'Mês de Referência'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_receita.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_receita, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Gráfico B: Composição Avulsas vs Redes
    with colB:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("🏢 Estrutura das Clínicas (Avulsas vs Redes)")
        
        df_rede_grp = df_clinicas_demog.groupby(['Safra (Cohort)', 'Tipo de Rede']).size().reset_index(name='Quantidade')
        
        fig_rede = px.bar(
            df_rede_grp, 
            x='Safra (Cohort)', 
            y='Quantidade', 
            color='Tipo de Rede',
            barmode='group',
            labels={'Quantidade': 'Nº de Clínicas', 'Safra (Cohort)': 'Safra'},
            color_discrete_map={'Avulsas': '#0D9488', 'Redes/Parceiros': '#EF4444'} # Teal and Crimson
        )
        fig_rede.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_rede, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    colC, colD = st.columns(2)
    
    # Gráfico C: Distribuição de Segmentos (ICP)
    with colC:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("🍕 Distribuição por Especialidade (Segmento)")
        
        df_seg_grp = df_clinicas_demog.groupby('Segmento').size().reset_index(name='Qtd').sort_values('Qtd', ascending=False)
        
        fig_seg = px.pie(
            df_seg_grp, 
            values='Qtd', 
            names='Segmento', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal_r
        )
        fig_seg.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig_seg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Gráfico D: Ticket Médio Fechado
    with colD:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("💵 Evolução do Ticket Médio (Propostas Fechadas)")
        
        df_ticket = df_melt_filtered[df_melt_filtered['Indicador'] == 'Ticket medio fechadas']
        
        fig_ticket = px.line(
            df_ticket, 
            x='Mês Referência', 
            y='Valor', 
            color='Safra (Cohort)', 
            markers=True,
            labels={'Valor': 'Ticket Médio (R$)', 'Mês Referência': 'Mês de Referência'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_ticket.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_ticket, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: MATRIZ DE COHORT & RETENÇÃO =================
with tab_cohort:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.subheader("🔍 Matriz de Retenção Ativa de Clínicas")
    st.markdown("""
        Esta matriz mostra a retenção relativa das clínicas ao longo dos meses. O **Mês 0** representa o mês de entrada (Safra) 
        e os meses subsequentes representam a taxa de clínicas ativas em relação ao número inicial de clínicas adquiridas naquela safra.
    """)
    
    # 1. Puxar dados de clínicas ativas e clínicas totais
    df_cohort_active = df_melt_filtered[df_melt_filtered['Indicador'] == 'Clinicas Ativas']
    df_cohort_total = df_melt_filtered[df_melt_filtered['Indicador'] == 'Total de clínicas']
    
    if df_cohort_active.empty or df_cohort_total.empty:
        st.info("Sem dados de clínicas ativas disponíveis para as safras selecionadas.")
    else:
        # Pivo para safras e meses
        pivot_active = df_cohort_active.pivot(index='Safra (Cohort)', columns='Mês Referência', values='Valor')
        pivot_total = df_cohort_total.pivot(index='Safra (Cohort)', columns='Mês Referência', values='Valor')
        
        months_order = sorted(list(df_melt['Mês Referência'].unique()))
        safras_list = sorted(list(pivot_active.index))
        
        # Estruturando matriz de retenção de meses relativos (Mês 0, Mês 1, etc.)
        num_safras = len(safras_list)
        num_months = len(months_order)
        
        ret_matrix = np.full((num_safras, num_months), np.nan)
        text_matrix = np.full((num_safras, num_months), "", dtype=object)
        
        for i, safra in enumerate(safras_list):
            safra_start_idx = months_order.index(safra)
            
            # Percorrendo os meses a partir do mês em que a safra iniciou
            for m_idx, month in enumerate(months_order[safra_start_idx:]):
                rel_month = m_idx  # Mês 0, Mês 1, ...
                
                # Resgata valor de ativas e totais
                act = pivot_active.loc[safra, month] if month in pivot_active.columns else np.nan
                tot = pivot_total.loc[safra, month] if month in pivot_total.columns else np.nan
                
                # Fallback seguro para o tamanho inicial da safra caso o total venha vazio
                if pd.isna(tot) or tot == 0:
                    tot = pivot_total.loc[safra, safra] if safra in pivot_total.columns else np.nan
                if pd.isna(tot) or tot == 0:
                    tot = act # Fallback extremo
                
                if not pd.isna(act) and not pd.isna(tot) and tot > 0:
                    pct = (act / tot) * 100
                    ret_matrix[i, rel_month] = pct
                    text_matrix[i, rel_month] = f"{pct:.1f}%<br>({int(act)}/{int(tot)})"
        
        # Plot do Heatmap Cohort
        fig_heat = go.Figure(data=go.Heatmap(
            z=ret_matrix,
            x=[f"Mês {i}" for i in range(num_months)],
            y=safras_list,
            text=text_matrix,
            texttemplate="%{text}",
            hoverinfo="text",
            colorscale="Teal",
            zmin=0,
            zmax=100,
            showscale=True,
            colorbar=dict(title="Retenção", ticksuffix="%")
        ))
        
        fig_heat.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Meses desde o Cadastro (Relativo)", tickmode="linear"),
            yaxis=dict(title="Safra do Cohort", type="category", autorange="reverse"),
            margin=dict(l=40, r=40, t=20, b=40),
            height=350
        )
        
        st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Detalhes de Performance do Cohort
    st.subheader("📋 Comparador Geral de Métricas por Safra")
    st.markdown("Selecione um indicador para comparar o desempenho numérico das safras lado a lado:")
    
    indicadores_disponiveis = sorted(df_melt_filtered['Indicador'].unique())
    indicador_selecionado = st.selectbox("Escolha o Indicador para Tabela:", options=indicadores_disponiveis, index=indicadores_disponiveis.index("Receita") if "Receita" in indicadores_disponiveis else 0)
    
    df_compare = df_melt_filtered[df_melt_filtered['Indicador'] == indicador_selecionado]
    pivot_compare = df_compare.pivot(index='Safra (Cohort)', columns='Mês Referência', values='Valor')
    
    # Formatação elegante da tabela
    st.dataframe(
        pivot_compare.style.format("{:,.2f}", na_rep="-").background_gradient(cmap="BuGn", axis=1),
        use_container_width=True
    )


# 6. Rodapé e Links Úteis
st.markdown("---")
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    st.markdown("<p style='color:#64748B; font-size:0.85rem;'>Dashboard desenvolvido com Streamlit & Plotly. Dados confidenciais Dr.Cash.</p>", unsafe_allow_html=True)
with col_foot2:
    st.markdown("<p style='color:#64748B; font-size:0.85rem; text-align:right;'>Safra ativa: " + ", ".join(safra_selecionada) + "</p>", unsafe_allow_html=True)
