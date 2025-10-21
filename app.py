import streamlit as st
import matplotlib.pyplot as plt
import os

ARQUIVO = "aluno.txt"

def salvar(nome, serie, n1, n2, n3):
    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(f"{nome},{serie},{n1},{n2},{n3}\n")

def ldados():
    if not os.path.exists(ARQUIVO):
        return[]
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    dados = []
    for linha in linhas:
        partes = linha.strip().split(",")
        if len(partes) ==5:
            nome, serie, n1, n2, n3 = partes
            notas = list(map(float, [n1, n2, n3]))
            dados.append((nome, serie, notas))
    return dados

def media(dados):
    medias = {}
    for nome, serie,notas in dados:
        media = sum(notas) / 3
        if serie not in medias:
            medias[serie] = []
        medias[serie].append(media)
    return medias

st.title("Sistemas de Relatórios de Notas")

aba = st.sidebar.selectbox(('Esolha uma opção'), ["Cadastrar Aluno", "Relatórios"])
if aba =="Cadastrar Aluno":
    st.header("Cadastro de Aluno")
    nome = st.text_input("Nome do aluno:")
    serie = st.text_input("Série")
    n1 = st.number_input("Nota 1", 0.0, 10.0, step=0.1)
    n2 = st.number_input("Nota 2", 0.0, 10.0, step=0.1)
    n3 = st.number_input("Nota 3", 0.0, 10.0, step=0.1)

    if st.button("Salvar Aluno"):
        if nome and serie:
            salvar(nome, serie, n1, n2, n3)
            st.success(f"Aluno {nome} salvo vom sucesso")
        else:
            st.warning("preencha todos os campos")

elif aba == "Relatórios":
    st.header("Relatório de notas")
    dados = ldados()
    if not dados:
        st.info("Nenhum dado Cadastrado ainda")
    else:
        medias = media(dados)
        series =list(medias.keys())
        mediageral = {s: sum(medias[s]) / len(medias[s]) for s in series}

        st.subheader("Média geral por Série")
        for serie, media in mediageral.items():
            st.write(f"**{serie}:** {media:.2f}")
        
        serieselecionada = st.selectbox("Selecioneuma Série para ver o gráfico:", series)
        if serieselecionada:
            fig, ax = plt.subplots()
            ax.bar(range(len(medias[serieselecionada])), medias[serieselecionada])   
            ax.set_title(f"Distribuição das médias / {serieselecionada}.")
            ax.set_xlabel("Alunos.")
            ax.set_ylabel("Média final.")
            st.pyplot(fig)