import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÕES INICIAIS ---
# Definição da hora certa com fuso horário de Brasília (UTC-3)
fuso_brasilia = timezone(timedelta(hours=-3))
hora_certa = datetime.now(fuso_brasilia).strftime('%d/%m/%Y %H:%M:%S')

# Configuração visual
st.set_page_config(page_title="Diagnóstico MAPI - Inteligência Política", page_icon="🧩", layout="centered")

st.title("Impacto comprovado conquista votos.")
st.markdown("### Descubra se o eleitor reconhece sua atuação como promessa política ou liderança de impacto real.")
st.write("---")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULÁRIO DE CAPTURA ---
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
    
    # Perguntas
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

    # Botão oficial do formulário
    enviar = st.form_submit_button("🔥 GERAR MEU DIAGNÓSTICO")

# --- LÓGICA DE PROCESSAMENTO E RESULTADO ---
# Tudo acontece aqui dentro quando o usuário clica em enviar!
if enviar:
    if not nome or not whatsapp or not cidade or not email or not instagram:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        # 1. CÁLCULO DINÂMICO DE PONTOS
        respostas = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12]
        total_score = 0
        for resp in respostas:
            if resp.startswith("Sim") or resp.startswith("Estratégia") or resp.startswith("Reconhecimento"):
                total_score += 10
            elif resp.startswith("Parcialmente") or resp.startswith("Mais ou menos") or resp.startswith("Às vezes") or resp.startswith("Em partes") or resp.startswith("Um pouco") or resp.startswith("Algumas") or resp.startswith("Ambos"):
                total_score += 5
            # Respostas negativas somam 0

        # 2. SALVAR NA PLANILHA GOOGLE
        novo_dado = {
            "Data_Hora": hora_certa,
            "Nome": nome,
            "WhatsApp": whatsapp,
            "E-mail": email,
            "Instagram": instagram,
            "Cidade": cidade,
            "Cargo": cargo,
            "Total_Score": total_score
        }
        
        try:
            dados_existentes = conn.read(worksheet="Página1")
            df_atual = pd.DataFrame(dados_existentes)
        except Exception:
            df_atual = pd.DataFrame()
            
        df_novo = pd.DataFrame([novo_dado])
        df_final = pd.concat([df_atual, df_novo], ignore_index=True)
        conn.update(worksheet="Página1", data=df_final)
        
        # 3. DEFINIR O PERFIL COM BASE NO SCORE
        if total_score >= 80:
            perfil = "🔥 Perfil 3 – Liderança Estratégica"
            detalhe_perfil = "Sua pré-campanha já demonstra posicionamento e potencial de autoridade máxima."
        elif total_score >= 50:
            perfil = "⚡ Perfil 2 – Potencial em Crescimento"
            detalhe_perfil = "Sua pré-campanha tem bons alicerces, mas precisa refinar a estratégia digital."
        else:
            perfil = "🌱 Perfil 1 – Estruturação Inicial"
            detalhe_perfil = "Sua jornada está no começo. É hora de construir sua base de conexão real."

        # 4. EXIBIR O DIAGNÓSTICO NA TELA
        st.success("✅ Informações processadas com sucesso!")
        st.markdown("---")
        st.subheader("📊 Seu Diagnóstico MAPI está pronto!")
        st.markdown(f"### {perfil}")
        st.write(detalhe_perfil)
        
        st.write("Como interpretar esses indicadores e aplicar na sua cidade?")
        st.write("O próximo passo é entender quais ODS específicos o seu município necessita para se destacar.")

        # 5. CONFIGURAR E EXIBIR O BOTÃO DO WHATSAPP
        numero_whatsapp = "5585988096429"  
        
        texto_mensagem = (
            f"Olá Convergência Política, acabei de realizar o Diagnóstico MAPI para a cidade de {cidade}.\n"
            f"Meu resultado foi: *{perfil}*.\n"
            f"Gostaria de agendar minha consultoria de ODS!"
        )
        
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={texto_mensagem.replace(' ', '%20')}"
        
        st.link_button("CLIQUE AQUI PARA AGENDAR SUA CONSULTORIA DOS ODS", link_whatsapp)