import streamlit as st
from components.navigation import navigation_buttons

def show():
    """Página de boas-vindas"""
    
    st.markdown("""
    <style>
        .main-title {
            color: #2F4F4F;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        .welcome-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .steps-container {
            display: grid;
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .step-card {
            background: #F8F9FA;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #4F8BF9;
        }
        
        .step-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4F8BF9;
            margin-bottom: 0.5rem;
        }
        
        .step-content h3 {
            color: #2F4F4F;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }
        
        .step-content p {
            color: #6C757D;
            line-height: 1.6;
        }
        
        .center-content {
            display: flex;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .stButton>button {
            background-color: #4F8BF9;
            color: white;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #3B6FB6;
            transform: translateY(-2px);
        }
    </style>

    <div class="welcome-container">
        <h1 class="main-title">Análise Financeira Pessoal</h1>
        
        <p style='text-align: center; color: #6C757D; line-height: 1.6;'>
            Bem-vindo à sua jornada de autoconhecimento financeiro! Esta ferramenta foi desenvolvida para ajudar você a 
            entender melhor sua relação com o dinheiro, analisar sua situação financeira atual e receber recomendações 
            personalizadas para melhorar sua saúde financeira.
        </p>
        
        <h2 style='text-align: center; margin: 2rem 0; color: #2F4F4F;'>Como funciona?</h2>
        
        <div class="steps-container">
            <!-- Step cards mantêm a mesma estrutura -->
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
        
        <div class="center-content">
    """, unsafe_allow_html=True)

    # Botão "Começar Agora" centralizado
    if st.button("Começar Agora", key="start_button"):
        st.session_state.current_page = "onboarding"
        st.rerun()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Seção expandível "Sobre esta ferramenta"
    with st.expander("Sobre esta ferramenta"):
        st.markdown("""
        **Recursos principais:**
        - Importação e análise de dados financeiros
        - Questionário comportamental adaptativo
        - Dashboard interativo com visualizações personalizadas
        - Relatórios detalhados com recomendações específicas
        - Plano de ação personalizado

        **Privacidade e segurança:**
        Seus dados são processados localmente e não são compartilhados com terceiros.
        """)

    navigation_buttons(prev_page=None, next_page="onboarding")
