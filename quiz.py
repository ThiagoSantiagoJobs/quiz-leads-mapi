import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# Configuração visual da página (Modo Escuro / Premium focado em conversão)
st.set_page_config(page_title="Diagnóstico MAPI - Inteligência Política", page_icon="🧩", layout="centered")

st.title("Seu posicionamento político está preparado para a nova era?")
st.markdown("### Descubra se sua pré-campanha transmite autoridade e conexão real através dos ODS.")
st.write("---")

# Estabelecendo a conexão segura com o Google Sheets através do secrets.toml (ttl=0 limpa o cache)
conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# Formulário de Captura (Leads Qualificados para sua análise de dados)
with st.form("quiz_attraction"):
    st.subheader("📋 Informações Estratégicas")
    nome = st.text_input("Seu Nome / Nome do Pré-Candidato *")
    whatsapp = st.text_input("WhatsApp de Contato (com DDD) *")
    email = st.text_input("Seu melhor E-mail *")
    instagram = st.text_input("Qual o seu @ do Instagram? (Ex: @seu_perfil) *")
    cidade = st.text_input("Cidade / Estado de Atuação *")
    cargo = st.selectbox("Cargo Pretendido em 2026 *", [
        "Deputado Estadual", 
        "Deputado Federal", 
        "Majoritária (Senado/Governo/Vice)", 
        "Assessor / Coordenador de Campanha"
    ])
    
    st.write("---")
    
    # Inicializando pontuações por bloco
    score_pos = 0
    score_aut = 0
    score_imp = 0
    
    # 🔵 BLOCO 1 — POSICIONAMENTO
    st.subheader("🔵 BLOCO 1 — POSICIONAMENTO (A Base da Narrativa)")
    
    q1 = st.radio("1. Você consegue resumir claramente a principal causa que defende?", 
                  ["Sim, com total clareza", "Mais ou menos, mudo o foco às vezes", "Ainda não defini um nicho claro"])
    
    q2 = st.radio("2. Seu posicionamento político está conectado a algum impacto social específico e mensurável?", 
                  ["Sim, minhas pautas são baseadas em indicadores reais", "Parcialmente, defendo causas gerais (ex: saúde/educação)", "Não, foco em críticas ou propostas genéricas"])
    
    q3 = st.radio("3. O eleitor comum entende facilmente: 'Por que votar em você e não no seu adversário?'", 
                  ["Sim, meu diferencial é nítido", "Às vezes sinto que me confundem com outros candidatos", "Não, ainda preciso desenhar essa differentiation"])
    
    q4 = st.radio("4. Você possui uma narrativa política estruturada (Storytelling de Campanha)?", 
                  ["Sim, tenho meu 'porquê', minha história e bandeiras alinhadas", "Parcialmente, tenho ideias soltas sem linha condutora", "Não tenho uma narrativa definida ainda"])
    
    # Lógica de cálculo Bloco 1
    score_pos += 3 if q1 == "Sim, com total clareza" else (2 if q1 == "Mais ou menos, mudo o foco às vezes" else 1)
    score_pos += 3 if q2 == "Sim, minhas pautas são baseadas em indicadores reais" else (2 if q2 == "Parcialmente, defendo causas gerais (ex: saúde/educação)" else 1)
    score_pos += 3 if q3 == "Sim, meu diferencial é nítido" else (2 if q3 == "Às vezes sinto que me confundem com outros candidatos" else 1)
    score_pos += 3 if q4 == "Sim, tenho meu 'porquê', minha história e bandeiras alinhadas" else (2 if q4 == "Parcialmente, tenho ideias soltas sem linha condutora" else 1)
    
    st.write("---")
    
    # 🟡 BLOCO 2 — AUTORIDADE E COMUNICAÇÃO
    st.subheader("🟡 BLOCO 2 — AUTORIDADE E COMUNICAÇÃO (A Percepção Pública)")
    
    q5 = st.radio("5. Hoje, olhando para as suas redes e discursos, sua comunicação gera Autoridade, Identificação e Confiança imediata?", 
                  ["Sim, o retorno do público valida isso", "Em partes, gera engajamento (likes), mas não sinto autoridade política", "Ainda não consegui passar essa imagem"])
    
    q6 = st.radio("6. Você possui uma mensagem-chave forte e consistente que repete em todos os canais?", 
                  ["Sim, minha equipe e eu falamos a mesma língua", "Parcialmente, a mensagem muda dependendo da semana", "Não, atiro para todos os lados para ver o que engaja"])
    
    q7 = st.radio("7. Seu conteúdo nas redes sociais possui estratégia de dados ou apenas frequência de postagens?", 
                  ["Estratégia clara: cada post atende a uma dor ou meta de imagem", "Um pouco dos dois: a rotina vira um 'apaga incêndio'", "Apenas postagem: agendas, fotos de reuniões e parabéns à cidade"])
    
    q8 = st.radio("8. Seu posicionamento atual diferencia você visualmente e conceitualmente dos seus concorrentes diretos?", 
                  ["Sim, nossa identidade e discurso são únicos", "Parcialmente, mas a estética e temas parecem o padrão político", "Não, se trocar a foto o conteúdo parece o mesmo"])
    
    # Lógica de cálculo Bloco 2
    score_aut += 3 if q5 == "Sim, o retorno do público valida isso" else (2 if q5 == "Em partes, gera engajamento (likes), mas não sinto autoridade política" else 1)
    score_aut += 3 if q6 == "Sim, minha equipe e eu falamos a mesma língua" else (2 if q6 == "Parcialmente, a mensagem muda dependendo da semana" else 1)
    score_aut += 3 if q7 == "Estratégia clara: cada post atende a uma dor ou meta de imagem" else (2 if q7 == "Um pouco dos dois: a rotina vira um 'apaga incêndio'" else 1)
    score_aut += 3 if q8 == "Sim, nossa identidade e discurso são únicos" else (2 if q8 == "Parcialmente, mas a estética e temas parecem o padrão político" else 1)
    
    st.write("---")
    
    # 🔴 BLOCO 3 — IMPACTO E LEGADO (Fator ODS)
    st.subheader("🔴 BLOCO 3 — IMPACTO E LEGADO (O Fator ODS)")
    
    q9 = st.radio("9. Você consegue provar e mensurar (com dados e indicadores) o impacto real das suas ações ou propostas?", 
                  ["Sim, uso dados públicos e estatísticas para embasar o que faço/proponho", "Parcialmente, sei de forma intuitiva, mas sem dados para provar", "Não, minhas propostas são totalmente conceituais"])
    
    q10 = st.radio("10. Suas propostas de mandato ou planos de governo possuem conexão direta com as metas dos ODS (Agenda 2030 da ONU)?", 
                   ["Sim, mapeamos nossos projetos dentro dos Objetivos globais", "Algumas propostas batem por configuração, mas sem plano intencional", "Não adotamos os ODS na nossa linha de discurso ainda"])
    
    q11 = st.radio("11. Você acredita que hoje sua imagem pública transmite Legado, Liderança e Preparo Técnico?", 
                   ["Sim, sou visto como um quadro preparado e pronto para o cargo", "Parcialmente, me acham esforçado, mas falta imagem de gestor/estadista", "Não, sinto que me veem apenas como mais um candidato"])
    
    q12 = st.radio("12. Sua pré-campanha está construindo Reconhecimento Real ou apenas Visibilidade Passageira?", 
                   ["Reconhecimento: o eleitor lembra de mim pelo que eu defendo", "Ambos: tenho picos de views, mas oscilo na fixação da mensagem", "Apenas visibilidade: muitos veem posts/santinhos,amp; poucos sabem as propostas"])
    
    # Lógica de cálculo Bloco 3
    score_imp += 3 if q9 == "Sim, uso dados públicos e estatísticas para embasar o que faço/proponho" else (2 if q9 == "Parcialmente, sei de forma intuitiva, mas sem dados para provar" else 1)
    score_imp += 3 if q10 == "Sim, mapeamos nossos projetos dentro dos Objetivos globais" else (2 if q10 == "Algumas propostas batem por configuração, mas sem plano intencional" else 1)
    score_imp += 3 if q11 == "Sim, sou visto como um quadro preparado e pronto para o cargo" else (2 if q11 == "Parcialmente, me acham esforçado, mas falta imagem de gestor/estadista" else 1)
    score_imp += 3 if q12 == "Reconhecimento: o eleitor lembra de mim pelo que eu defendo" else (2 if q12 == "Ambos: tenho picos de views, mas oscilo na fixação da mensagem" else 1)
    
    st.write("---")
    
    # Botão de Envio
    enviar = st.form_submit_button("🔥 GERAR MEU DIAGNÓSTICO DE AUTORIDADE")

