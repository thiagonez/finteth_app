import streamlit as st
import stripe
from components.navigation import navigation_buttons
from config import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY

# Configurar Stripe
stripe.api_key = STRIPE_SECRET_KEY

def show():
    """Página de pagamento para acesso a relatórios premium"""
    
    st.markdown("<h1>Relatórios Premium</h1>", unsafe_allow_html=True)
    
    # Verificar se o usuário já é premium
    if st.session_state.get("premium_user", False):
        st.success("Você já possui acesso aos relatórios premium!")
        
        # Botão para ver relatórios
        if st.button("Ver Meus Relatórios Premium"):
            st.session_state.current_page = "reports"
            st.experimental_rerun()
        
        return
    
    # Exibir informações sobre os relatórios premium
    st.markdown("""
    <div class="premium-info">
        <h2>Desbloqueie Análises Avançadas e Personalizadas</h2>
        <p>Nossos relatórios premium oferecem uma análise completa e personalizada da sua situação financeira 
        e comportamental, com recomendações específicas para melhorar sua saúde financeira.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Comparativo entre planos
    st.markdown("<h3>Comparativo de Planos</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="plan-card free">
            <h4>Plano Gratuito</h4>
            <div class="price">R$ 0</div>
            <ul>
                <li>Perfil de Comportamento com o Dinheiro (Básico)</li>
                <li>Relatório Financeiro Objetivo (Versão Básica)</li>
                <li>Visão Geral e Saúde Financeira (Versão Básica)</li>
                <li>Dashboard Resumido</li>
                <li>Recomendações Gerais</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="plan-card premium">
            <h4>Plano Premium</h4>
            <div class="price">R$ 50</div>
            <ul>
                <li>Todos os recursos do plano gratuito</li>
                <li>Relatório Financeiro Objetivo (Completo)</li>
                <li>Visão Geral e Saúde Financeira (Completa)</li>
                <li>Relatório Psicológico Completo</li>
                <li>Relatório Integrado e Perfil Comportamental</li>
                <li>Simulador de Cenários</li>
                <li>Sistema de Recomendações Híbridas</li>
                <li>Avaliação de Sonhos e Objetivos</li>
                <li>SWOT Financeira</li>
                <li>Planejamento Estratégico e Plano de Ação</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Formulário de pagamento
    st.markdown("<h3>Adquirir Plano Premium</h3>", unsafe_allow_html=True)
    
    # Informações de pagamento
    with st.form("payment_form"):
        st.markdown("<p>Preencha os dados abaixo para adquirir o plano premium:</p>", unsafe_allow_html=True)
        
        # Nome no cartão
        card_name = st.text_input("Nome no Cartão")
        
        # Informações do cartão
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Número do Cartão", placeholder="4242 4242 4242 4242")
        with col2:
            card_expiry = st.text_input("Validade (MM/AA)", placeholder="12/25")
        
        col1, col2 = st.columns(2)
        with col1:
            card_cvc = st.text_input("CVC", placeholder="123")
        with col2:
            card_zip = st.text_input("CEP", placeholder="12345-678")
        
        # Termos e condições
        terms = st.checkbox("Concordo com os termos e condições")
        
        # Botão de pagamento
        submitted = st.form_submit_button("Pagar R$ 50,00")
        
        if submitted:
            if not card_name or not card_number or not card_expiry or not card_cvc or not card_zip:
                st.error("Por favor, preencha todos os campos.")
            elif not terms:
                st.error("Você precisa concordar com os termos e condições.")
            else:
                # Simulação de processamento de pagamento
                # Em um ambiente real, aqui seria integrado com o Stripe
                with st.spinner("Processando pagamento..."):
                    # Simulação de processamento
                    import time
                    time.sleep(2)
                    
                    # Simular sucesso no pagamento
                    st.session_state.premium_user = True
                    st.success("Pagamento realizado com sucesso! Você agora tem acesso aos relatórios premium.")
                    
                    # Botão para ver relatórios
                    if st.button("Ver Meus Relatórios Premium"):
                        st.session_state.current_page = "reports"
                        st.experimental_rerun()
    
    # Informações de segurança
    st.markdown("""
    <div class="security-info">
        <h4>Pagamento 100% Seguro</h4>
        <p>Seus dados de pagamento são processados com segurança pela plataforma Stripe, 
        líder global em processamento de pagamentos online.</p>
        <p>Todos os dados são criptografados e protegidos pelos mais altos padrões de segurança.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Política de reembolso
    st.markdown("""
    <div class="refund-policy">
        <h4>Política de Reembolso</h4>
        <p>Oferecemos garantia de satisfação de 30 dias. Se você não estiver satisfeito com os relatórios premium, 
        entre em contato conosco para solicitar um reembolso integral.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegação
    navigation_buttons(prev_page="dashboard", next_page="reports" if st.session_state.get("premium_user", False) else None)
