import streamlit as st
from components.navigation import navigation_buttons

def show():
    """Página de onboarding e consentimento"""
    
    st.markdown("<h1>Bem-vindo à sua Jornada Financeira</h1>", unsafe_allow_html=True)
    
    # Formulário de consentimento
    st.markdown("<h2>Termos de Uso e Consentimento</h2>", unsafe_allow_html=True)
    
    with st.form("consent_form"):
        st.markdown("""
        Antes de começarmos, precisamos do seu consentimento para coletar e processar seus dados financeiros e comportamentais.
        
        **Como usamos seus dados:**
        - Para gerar análises financeiras personalizadas
        - Para identificar padrões comportamentais relacionados ao dinheiro
        - Para criar recomendações específicas para sua situação
        
        **Seus direitos:**
        - Seus dados são processados localmente e não são compartilhados com terceiros
        - Você pode solicitar a exclusão de seus dados a qualquer momento
        - Você pode exportar seus dados em formato aberto
        
        **Segurança:**
        - Utilizamos as melhores práticas de segurança para proteger suas informações
        - Seus dados sensíveis são armazenados de forma criptografada
        """)
        
        # Checkboxes de consentimento
        consent1 = st.checkbox("Concordo em fornecer meus dados financeiros para análise")
        consent2 = st.checkbox("Concordo em responder ao questionário comportamental")
        consent3 = st.checkbox("Entendo que posso usar esta ferramenta de forma anônima")
        
        # Botão de envio
        submitted = st.form_submit_button("Concordo e Quero Continuar")
        
        if submitted:
            if consent1 and consent2 and consent3:
                st.session_state.current_page = "financial_input"
                st.rerun()

            else:
                st.error("Por favor, concorde com todos os termos para continuar.")
    
    # Informações adicionais
    with st.expander("Por que precisamos do seu consentimento?"):
        st.markdown("""
        A análise financeira pessoal envolve dados sensíveis que revelam aspectos importantes da sua vida. 
        Levamos a sério a responsabilidade de processar esses dados e queremos garantir que você esteja 
        confortável com a forma como utilizamos essas informações.
        
        Esta ferramenta foi projetada com privacidade em mente. Seus dados são processados localmente 
        e você mantém controle total sobre eles. Não compartilhamos suas informações com terceiros 
        e não utilizamos seus dados para fins além dos descritos acima.
        """)
    
    # Navegação
    navigation_buttons(prev_page="welcome", next_page=None)