# Processamento após o clique
if enviar:
    # 🛡️ VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS
    if not nome or not whatsapp or not cidade or not email or not instagram:
        st.error("⚠️ Por favor, preencha TODOS os campos do cabeçalho (Nome, WhatsApp, E-mail, Instagram e Cidade) para gerar o relatório.")
    else:
        score_total = score_pos + score_aut + score_imp
        
        # Criando o dicionário com a nova linha de dados
        nova_linha = {
            "Data_Hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nome": nome,
            "WhatsApp": whatsapp,
            "E-mail": email,
            "Instagram": instagram,
            "Cidade": cidade,
            "Cargo": cargo,
            "Score_Posicionamento": int(score_pos),
            "Score_Autoridade": int(score_aut),
            "Score_Impacto_ODS": int(score_imp),
            "Total_Score": int(score_total)
        }
        
        try:
            # Busca os dados atuais existindo no Google Sheets forçando ttl=0
            dados_existentes = conn.read(worksheet="Página1", ttl=0)
            df_atual = pd.DataFrame(dados_existentes)
        except Exception:
            # Caso a planilha esteja 100% vazia
            df_atual = pd.DataFrame()
            
        # Adiciona a nova linha ao DataFrame
        df_novo = pd.DataFrame([nova_linha])
        df_final = pd.concat([df_atual, df_novo], ignore_index=True)
        
        # Faz o upload da tabela atualizada de volta para o Google Sheets em tempo real
        conn.update(worksheet="Página1", data=df_final)
        
        st.success("✅ Diagnóstico Estratégico Concluído com Sucesso!")
        st.write(f"### Raio-X de Performance Política - Pré-Campanha de {nome}")
        
        # Exibição do Perfil DIRETO EM TEXTO
        st.write("### 🧠 Avaliação de Perfil")
        
        if score_total <= 20:
            st.subheader("🔥 Perfil 1 — Candidatura Invisível")
            st.markdown("> **“Você ainda não construiu um posicionamento forte.”**\n\nSeu desafio hoje não é aparecer mais ou investir massivamente em tráfego de internet. É gerar clareza, autoridade e diferenciação. Sem estruturar sua narrativa de dados, seu discurso corre o risco de passar despercebido pelo eleitor moderno.")
        elif score_total <= 30:
            st.subheader("🔥 Perfil 2 — Comunicador em Construção")
            st.markdown("> **“Você já possui presença, mas falta estrutura estratégica.”**\n\nSua comunicação existe e as pessoas te ouvem, mas falta a engrenagem que transforma relevância em voto garantido. Sua pré-campanha precisa urgentemente de uma narrativa amarrada, consistência visual e um impacto social baseado em dados e ODS.")
        else:
            st.subheader("🔥 Perfil 3 — Liderança Estratégica")
            st.markdown("> **“Sua pré-campanha já demonstra posicionamento e potencial de autoridade.”**\n\nParabéns! Você está acima da média do mercado político tradicional. Agora o foco deve ser a blindagem do seu legado e a escala de imagem: consolidar sua reputação técnica através dos ODS e converter essa percepção de alto nível em liderança consolidada.")
            
        st.write("---")
        st.subheader("📥 Como interpretar esses indicadores e aplicar na sua cidade?")
        st.write("O próximo passo é entender quais ODS específicos o seu município necessita para criarmos uma linha de discurso técnica, inatacável e atraente para o eleitorado.")
        
        # CONFIGURAÇÃO DO WHATSAPP
        seu_numero = "5585988096429" 
        texto_mensagem = f"Olá Convergência Política, acabei de realizar o Diagnóstico MAPI para o cargo de {cargo} em {cidade}. Minha pontuação final foi de {score_total} pontos. Quero agendar uma apresentação do meu Raio-X dos ODS."
        
        link_whatsapp = f"https://wa.me/{seu_numero}?text={texto_mensagem.replace(' ', '%20')}"
        st.link_button("💬 CLIQUE AQUI PARA AGENDAR SUA CONSULTORIA DOS ODS", link_whatsapp)