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
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(lista_dicts):
    with open(DATA_FILE, "w") as f:
        json.dump(lista_dicts, f)

if "lista" not in st.session_state:
    st.session_state.lista = carregar_dados()

st.title("🛒 Minha Lista Editável")

# --- Área de Adição ---
with st.expander("➕ Adicionar Novo Produto", expanded=False):
    nome = st.text_input("Nome")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Qtd Inicial", min_value=1, value=1)
    preco = c2.number_input("Preço Inicial", min_value=0.0, format="%.2f")
    
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

# --- Área de Edição Direta ---
if st.session_state.lista:
    st.write("💡 *Toque nos valores abaixo para editar quantidade ou preço:*")
    
    # Convertemos para DataFrame (tabela) para usar o editor poderoso
    df = pd.DataFrame(st.session_state.lista)
    
    # Configuração do Editor
    df_editado = st.data_editor(
        df,
        column_config={
            "Comprado": st.column_config.CheckboxColumn(),
            "Preço Unit.": st.column_config.NumberColumn(format="R$ %.2f"),
            "Qtd": st.column_config.NumberColumn(min_value=1),
        },
        disabled=["Produto"], # Opcional: trava o nome para não mudar sem querer
        hide_index=True,
        use_container_width=True,
        key="editor_compras"
    )

    # Se houve mudança na tabela, salvamos
    if not df.equals(df_editado):
        st.session_state.lista = df_editado.to_dict('records')
        salvar_dados(st.session_state.lista)
        st.rerun()

    # Cálculo do Total
    total = (df_editado["Qtd"] * df_editado["Preço Unit."]).sum()
    st.metric("Total Atual", f"R$ {total:.2f}")

else:
    st.info("Sua lista está vazia. Adicione itens acima!")

# --- Funções Extras ---
st.divider()
col_a, col_b = st.columns(2)

if col_a.button("🗑️ Excluir Selecionados"):
    # Remove itens que estão com o Checkbox marcado
    st.session_state.lista = [item for item in st.session_state.lista if not item["Comprado"]]
    salvar_dados(st.session_state.lista)
    st.rerun()

if col_b.button("🔥 Limpar Tudo"):
    st.session_state.lista = []
    salvar_dados([])
    st.rerun()
