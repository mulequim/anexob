import streamlit as st
from fpdf import FPDF
from datetime import date

# Configuração da Página
st.set_page_config(page_title="Gerador Anexo Bravo - GTE", page_icon="✈️")

DADOS_MILITARES = {
    "Aeronáutica": ["Cel", "Ten Cel", "Maj", "Cap", "1º Ten", "2º Ten", "Asp", "SO", "1º Sgt", "2º Sgt", "3º Sgt", "Cb", "S1", "S2"],
    "Exército": ["Cel", "Ten Cel", "Maj", "Cap", "1º Ten", "2º Ten", "Asp", "ST", "1º Sgt", "2º Sgt", "3º Sgt", "Cb", "Sd"],
    "Marinha": ["CMG", "CF", "CC", "CT", "1º Ten", "2º Ten", "GM", "SO", "1º Sgt", "2º Sgt", "3º Sgt", "Cb", "Mn"]
}

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Destinatário [cite: 1, 2]
    pdf.cell(0, 10, text="Ao Ministério das Relações Exteriores (Setor de Contabilidade)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text="Sr Responsável,", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # 2. Corpo do Texto [cite: 3, 4, 5, 6, 7]
    texto = (f"Eu, {dados['nome']}, carteira de identidade n° {dados['identidade']}, CPF {dados['cpf']}, "
             f"manifesto o interesse em receber os valores das diárias referentes à viagem realizada para "
             f"{dados['localidades']} diretamente creditadas na minha conta corrente, cujos dados bancários são:")
    pdf.multi_cell(0, 10, text=texto)
    pdf.ln(5)
    
    # 3. Dados Bancários [cite: 8, 9, 10, 11]
    pdf.cell(0, 10, text=f"Banco: {dados['banco']}; Agência: {dados['agencia']}; Conta Corrente: {dados['conta']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.multi_cell(0, 10, text="Declaro, ainda, que os dados bancários por mim informados estão ativos no Sistema Integrado de Administração Financeira (SIAFI).")
    
    # 4. Assinatura [cite: 12, 16]
    pdf.ln(20)
    pdf.cell(0, 10, text="Respeitosamente/Atenciosamente,", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.cell(0, 10, text="________________________________________________", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, text=f"{dados['nome']} - {dados['graduacao']}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, text=f"Função: {dados['funcao']}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    # 5. Local e Data [cite: 13, 14, 15]
    pdf.ln(15)
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", " junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    dia = dados['data_doc'].day
    mes = meses[dados['data_doc'].month - 1]
    ano = dados['data_doc'].year
    pdf.cell(0, 10, text=f"Brasília, DF, {dia} de {mes} de {ano}", new_x="LMARGIN", new_y="NEXT", align='R')
    
    return pdf.output()

# --- INTERFACE STREAMLIT ---
st.header("✈️ Preenchimento de Opção de Diária (Anexo B)")

with st.form("form_diaria"):
    col1, col2 = st.columns([2, 1])
    nome = col1.text_input("Nome Completo")
    forca = col2.selectbox("Força", list(DADOS_MILITARES.keys()))
    
    col3, col4, col5 = st.columns(3)
    identidade = col3.text_input("Identidade")
    cpf = col4.text_input("CPF")
    graduacao = col5.selectbox("Posto/Graduação", DADOS_MILITARES[forca])
    
    funcao = st.text_input("Função (Ex: Mecânico de Voo, Comissário, etc.)")
    
    localidades = st.text_area("Cidades/Países da Missão (Ex: Seul/Coreia do Sul, Túnis/Tunísia)")
    
    st.subheader("Dados Bancários (SIAFI)")
    c_banco, c_ag, c_cc = st.columns(3)
    banco = c_banco.text_input("Banco")
    agencia = c_ag.text_input("Agência")
    conta = c_cc.text_input("Conta Corrente")
    
    data_doc = st.date_input("Data do Documento", value=date.today())
    
    submitted = st.form_submit_button("Gerar PDF para Impressão")

if submitted:
    if not nome or not cpf:
        st.error("Por favor, preencha o nome e o CPF.")
    else:
        dados_finais = {
            "nome": nome.upper(), "identidade": identidade, "cpf": cpf,
            "forca": forca, "graduacao": graduacao, "funcao": funcao.upper(),
            "localidades": localidades, "banco": banco, "agencia": agencia, 
            "conta": conta, "data_doc": data_doc
        }
        pdf_out = gerar_pdf(dados_finais)
        st.success("PDF Gerado com sucesso!")
        st.download_button(label="📥 Baixar Anexo B", data=bytes(pdf_out), file_name=f"Anexo_B_{nome.replace(' ', '_')}.pdf", mime="application/pdf")
