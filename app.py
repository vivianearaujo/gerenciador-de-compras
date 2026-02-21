import streamlit as st
import json
import os

# 1. Configuração SEMPRE no topo
st.set_page_config(page_title="Lista Viviane")

# 2. Caminho do arquivo
DATA_FILE = "compras.json"

# 3. Funções de dados
def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(lista):
    with open(DATA_FILE, "w") as f:
        json.dump(lista, f)

# 4. Inicializar Estado
if "lista" not in st.session_state:
    st.session_state.lista = carregar_dados()

# 5. Interface
st.title("🛒 Minha Lista")

nome = st.text_input("Produto")
c1, c2 = st.columns(2)
qtd = c1.number_input("Qtd", min_value=1, value=1)
preco = c2.number_input("Preço", min_value=0.0, format="%.2f")

if st.button("Adicionar"):
    if nome:
        st.session_state.lista.append({"nome": nome, "qtd": qtd, "preco": preco})
        salvar_dados(st.session_state.lista)
        st.rerun()

st.divider()

total = 0.0
for i, item in enumerate(st.session_state.lista):
    subtotal = item['qtd'] * item['preco']
    total += subtotal
    st.write(f"{item['nome']} - {item['qtd']}x: R$ {subtotal:.2f}")

st.header(f"Total: R$ {total:.2f}")
