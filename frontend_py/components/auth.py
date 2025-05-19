import streamlit as st
from streamlit_oauth import OAuth2Component

def login_with_google():
    """
    Handles Google OAuth2 login using streamlit-oauth package.
    Returns the token if authenticated, None otherwise.
    """
    client_id = st.secrets["client_id"]
    client_secret = st.secrets["client_secret"]
    redirect_uri = st.secrets["redirect_uri"]

    oauth2 = OAuth2Component(
        client_id=client_id,
        client_secret=client_secret,
        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        # redirect_uri=redirect_uri,
        
    )

    token = oauth2.authorize_button(
        "Login com Google",
        "Você está logado!",
        "Erro ao logar"
    )
    return token

def get_credentials():
    """
    Returns Google OAuth2.0 credentials (token dict) from session state.
    """
    return st.session_state.get('token', None)


def check_authentication() -> bool:
    """
    Checks if user is authenticated via Google OAuth2.0 using streamlit-oauth.
    Returns True if authenticated, False otherwise.
    """
    if not get_credentials():
        token = login_with_google()
        if token and "access_token" in token:
            st.session_state['token'] = token
            return True
        else:
            return False
    else:
        return True


