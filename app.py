import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Lista da Viviane", page_icon="🛒")

DATA_FILE = "compras.json"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                dados = json.load(f)
                # Verifica se o arquivo tem a coluna nova, se não tiver, descarta o antigo
                if len(dados) > 0 and "Produto" not in dados[0]:
                    return []
                return dados
        except:
            return []
    return []

def salvar_dados(lista_dicts):
    with open(DATA_FILE, "w") as f:
        json.dump(lista_dicts, f)

if "lista" not in st.session_state:
    st.session_state.lista = carregar_dados()

st.title("🛒 Minha Lista Editável")

# --- Adição ---
with st.expander("➕ Adicionar Novo Produto"):
    nome = st.text_input("Nome")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Qtd", min_value=1, value=1)
    preco = c2.number_input("Preço", min_value=0.0, format="%.2f")
    
    if st.button("Inserir na Lista", use_container_width=True):
        if nome:
            st.session_state.lista.append({
                "Comprado": False,
                "Produto": nome, 
                "Qtd": qtd, 
                "Preço Unit.": preco
            })
            salvar_dados(st.session_state.lista)
            st.rerun()

st.divider()

# --- Lista/Tabela ---
if st.session_state.lista:
    df = pd.DataFrame(st.session_state.lista)
    
    df_editado = st.data_editor(
        df,
        column_config={
            "Comprado": st.column_config.CheckboxColumn(),
            "Preço Unit.": st.column_config.NumberColumn(format="R$ %.2f"),
            "Qtd": st.column_config.NumberColumn(min_value=1),
        },
        hide_index=True,
        use_container_width=True,
        key="editor_compras"
    )

    # Só salva se houver mudança real
    if not df.equals(df_editado):
        st.session_state.lista = df_editado.to_dict('records')
        salvar_dados(st.session_state.lista)
        st.rerun()

    total = (df_editado["Qtd"] * df_editado["Preço Unit."]).sum()
    st.metric("Total Atual", f"R$ {total:.2f}")

else:
    st.info("Sua lista está vazia!")

if st.button("🔥 Limpar Tudo"):
    st.session_state.lista = []
    salvar_dados([])
    st.rerun()
