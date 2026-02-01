import streamlit as st
from fpdf import FPDF
from datetime import date

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
    
    # Cabeçalho
    pdf.cell(0, 10, text="Ao Ministério das Relações Exteriores (Setor de Contabilidade)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text="Sr Responsável,", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Função para escrever texto com partes destacadas (Negrito e Sublinhado)
    def escrever_misto(texto_normal, dado_destaque, texto_continua=None):
        pdf.set_font("Arial", style="", size=12)
        pdf.write(10, texto_normal)
        pdf.set_font("Arial", style="BU", size=12) # B=Negrito, U=Sublinhado
        pdf.write(10, f" {dado_destaque} ")
        if texto_continua:
            pdf.set_font("Arial", style="", size=12)
            pdf.write(10, texto_continua)

    # Início do Corpo do Texto
    escrever_misto("Eu, ", dados['nome'])
    escrever_misto(", carteira de identidade n° ", dados['identidade'])
    escrever_misto(", CPF ", dados['cpf'])
    pdf.write(10, ", manifesto o interesse em receber os valores das diárias referentes à viagem realizada para ")
    escrever_misto("", dados['localidades'])
    pdf.write(10, " diretamente creditadas na minha conta corrente, cujos dados bancários são: ")
    
    pdf.ln(15)
    
    # Dados Bancários
    escrever_misto("Banco: ", dados['banco'])
    escrever_misto("; Agência: ", dados['agencia'])
    escrever_misto("; Conta Corrente: ", dados['conta'])
    
    pdf.ln(15)
    pdf.set_font("Arial", style="", size=12)
    pdf.multi_cell(0, 10, text="Declaro, ainda, que os dados bancários por mim informados estão ativos no Sistema Integrado de Administração Financeira (SIAFI).")
    
    # Assinatura
    pdf.ln(20)
    pdf.cell(0, 10, text="Respeitosamente/Atenciosamente,", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(15)
    pdf.cell(0, 10, text="________________________________________________", new_x="LMARGIN", new_y="NEXT", align='C')
    
    # Nome e Graduação em Negrito/Sublinhado na assinatura
    pdf.set_font("Arial", style="BU", size=12)
    pdf.cell(0, 10, text=f"{dados['nome']} - {dados['graduacao']}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font("Arial", style="", size=12)
    pdf.cell(0, 10, text=f"Função: {dados['funcao']}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    # Data
    pdf.ln(15)
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    data_str = f"{dados['data_doc'].day} de {meses[dados['data_doc'].month - 1]} de {dados['data_doc'].year}"
    
    pdf.set_font("Arial", style="", size=12)
    pdf.write(10, "Brasília, DF, ")
    pdf.set_font("Arial", style="BU", size=12)
    pdf.write(10, data_str)
    
    return pdf.output()

# --- INTERFACE STREAMLIT ---
st.header("✈️ Preenchimento de Opção de Diária (Anexo B)")

with st.form("form_diaria"):
    nome = st.text_input("Nome Completo").upper()
    
    col1, col2, col3 = st.columns(3)
    identidade = col1.text_input("Identidade")
    cpf = col2.text_input("CPF")
    forca = col3.selectbox("Força", list(DADOS_MILITARES.keys()))
    
    col4, col5 = st.columns(2)
    graduacao = col4.selectbox("Posto/Graduação", DADOS_MILITARES[forca])
    funcao = col5.text_input("Função").upper()
    
    localidades = st.text_area("Cidades/Países da Missão")
    
    st.subheader("Dados Bancários (SIAFI)")
    c_banco, c_ag, c_cc = st.columns(3)
    banco = c_banco.text_input("Banco")
    agencia = c_ag.text_input("Agência")
    conta = c_cc.text_input("Conta Corrente")
    
    data_doc = st.date_input("Data do Documento", value=date.today())
    
    submitted = st.form_submit_button("Gerar PDF com Destaque")

if submitted:
    if not nome or not cpf:
        st.error("Campos obrigatórios faltando.")
    else:
        dados_finais = {
            "nome": nome, "identidade": identidade, "cpf": cpf,
            "forca": forca, "graduacao": graduacao, "funcao": funcao,
            "localidades": localidades, "banco": banco, "agencia": agencia, 
            "conta": conta, "data_doc": data_doc
        }
        pdf_out = gerar_pdf(dados_finais)
        st.download_button(label="📥 Baixar Anexo B", data=bytes(pdf_out), file_name="Anexo_B_Destaque.pdf", mime="application/pdf")
