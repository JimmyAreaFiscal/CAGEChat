import streamlit as st
import sys, os 
# from frontend.components.auth import check_authentication
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="RAG System Home",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

def main():
    # Authentication
    # authenticated = check_authentication()
    # if not authenticated:
       #  st.warning("Por favor, faça login com sua conta Google para acessar o sistema.")
       #  st.stop()

    # App Title and Subtitle
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #4F8BF9; margin-bottom: 0;">🧠 CAGEChat </h1>
            <h3 style="color: #555; margin-top: 0;">Seu sistema inteligente de Recuperação de Informação com IA</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Welcome Message
    st.markdown(
        """
        <div style="background-color: transparent; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; text-align: center;">
            <p style="font-size: 1.2rem;">
                Bem-vindo ao <b>Sistema CAGEChat</b>!<br>
                Este é um protótipo para integração de Inteligência Artificial e uso de Sistemas RAG para recuperação de conhecimentos do Rio Grande do Sul.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Features Section
    st.markdown("### 🚀 O que há aqui?")
    st.markdown(
        """
        <ul>
            <li><b>Chat Inteligente:</b> Faça perguntas e obtenha respostas baseadas nos documentos da CAGE inseridos anteriormente.</li>
            <li><b>Busca Avançada:</b> Encontre informações rapidamente com busca semântica, e identifique quais foram os documentos utilizados.</li>
            <li><b>Criação de Testes:</b> Redija Perguntas e Respostas que você saiba a resposta para apoiar o processo de construção desse protótipo.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # # Call to Action
    # st.markdown(
    #     """
    #     <div style="text-align: center; margin-top: 2rem;">
    #         <a href="/Upload" target="_self">
    #             <button style="background-color: #4F8BF9; color: white; border: none; border-radius: 8px; padding: 0.8rem 2rem; font-size: 1.1rem; cursor: pointer;">
    #                 📤 Fazer Upload de Documentos
    #             </button>
    #         </a>
    #         <br><br>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    # Routing to Chat page using Streamlit button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("💬 Ir para o Chat", key="go_to_chat", use_container_width=True):
            st.switch_page("pages/chat.py")

    # Footer
    st.markdown(
        """
        <hr>
        <div style="text-align: center; color: #888; font-size: 0.95rem;">
            Desenvolvido por <b>Sua Equipe de IA</b> • 2024
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
