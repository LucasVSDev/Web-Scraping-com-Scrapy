# Import ultilizados
import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("../data/quotes.db")

# Carregar os dados da tabela 'mercadolivre_items' em uma DataFrame pandas
df = pd.read_sql_query("SELECT * FROM mercadolivre_item", conn)

# Fechar a conexão com o banco de dados
conn.close()

# Título da aplicação
st.title("Pesquisar de mercado - Tenis Esportivos no mercado Livre")

# melhorar o layout com colunas para KPIs
st.subheader("KPIs principais do sistema")
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label="Número total de itens", value=total_itens)
# KPI 2: Número de marcas únicas
unique_brands = df["brand"].nunique()
col2.metric(label="Número de Marcas Únicas", value=unique_brands)

# KPI 3: Preço médio novo (em reias)
average_new_price = df["new_price"].mean()
col3.metric(label="Preço Médio Novo (R$)", value=f"{average_new_price:.2f}")

# Quais marcas são mais encontradas até a 10ª página
col1, col2 = st.columns([4, 2])
top_10_pages_brand = df["brand"].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brand)
col2.write(top_10_pages_brand)

# Quais o preço médio por marca
st.subheader("Preço Médio por marca")
df_non_zero_price = df[df["new_price"] > 0]  # Tira os resultados de reviews com zero
col1, col2 = st.columns([4, 2])
averege_price_by_brand = (
    df_non_zero_price.groupby("brand")["new_price"].mean().sort_values(ascending=False)
)
col1.bar_chart(averege_price_by_brand)
col2.write(averege_price_by_brand)

# Qual a satisfção por marca
st.subheader("Satisfação por marca")
col1, col2 = st.columns([4, 3])
df_non_zero_reviews = df[
    df["reviews_rating_number"] > 0
]  # Tira os resultados de reviews com zero
satisfaction_by_brand = (
    df_non_zero_reviews.groupby("brand")["reviews_rating_number"]
    .mean()
    .sort_values(ascending=False)
)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
