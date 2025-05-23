import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Inicializar sessão
if 'current_page' not in st.session_state:
    st.session_state.current_page = "welcome"
    st.session_state.financial_data_submitted = False
    st.session_state.questionnaire_completed = False
    st.session_state.financial_data = {
        "income": {
            "salary": 0,
            "investments": 0,
            "other": 0,
            "total": 0
        },
        "expenses": {
            "housing": 0,
            "food": 0,
            "transportation": 0,
            "utilities": 0,
            "leisure": 0,
            "other": 0,
            "total": 0
        },
        "assets": {
            "savings": 0,
            "investments": 0,
            "real_estate": 0,
            "other": 0,
            "total": 0
        },
        "debts": {
            "credit_card": 0,
            "credit_card_rate": 0,
            "loans": 0,
            "loans_rate": 0,
            "other": 0,
            "other_rate": 0,
            "total": 0
        }
    }
    st.session_state.question_responses = {}

# Configuração da página
st.set_page_config(
    page_title="Análise Financeira Pessoal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Carregar CSS personalizado
def load_css():
    with open("static/css/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css()
except Exception as e:
    st.warning(f"Não foi possível carregar o CSS: {e}")

# Importar páginas
from app.pages.welcome import show as show_welcome
from app.pages.onboarding import show as show_onboarding
from app.pages.financial_input import show as show_financial_input
from app.pages.questionnaire import show as show_questionnaire
from app.pages.dashboard import show as show_dashboard
from app.pages.payment import show as show_payment
from app.pages.reports import show as show_reports

# Roteamento de páginas
def route():
    if st.session_state.current_page == "welcome":
        show_welcome()
    elif st.session_state.current_page == "onboarding":
        show_onboarding()
    elif st.session_state.current_page == "financial_input":
        show_financial_input()
    elif st.session_state.current_page == "questionnaire":
        show_questionnaire()
    elif st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "payment":
        show_payment()
    elif st.session_state.current_page == "reports":
        show_reports()
    else:
        show_welcome()

# Executar a aplicação
if __name__ == "__main__":
    route()
