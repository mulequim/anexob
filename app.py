import streamlit as st
from fpdf import FPDF
from datetime import date

# Dados para os selects (Exemplo simplificado)
DADOS_MILITARES = {
    "Aeronáutica": ["Marechal do Ar", "Tenente-Brigadeiro", "Major-Brigadeiro", "Brigadeiro", "Coronel", "Tenente-Coronel", "Major", "Capitão", "Primeiro-Tenente", "Segundo-Tenente", "Aspirante", "Suboficial", "Primeiro-Sargento", "Segundo-Sargento", "Terceiro-Sargento", "Cabo", "Soldado"],
    "Exército": ["Marechal", "General de Exército", "General de Divisão", "General de Brigada", "Coronel", "Tenente-Coronel", "Major", "Capitão", "Primeiro-Tenente", "Segundo-Tenente", "Aspirante", "Subtenente", "Primeiro-Sargento", "Segundo-Sargento", "Terceiro-Sargento", "Cabo", "Soldado"],
    "Marinha": ["Almirante", "Almirante de Esquadra", "Vice-Almirante", "Contra-Almirante", "Capitão de Mar e Guerra", "Capitão de Fragata", "Capitão de Corveta", "Capitão-Tenente", "Primeiro-Tenente", "Segundo-Tenente", "Guarda-Marinha", "Suboficial", "Primeiro-Sargento", "Segundo-Sargento", "Terceiro-Sargento", "Cabo", "Marinheiro"]
}

# Localidades (Pode ser expandido ou usar uma API)
LOCALIDADES = {
    "Brasil": ["Brasília", "Rio de Janeiro", "São Paulo"],
    "Estados Unidos": ["Washington", "Nova York", "Miami"],
    "Panamá": ["Cidade do Panamá", "Colón"],
    "Coreia do Sul": ["Seul", "Busan"],
    "Índia": ["Nova Deli", "Mumbai"],
    "Tunísia": ["Túnis", "Sfax"]
}

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho baseado no formulário [cite: 1, 2]
    pdf.cell(200, 10, txt="Ao Ministério das Relações Exteriores (Setor de Contabilidade)", ln=True)
    pdf.cell(200, 10, txt="Sr Responsável,", ln=True, h=15)
    
    # Corpo do texto [cite: 3, 4, 5, 6, 7, 8]
    texto = (f"Eu, {dados['nome']}, carteira de identidade n° {dados['identidade']}, CPF {dados['cpf']}, "
             f"manifesto o interesse em receber os valores das diárias referentes à viagem realizada para "
             f"{dados['localidades']} diretamente creditadas na minha conta corrente.")
    pdf.multi_cell(0, 10, txt=texto)
    
    # Dados Bancários [cite: 8, 9, 10, 11]
    pdf.ln(5)
    pdf.cell(0, 10, txt=f"Banco: {dados['banco']}; Agência: {dados['agencia']} Conta Corrente: {dados['conta']}", ln=True)
    pdf.multi_cell(0, 10, txt="Declaro, ainda, que os dados bancários por mim informados estão ativos no Sistema Integrado de Administração Financeira (SIAFI).")
    
    # Assinatura e Data [cite: 12, 13, 14, 15, 16]
    pdf.ln(20)
    pdf.cell(0, 10, txt="Respeitosamente/Atenciosamente,", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, txt="________________________________________________", ln=True, align='C')
    pdf.cell(0, 10, txt=f"{dados['nome']} - {dados['graduacao']} ({dados['forca']})", ln=True, align='C')
    pdf.cell(0, 10, txt=f"Função: {dados['funcao']}", ln=True, align='C')
    
    data_formatada = dados['data_doc'].strftime("%d de %B de %Y")
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Brasília, DF, {data_formatada}", ln=True, align='R')
    
    return pdf.output()

# --- INTERFACE STREAMLIT ---
st.title("Gerador de Formulário de Diárias")

with st.expander("Dados Pessoais e Militares"):
    nome = st.text_input("Nome Completo")
    col1, col2 = st.columns(2)
    identidade = col1.text_input("Identidade")
    cpf = col2.text_input("CPF")
    
    forca = st.selectbox("Força Armada", list(DADOS_MILITARES.keys()))
    graduacao = st.selectbox("Posto/Graduação", DADOS_MILITARES[forca])
    funcao = st.text_input("Função")

with st.expander("Dados da Viagem"):
    paises_selecionados = st.multiselect("Selecione os Países", list(LOCALIDADES.keys()))
    cidades_selecionadas = []
    for p in paises_selecionados:
        cidades = st.multiselect(f"Cidades em {p}", LOCALIDADES[p])
        cidades_selecionadas.extend(cidades)
    
    data_doc = st.date_input("Data do Documento", value=date.today())

with st.expander("Dados Bancários"):
    banco = st.text_input("Banco")
    col3, col4 = st.columns(2)
    agencia = col3.text_input("Agência")
    conta = col4.text_input("Conta Corrente")

if st.button("Gerar PDF"):
    dados = {
        "nome": nome, "identidade": identidade, "cpf": cpf,
        "forca": forca, "graduacao": graduacao, "funcao": funcao,
        "localidades": ", ".join(cidades_selecionadas) if cidades_selecionadas else "_______",
        "banco": banco, "agencia": agencia, "conta": conta, "data_doc": data_doc
    }
    pdf_bytes = gerar_pdf(dados)
    st.download_button("Baixar Formulário PDF", data=pdf_bytes, file_name="Formulario_Diaria.pdf", mime="application/pdf")
