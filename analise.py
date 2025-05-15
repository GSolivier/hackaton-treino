import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Dashboard de gastos financeiros", page_icon="🛒", layout="wide")

df = pd.read_excel('despesas_tratadas.xlsx')

st.sidebar.header("Selecione os Filtros")

setores = st.sidebar.multiselect(
    "Setores",
    options=df["setor"].unique(),
    default=df["setor"].unique(),
    key="setor"
)

tipos = st.sidebar.multiselect(
    "Tipos",
    options=df["tipo"].unique(),
    default=df["tipo"].unique(),
    key="tipo"
)


df_selecao = df.query("setor in @setores and tipo in @tipos")

def Home():
    st.title("📊 Despesas mensais por setor")

    df_selecao['mes_ano'] = df_selecao['data'].dt.to_period('M').astype(str)

    df_grouped = (
        df_selecao
        .groupby(['mes_ano', 'setor'])['valor']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        df_grouped,
        x="mes_ano",
        y="valor",
        color="setor",
        title="Despesas Mensais por Setor",
        labels={"mes_ano": "Mês/Ano", "valor": "Valor (R$)", "setor": "Setor"},
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Mês/Ano",
        yaxis_title="Valor (R$)",
        xaxis=dict(
            type='category',  # ← força o eixo a mostrar todas as categorias
            categoryorder='array',
        ),
        legend_title="Setor",
        xaxis_tickangle=-45,
    )

    st.plotly_chart(fig, use_container_width=True)
    

    gastos_por_setor = df.groupby('setor')['valor'].sum().reset_index()

    fig_barras = px.bar(
        gastos_por_setor,
        x='setor',
        y='valor',
        title='Total de Gastos por Setor',
        labels={'setor': 'Setor', 'valor': 'Valor Total (R$)'},
        color="setor",
        text_auto='.2s'
    )

    fig_barras.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig_barras, use_container_width=True)
        
    df_grouped_tipo = (
        df_selecao.groupby(['tipo', 'setor'])['valor'].sum().reset_index()
    )

    fig_barras_tipo = px.bar(
        df_grouped_tipo,
        x="setor",       # agora eixo X é setor
        y="valor",
        color="tipo",    # e cor para tipo
        title="Despesas por setor",
        labels={"setor": "Setor", "valor": "Valor (R$)", "tipo": "Tipo"},
        text_auto=".2s"
    )

    fig_barras_tipo.update_layout(
        xaxis_title="Setor",
        yaxis_title="Valor (R$)",
        xaxis={'categoryorder':'category ascending'},
        legend_title="Tipo",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_barras_tipo, use_container_width=True)
    
    df_selecao['trimestre'] = df_selecao['data'].dt.to_period('Q').astype(str)
    
    gastos_trimestre = df_selecao.groupby('trimestre')['valor'].sum().reset_index()

    fig_trimestres = px.line(
        gastos_trimestre,
        x='trimestre',
        y='valor',
        title='Gastos Totais por Trimestre',
        labels={'trimestre': 'Trimestre', 'valor': 'Valor Total (R$)'},
        markers=True
    )

    fig_trimestres.update_traces(line=dict(width=3))
    fig_trimestres.update_layout(xaxis_title="Trimestre", yaxis_title="Valor (R$)")

    st.plotly_chart(fig_trimestres, use_container_width=True)
    

def sidebar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=["Home", "Gráficos"],
            icons=["house", "bar-chart"],
            default_index=0,
        )
    
    if selecionado == "Home":
        Home()
    elif selecionado == "Gráficos":
        st.title("aa")
    
sidebar()

    
