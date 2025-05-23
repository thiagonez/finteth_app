import streamlit as st
from components.navigation import navigation_buttons

def show():
    """Página de boas-vindas"""

    st.markdown("""
    <style>
        .steps-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 24px;
        }
        .step-card {
            border: 1px solid #eee;
            padding: 16px;
            border-radius: 8px;
            background: #fafafa;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            margin-bottom: 8px;
        }
        .step-number {
            font-size: 2em;
            font-weight: bold;
            color: #4F8BF9;
            margin-bottom: 8px;
        }
        .step-content h3 {
            margin: 0 0 4px 0;
        }
    </style>

    <h1>Análise Financeira Pessoal</h1>
    <p>
    Bem-vindo à sua jornada de autoconhecimento financeiro! Esta ferramenta foi desenvolvida para ajudar você a entender melhor sua relação com o dinheiro, analisar sua situação financeira atual e receber recomendações personalizadas para melhorar sua saúde financeira.
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
    """, unsafe_allow_html=True)

    navigation_buttons()
