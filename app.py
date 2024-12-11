import os
import json
import streamlit as st
from groq import Groq


# Cria instância do cliente Groq
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.set_page_config(page_title="Veloso e Almeida - Serviços Acadêmicos", page_icon=":mortar_board:")

# CSS customizado para aplicar as cores da identidade visual e ajustar o campo de entrada
st.markdown("""
<style>
    /* Ajusta o fundo da página principal */
    .main, .block-container {
        background-color: #003f3f; /* Verde escuro */
        color: #ffffff; /* Texto branco */
    }
    
    /* Ajusta a barra lateral */
    .css-1cypcdb.e1fqkh3o3, .css-1cypcdb.e1fqkh3o1 {
        background-color: #003f3f !important;
        color: #ffffff !important;
    }
    
    /* Títulos em dourado */
    h1, h2, h3, h4, h5, h6 {
        color: #D4AF37; /* Dourado */
    }

    /* Mensagem do usuário */
    .stChatMessage.user {
        background-color: #D4AF37 !important; /* Dourado */
        color: #003f3f !important; /* Texto em verde escuro */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Mensagem do assistente */
    .stChatMessage.assistant {
        background-color: #ffffff !important; /* Fundo branco */
        color: #000000 !important; /* Texto preto */
        border: 1px solid #D4AF37; /* Borda dourada */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Campo de entrada do chat */
    .stChatInput {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #D4AF37;
        border-radius: 5px;
    }

    /* Ajuste adicional para o textarea interno do st.chat_input, garantindo visibilidade do texto */
    .stChatInput textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .stChatInput textarea::placeholder {
        color: #000000 !important;
    }

    /* Ajusta rótulos, textos secundários etc. */
    .css-1offfwp p, .css-1vgnld6 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Exibe o logo na barra lateral
st.sidebar.image("logoo-removebg-preview.png", use_container_width=True)

st.sidebar.markdown("### Veloso e Almeida - Serviços Acadêmicos")
st.sidebar.markdown("**Consultoria acadêmica, mentoria, escrita acadêmica e serviços educacionais.**")

# Seleção do tipo de serviço
servico_escolhido = st.sidebar.selectbox(
    "Selecione o tipo de serviço:",
    [
        "Consultoria em Escrita Acadêmica",
        "Mentoria sobre Publicação Científica",
        "Apoio em Metodologia de Pesquisa",
        "Formatação e Normas Acadêmicas"
    ]
)

st.title("Bem-vindo à Plataforma de Consultoria Acadêmica")
st.markdown("""
Esta aplicação utiliza modelos da API da Groq para auxiliar em diversas etapas do trabalho acadêmico.
Selecione um serviço na barra lateral e faça suas perguntas no campo abaixo.
""")

if servico_escolhido == "Consultoria em Escrita Acadêmica":
    acao = "Forneça sugestões detalhadas de aprimoramento na escrita acadêmica."
elif servico_escolhido == "Mentoria sobre Publicação Científica":
    acao = "Forneça orientação sobre os próximos passos para publicação, possíveis revistas científicas adequadas e dicas para melhorar a probabilidade de aceitação."
elif servico_escolhido == "Apoio em Metodologia de Pesquisa":
    acao = "Forneça orientação metodológica sólida, sugestões de desenhos de pesquisa, técnicas analíticas e referências."
else:
    acao = "Explique as normas, a formatação e dê exemplos claros."

# Botão para iniciar nova conversa
if st.sidebar.button("Nova Conversa"):
    if "messages" in st.session_state:
        del st.session_state["messages"]

# Inicializa a sessão de conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"Você é um consultor acadêmico sênior da empresa 'Veloso e Almeida - Serviços Acadêmicos', especialista em orientação, mentoria, escrita e serviços educacionais no âmbito acadêmico. {acao}"
        }
    ]

# Exibe as mensagens já existentes
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    elif msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# Campo de entrada no estilo chat
user_input = st.chat_input("Digite sua pergunta ou mensagem...")

if user_input:
    # Adiciona a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Chamada ao modelo da Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=st.session_state.messages,
        )
        resposta = response.choices[0].message.content.strip()
    except Exception as e:
        resposta = f"Erro ao obter resposta da API: {e}"

    # Adiciona resposta do assistente
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.write(resposta)

# Adiciona um botão de download da conversa
if st.session_state.messages:
    conversation_json = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
    st.download_button(
        label="Baixar Conversa",
        data=conversation_json,
        file_name="conversa.json",
        mime="application/json"
    )
