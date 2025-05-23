import streamlit as st
from app.components.navigation import navigation_buttons

def show():
    """Página de boas-vindas"""
    
    st.markdown("<h1 class='main-title'>Análise Financeira Pessoal</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-container">
        <p class="welcome-text">
            Bem-vindo à sua jornada de autoconhecimento financeiro! Esta ferramenta foi desenvolvida para ajudar você a 
            entender melhor sua relação com o dinheiro, analisar sua situação financeira atual e receber recomendações 
            personalizadas para melhorar sua saúde financeira.
        </p>
        
        <h2>Como funciona?</h2>
        
        <div class="steps-container">
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>Forneça seus dados financeiros</h3>
                    <p>Insira informações sobre suas receitas, despesas, ativos e dívidas. Você pode inserir manualmente ou importar de arquivos.</p>
                </div>
            </div>
            
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>Responda ao questionário comportamental</h3>
                    <p>Um conjunto de perguntas para entender sua relação psicológica com o dinheiro e seus hábitos financeiros.</p>
                </div>
            </div>
            
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>Receba análises personalizadas</h3>
                    <p>Visualize dashboards interativos e relatórios detalhados sobre sua saúde financeira e comportamental.</p>
                </div>
            </div>
            
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h3>Obtenha recomendações</h3>
                    <p>Receba um plano de ação personalizado com estratégias específicas para melhorar sua situação financeira.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='center-content'>", unsafe_allow_html=True)
    if st.button("Começar Agora", key="start_button"):
        st.session_state.current_page = "onboarding"
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Informações adicionais
    with st.expander("Sobre esta ferramenta"):
        st.markdown("""
        Esta ferramenta de análise financeira pessoal foi desenvolvida para ajudar indivíduos e casais a 
        compreenderem melhor sua situação financeira e comportamental. Combinando análises objetivas de dados 
        financeiros com insights psicológicos sobre sua relação com o dinheiro, oferecemos uma visão holística 
        da sua saúde financeira.
        
        **Recursos principais:**
        - Importação e análise de dados financeiros
        - Questionário comportamental adaptativo
        - Dashboard interativo com visualizações personalizadas
        - Relatórios detalhados com recomendações específicas
        - Plano de ação personalizado
        
        **Privacidade e segurança:**
        Seus dados são processados localmente e não são compartilhados com terceiros. 
        Utilizamos as melhores práticas de segurança para proteger suas informações.
        """)
    
    # Navegação (apenas próximo)
    navigation_buttons(prev_page=None, next_page="onboarding")
