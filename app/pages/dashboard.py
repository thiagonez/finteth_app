import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from components.navigation import navigation_buttons

def show():
    """Página de dashboard com visualizações financeiras e comportamentais"""
    
    st.markdown("<h1>Seu Dashboard Financeiro</h1>", unsafe_allow_html=True)
    
    # Verificar se os dados necessários estão disponíveis
    if not st.session_state.financial_data_submitted or not st.session_state.questionnaire_completed:
        st.warning("Por favor, complete o questionário financeiro e comportamental para visualizar seu dashboard.")
        
        # Botão para voltar
        if st.button("Voltar para o Questionário"):
            if not st.session_state.financial_data_submitted:
                st.session_state.current_page = "financial_input"
            else:
                st.session_state.current_page = "questionnaire"
            st.rerun()
        
        return
    
    # Obter dados financeiros
    financial_data = st.session_state.financial_data
    
    # Obter perfil comportamental
    from pages.questionnaire import calculate_profile
    profile_scores = calculate_profile(st.session_state.question_responses)
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise Financeira", "Perfil Comportamental"])
    
    with tab1:
        st.markdown("<h2>Visão Geral da Sua Saúde Financeira</h2>", unsafe_allow_html=True)
        
        # Calcular métricas principais
        income_total = financial_data["income"]["total"]
        expenses_total = financial_data["expenses"]["total"]
        balance = income_total - expenses_total
        assets_total = financial_data["assets"]["total"]
        debts_total = financial_data["debts"]["total"]
        net_worth = assets_total - debts_total
        
        # Exibir métricas em cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card">
                <h3>Fluxo de Caixa Mensal</h3>
                <div class="metric-container">
                    <div class="metric-value">R$ {:.2f}</div>
                    <div class="metric-label">Saldo</div>
                </div>
                <div class="metric-details">
                    <div>Receitas: R$ {:.2f}</div>
                    <div>Despesas: R$ {:.2f}</div>
                </div>
            </div>
            """.format(balance, income_total, expenses_total), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>Patrimônio Líquido</h3>
                <div class="metric-container">
                    <div class="metric-value">R$ {:.2f}</div>
                    <div class="metric-label">Valor Total</div>
                </div>
                <div class="metric-details">
                    <div>Ativos: R$ {:.2f}</div>
                    <div>Dívidas: R$ {:.2f}</div>
                </div>
            </div>
            """.format(net_worth, assets_total, debts_total), unsafe_allow_html=True)
        
        # Calcular taxa de poupança
        savings_rate = (balance / income_total) * 100 if income_total > 0 else 0
        
        # Calcular índice de endividamento
        debt_to_income = (debts_total / (income_total * 12)) * 100 if income_total > 0 else 0
        
        # Calcular índice de bem-estar financeiro (simplificado para o MVP)
        financial_wellbeing = 0
        
        # Fatores positivos
        if savings_rate >= 20:
            financial_wellbeing += 30
        elif savings_rate >= 10:
            financial_wellbeing += 20
        elif savings_rate > 0:
            financial_wellbeing += 10
        
        # Fatores negativos
        if debt_to_income > 40:
            financial_wellbeing -= 30
        elif debt_to_income > 20:
            financial_wellbeing -= 15
        
        # Ajustar para escala 0-100
        financial_wellbeing = max(0, min(100, financial_wellbeing + 50))
        
        # Exibir índice de bem-estar financeiro
        st.markdown("<h3>Índice de Bem-Estar Financeiro</h3>", unsafe_allow_html=True)
        
        # Criar gráfico de medidor
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = financial_wellbeing,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Bem-Estar Financeiro"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#5a67d8"},
                'steps': [
                    {'range': [0, 30], 'color': "#fc8181"},
                    {'range': [30, 70], 'color': "#f6ad55"},
                    {'range': [70, 100], 'color': "#48bb78"}
                ]
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretação do índice
        if financial_wellbeing >= 70:
            interpretation = """
            <div class="interpretation good">
                <h4>Boa Saúde Financeira</h4>
                <p>Você está no caminho certo! Sua taxa de poupança e baixo endividamento contribuem para um bom índice de bem-estar financeiro.</p>
            </div>
            """
        elif financial_wellbeing >= 30:
            interpretation = """
            <div class="interpretation moderate">
                <h4>Saúde Financeira Moderada</h4>
                <p>Há espaço para melhorias. Considere aumentar sua taxa de poupança ou reduzir dívidas para melhorar seu bem-estar financeiro.</p>
            </div>
            """
        else:
            interpretation = """
            <div class="interpretation poor">
                <h4>Saúde Financeira em Risco</h4>
                <p>Seu índice de bem-estar financeiro está baixo. Foque em reduzir dívidas e aumentar sua taxa de poupança.</p>
            </div>
            """
        
        st.markdown(interpretation, unsafe_allow_html=True)
        
        # Botão para ver relatório completo (versão premium)
        st.markdown("<div class='center-content'>", unsafe_allow_html=True)
        if st.button("Ver Relatório Completo (Premium)"):
            st.session_state.current_page = "payment"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h2>Análise Financeira Detalhada</h2>", unsafe_allow_html=True)
        
        # Gráfico de receitas vs despesas
        st.markdown("<h3>Receitas vs Despesas</h3>", unsafe_allow_html=True)
        
        # Criar dados para o gráfico
        categories = ['Receitas', 'Despesas']
        values = [income_total, expenses_total]
        
        # Criar gráfico de barras
        fig = px.bar(
            x=categories, 
            y=values,
            color=categories,
            color_discrete_map={'Receitas': '#48bb78', 'Despesas': '#fc8181'},
            labels={'x': 'Categoria', 'y': 'Valor (R$)'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de distribuição de despesas
        st.markdown("<h3>Distribuição de Despesas</h3>", unsafe_allow_html=True)
        
        # Criar dados para o gráfico
        expenses = financial_data["expenses"]
        expense_categories = ["Moradia", "Alimentação", "Transporte", "Contas", "Lazer", "Outros"]
        expense_values = [
            expenses["housing"], 
            expenses["food"], 
            expenses["transportation"], 
            expenses["utilities"], 
            expenses["leisure"], 
            expenses["other"]
        ]
        
        # Filtrar categorias com valores
        filtered_categories = []
        filtered_values = []
        for i, value in enumerate(expense_values):
            if value > 0:
                filtered_categories.append(expense_categories[i])
                filtered_values.append(value)
        
        # Criar gráfico de pizza
        if filtered_values:
            fig = px.pie(
                names=filtered_categories,
                values=filtered_values,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados de despesas para exibir.")
        
        # Análise de dívidas
        st.markdown("<h3>Análise de Dívidas</h3>", unsafe_allow_html=True)
        
        debts = financial_data["debts"]
        debt_categories = ["Cartão de Crédito", "Empréstimos", "Outros"]
        debt_values = [debts["credit_card"], debts["loans"], debts["other"]]
        debt_rates = [debts["credit_card_rate"], debts["loans_rate"], debts["other_rate"]]
        
        # Criar dataframe para tabela
        debt_df = pd.DataFrame({
            "Tipo de Dívida": debt_categories,
            "Valor (R$)": debt_values,
            "Taxa de Juros (%)": debt_rates,
            "Juros Mensais (R$)": [v * r / 100 for v, r in zip(debt_values, debt_rates)]
        })
        
        # Filtrar dívidas com valores
        debt_df = debt_df[debt_df["Valor (R$)"] > 0]
        
        if not debt_df.empty:
            st.dataframe(debt_df, use_container_width=True)
            
            # Calcular juros totais
            total_interest = debt_df["Juros Mensais (R$)"].sum()
            
            st.markdown(f"""
            <div class="alert">
                <p>Você paga aproximadamente <strong>R$ {total_interest:.2f}</strong> em juros mensalmente.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Não há dados de dívidas para exibir.")
    
    with tab3:
        st.markdown("<h2>Seu Perfil Comportamental</h2>", unsafe_allow_html=True)
        
        # Gráfico de perfil comportamental
        fig, ax = plt.subplots(figsize=(10, 6))
        profiles = list(profile_scores.keys())
        scores = list(profile_scores.values())
        
        ax.bar(profiles, scores, color=['#5a67d8', '#38b2ac', '#f6ad55', '#fc8181'])
        ax.set_ylabel('Pontuação (%)')
        ax.set_title('Seu Perfil de Comportamento com o Dinheiro')
        
        # Rotacionar rótulos do eixo x para melhor visualização
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Exibir gráfico
        st.pyplot(fig)
        
        # Identificar perfil dominante
        dominant_profile = max(profile_scores.items(), key=lambda x: x[1])
        
        # Descrições dos perfis
        profile_descriptions = {
            "evitador": """
            <div class="profile-card">
                <h3>Perfil Evitador</h3>
                <p>Você tende a evitar lidar com questões financeiras, possivelmente por ansiedade ou desconforto. 
                Pode adiar decisões financeiras importantes e ter dificuldade em estabelecer metas claras.</p>
                <h4>Pontos Fortes:</h4>
                <p>Menos propenso a tomar riscos financeiros impulsivos.</p>
                <h4>Desafios:</h4>
                <p>Pode perder oportunidades por hesitação e ter dificuldade em planejar o futuro financeiro.</p>
            </div>
            """,
            
            "apegado": """
            <div class="profile-card">
                <h3>Perfil Apegado</h3>
                <p>Você tende a ser muito cauteloso com dinheiro, priorizando segurança e estabilidade. 
                Pode ter dificuldade em gastar, mesmo quando necessário, e focar excessivamente em economizar.</p>
                <h4>Pontos Fortes:</h4>
                <p>Disciplina para poupar e resistência a gastos impulsivos.</p>
                <h4>Desafios:</h4>
                <p>Pode ter dificuldade em desfrutar do dinheiro e sentir ansiedade ao gastar.</p>
            </div>
            """,
            
            "ostentador": """
            <div class="profile-card">
                <h3>Perfil Ostentador</h3>
                <p>Você tende a usar o dinheiro como forma de expressão social e status. 
                Pode priorizar gastos visíveis e ter dificuldade em resistir a compras que impressionem os outros.</p>
                <h4>Pontos Fortes:</h4>
                <p>Generosidade e capacidade de aproveitar experiências.</p>
                <h4>Desafios:</h4>
                <p>Tendência a gastar além do necessário e dificuldade em poupar consistentemente.</p>
            </div>
            """,
            
            "planejador": """
            <div class="profile-card">
                <h3>Perfil Planejador</h3>
                <p>Você tende a ser organizado e estratégico com suas finanças. 
                Estabelece metas claras e segue planos para alcançá-las, equilibrando necessidades atuais e futuras.</p>
                <h4>Pontos Fortes:</h4>
                <p>Disciplina financeira e capacidade de planejar a longo prazo.</p>
                <h4>Desafios:</h4>
                <p>Pode ser excessivamente rígido e ter dificuldade em adaptar-se a mudanças inesperadas.</p>
            </div>
            """
        }
        
        # Exibir descrição do perfil dominante
        st.markdown("<h3>Seu Perfil Dominante</h3>", unsafe_allow_html=True)
        st.markdown(profile_descriptions[dominant_profile[0]], unsafe_allow_html=True)
        
        # Nota sobre relatório completo
        st.markdown("""
        <div class="note">
            <p>Esta é uma análise básica do seu perfil comportamental. Para uma análise completa, 
            incluindo recomendações personalizadas e estratégias específicas para seu perfil, 
            acesse o relatório premium.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão para ver relatório completo (versão premium)
        st.markdown("<div class='center-content'>", unsafe_allow_html=True)
        if st.button("Ver Relatório Comportamental Completo (Premium)", key="premium_behavior"):
            st.session_state.current_page = "payment"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Navegação
    navigation_buttons(prev_page="questionnaire", next_page="reports")
