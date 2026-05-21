import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# Configuração visual
st.set_page_config(page_title="Diagnóstico MAPI - Inteligência Política", page_icon="🧩", layout="centered")

st.title("Seu posicionamento político está preparado para a nova era?")
st.markdown("### Descubra se sua pré-campanha transmite autoridade e conexão real através dos ODS.")
st.write("---")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulário de Captura
with st.form("quiz_attraction"):
    st.subheader("📋 Informações Estratégicas")
    nome = st.text_input("Seu Nome / Nome do Pré-Candidato *")
    whatsapp = st.text_input("WhatsApp de Contato (com DDD) *")
    email = st.text_input("Seu melhor E-mail *")
    instagram = st.text_input("Qual o seu @ do Instagram? (Ex: @seu_perfil) *")
    cidade = st.text_input("Cidade / Estado de Atuação *")
    cargo = st.selectbox("Cargo Pretendido em 2026 *", [
        "Deputado Estadual", "Deputado Federal", "Majoritária (Senado/Governo/Vice)", "Assessor / Coordenador de Campanha"
    ])
    
    st.write("---")
    
    # Perguntas (O seu questionário completo)
    q1 = st.radio("1. Você consegue resumir claramente a principal causa que defende?", ["Sim, com total clareza", "Mais ou menos, mudo o foco às vezes", "Ainda não defini um nicho claro"])
    q2 = st.radio("2. Seu posicionamento político está conectado a algum impacto social específico e mensurável?", ["Sim, minhas pautas são baseadas em indicadores reais", "Parcialmente, defendo causas gerais", "Não, foco em críticas ou propostas genéricas"])
    q3 = st.radio("3. O eleitor comum entende facilmente: 'Por que votar em você e não no seu adversário?'", ["Sim, meu diferencial é nítido", "Às vezes sinto que me confundem com outros candidatos", "Não, ainda preciso desenhar essa differentiation"])
    q4 = st.radio("4. Você possui uma narrativa política estruturada?", ["Sim, tenho meu 'porquê', minha história e bandeiras alinhadas", "Parcialmente, tenho ideias soltas", "Não tenho uma narrativa definida ainda"])
    
    q5 = st.radio("5. Sua comunicação gera Autoridade, Identificação e Confiança?", ["Sim, o retorno do público valida isso", "Em partes, gera engajamento, mas não sinto autoridade", "Ainda não consegui passar essa imagem"])
    q6 = st.radio("6. Você possui uma mensagem-chave forte e consistente?", ["Sim, minha equipe e eu falamos a mesma língua", "Parcialmente, a mensagem muda", "Não, atiro para todos os lados"])
    q7 = st.radio("7. Seu conteúdo possui estratégia de dados?", ["Estratégia clara", "Um pouco dos dois", "Apenas postagem de rotina"])
    q8 = st.radio("8. Seu posicionamento diferencia você visualmente e conceitualmente?", ["Sim, nossa identidade e discurso são únicos", "Parcialmente, parece o padrão político", "Não, parece o mesmo"])
    
    q9 = st.radio("9. Você consegue provar e mensurar o impacto real das suas ações?", ["Sim, uso dados públicos", "Parcialmente, sei de forma intuitiva", "Não, minhas propostas são conceituais"])
    q10 = st.radio("10. Suas propostas possuem conexão direta com os ODS?", ["Sim, mapeamos nossos projetos", "Algumas batem por configuração", "Não adotamos os ODS ainda"])
    q11 = st.radio("11. Sua imagem pública transmite Legado, Liderança e Preparo?", ["Sim, sou visto como um quadro preparado", "Parcialmente, falta imagem de gestor", "Não, sou apenas mais um"])
    q12 = st.radio("12. Reconhecimento Real ou Visibilidade Passageira?", ["Reconhecimento: o eleitor lembra do que defendo", "Ambos: tenho picos, mas oscilo", "Apenas visibilidade"])

    enviar = st.form_submit_button("🔥 GERAR MEU DIAGNÓSTICO")

# Lógica de processamento
if enviar:
    if not nome or not whatsapp or not cidade or not email or not instagram:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        # (Opcional: você pode simplificar o cálculo das pontuações aqui se quiser, 
        # mas a estrutura básica é essa)
        score_total = 36 # Exemplo simplificado
        
        nova_linha = {
            "Data_Hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nome": nome, "WhatsApp": whatsapp, "E-mail": email, "Instagram": instagram, 
            "Cidade": cidade, "Cargo": cargo, "Total_Score": int(score_total)
        }
        
        try:
            dados_existentes = conn.read(worksheet="Página1")
            df_atual = pd.DataFrame(dados_existentes)
        except Exception:
            df_atual = pd.DataFrame()