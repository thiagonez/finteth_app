import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from components.navigation import navigation_buttons

def show():
    """Página de relatórios detalhados"""
    
    st.markdown("<h1>Seus Relatórios</h1>", unsafe_allow_html=True)
    
    # Verificar se os dados necessários estão disponíveis
    if not st.session_state.financial_data_submitted or not st.session_state.questionnaire_completed:
        st.warning("Por favor, complete o questionário financeiro e comportamental para visualizar seus relatórios.")
        
        # Botão para voltar
        if st.button("Voltar para o Questionário"):
            if not st.session_state.financial_data_submitted:
                st.session_state.current_page = "financial_input"
            else:
                st.session_state.current_page = "questionnaire"
            st.experimental_rerun()
        
        return
    
    # Verificar se o usuário é premium
    is_premium = st.session_state.get("premium_user", False)
    
    # Obter dados financeiros
    financial_data = st.session_state.financial_data
    
    # Obter perfil comportamental
    from pages.questionnaire import calculate_profile
    profile_scores = calculate_profile(st.session_state.question_responses)
    
    # Tabs para diferentes relatórios
    tab1, tab2, tab3, tab4 = st.tabs([
        "Relatório Financeiro", 
        "Saúde Financeira", 
        "Perfil Comportamental",
        "Plano de Ação"
    ])
    
    with tab1:
        st.markdown("<h2>Relatório Financeiro Objetivo</h2>", unsafe_allow_html=True)
        
        # Calcular métricas principais
        income_total = financial_data["income"]["total"]
        expenses_total = financial_data["expenses"]["total"]
        balance = income_total - expenses_total
        assets_total = financial_data["assets"]["total"]
        debts_total = financial_data["debts"]["total"]
        net_worth = assets_total - debts_total
        
        # Balanço Patrimonial
        st.markdown("<h3>Balanço Patrimonial</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>Ativos</h4>", unsafe_allow_html=True)
            
            assets = financial_data["assets"]
            assets_df = pd.DataFrame({
                "Categoria": ["Poupança/Reserva", "Investimentos", "Imóveis", "Outros"],
                "Valor (R$)": [
                    assets["savings"], 
                    assets["investments"], 
                    assets["real_estate"], 
                    assets["other"]
                ]
            })
            
            # Filtrar categorias com valores
            assets_df = assets_df[assets_df["Valor (R$)"] > 0]
            
            if not assets_df.empty:
                st.dataframe(assets_df, use_container_width=True)
                st.metric("Total de Ativos", f"R$ {assets_total:.2f}")
            else:
                st.info("Não há dados de ativos para exibir.")
        
        with col2:
            st.markdown("<h4>Passivos</h4>", unsafe_allow_html=True)
            
            debts = financial_data["debts"]
            debts_df = pd.DataFrame({
                "Categoria": ["Cartão de Crédito", "Empréstimos", "Outros"],
                "Valor (R$)": [
                    debts["credit_card"], 
                    debts["loans"], 
                    debts["other"]
                ]
            })
            
            # Filtrar categorias com valores
            debts_df = debts_df[debts_df["Valor (R$)"] > 0]
            
            if not debts_df.empty:
                st.dataframe(debts_df, use_container_width=True)
                st.metric("Total de Passivos", f"R$ {debts_total:.2f}")
            else:
                st.info("Não há dados de passivos para exibir.")
        
        # Patrimônio Líquido
        st.metric("Patrimônio Líquido", f"R$ {net_worth:.2f}")
        
        # Fluxo de Caixa
        st.markdown("<h3>Fluxo de Caixa Mensal</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>Receitas</h4>", unsafe_allow_html=True)
            
            income = financial_data["income"]
            income_df = pd.DataFrame({
                "Categoria": ["Salário", "Investimentos", "Outros"],
                "Valor (R$)": [
                    income["salary"], 
                    income["investments"], 
                    income["other"]
                ]
            })
            
            # Filtrar categorias com valores
            income_df = income_df[income_df["Valor (R$)"] > 0]
            
            if not income_df.empty:
                st.dataframe(income_df, use_container_width=True)
                st.metric("Total de Receitas", f"R$ {income_total:.2f}")
            else:
                st.info("Não há dados de receitas para exibir.")
        
        with col2:
            st.markdown("<h4>Despesas</h4>", unsafe_allow_html=True)
            
            expenses = financial_data["expenses"]
            expenses_df = pd.DataFrame({
                "Categoria": ["Moradia", "Alimentação", "Transporte", "Contas", "Lazer", "Outros"],
                "Valor (R$)": [
                    expenses["housing"], 
                    expenses["food"], 
                    expenses["transportation"], 
                    expenses["utilities"], 
                    expenses["leisure"], 
                    expenses["other"]
                ]
            })
            
            # Filtrar categorias com valores
            expenses_df = expenses_df[expenses_df["Valor (R$)"] > 0]
            
            if not expenses_df.empty:
                st.dataframe(expenses_df, use_container_width=True)
                st.metric("Total de Despesas", f"R$ {expenses_total:.2f}")
            else:
                st.info("Não há dados de despesas para exibir.")
        
        # Saldo Mensal
        st.metric("Saldo Mensal", f"R$ {balance:.2f}")
        
        # Análise de Dívidas (versão premium)
        if is_premium:
            st.markdown("<h3>Análise Detalhada de Dívidas</h3>", unsafe_allow_html=True)
            
            debts = financial_data["debts"]
            debt_categories = ["Cartão de Crédito", "Empréstimos", "Outros"]
            debt_values = [debts["credit_card"], debts["loans"], debts["other"]]
            debt_rates = [debts["credit_card_rate"], debts["loans_rate"], debts["other_rate"]]
            
            # Calcular juros mensais e anuais
            monthly_interest = [v * r / 100 for v, r in zip(debt_values, debt_rates)]
            annual_interest = [m * 12 for m in monthly_interest]
            
            # Calcular tempo para quitação (assumindo pagamento de 10% ao mês)
            months_to_payoff = []
            for i, value in enumerate(debt_values):
                if value > 0 and debt_rates[i] > 0:
                    # Fórmula simplificada para estimativa
                    payment = value * 0.1
                    rate = debt_rates[i] / 100
                    months = -np.log(1 - (value * rate / payment)) / np.log(1 + rate)
                    months_to_payoff.append(round(months))
                else:
                    months_to_payoff.append(0)
            
            # Criar dataframe para tabela
            debt_analysis_df = pd.DataFrame({
                "Tipo de Dívida": debt_categories,
                "Valor (R$)": debt_values,
                "Taxa de Juros (%)": debt_rates,
                "Juros Mensais (R$)": monthly_interest,
                "Juros Anuais (R$)": annual_interest,
                "Meses para Quitação (10% ao mês)": months_to_payoff
            })
            
            # Filtrar dívidas com valores
            debt_analysis_df = debt_analysis_df[debt_analysis_df["Valor (R$)"] > 0]
            
            if not debt_analysis_df.empty:
                st.dataframe(debt_analysis_df, use_container_width=True)
                
                # Total de juros
                total_monthly_interest = sum(monthly_interest)
                total_annual_interest = sum(annual_interest)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total de Juros Mensais", f"R$ {total_monthly_interest:.2f}")
                with col2:
                    st.metric("Total de Juros Anuais", f"R$ {total_annual_interest:.2f}")
                
                # Recomendações para quitação de dívidas
                st.markdown("<h4>Estratégia de Quitação de Dívidas</h4>", unsafe_allow_html=True)
                
                # Ordenar dívidas por taxa de juros (método avalanche)
                avalanche_order = debt_analysis_df.sort_values("Taxa de Juros (%)", ascending=False)
                
                st.markdown("""
                <div class="strategy-card">
                    <h5>Método Avalanche (Recomendado)</h5>
                    <p>Priorize o pagamento das dívidas com maiores taxas de juros primeiro, 
                    enquanto mantém o pagamento mínimo nas demais.</p>
                    <p>Ordem de prioridade para quitação:</p>
                </div>
                """, unsafe_allow_html=True)
                
                for i, row in avalanche_order.iterrows():
                    st.markdown(f"""
                    <div class="priority-item">
                        <strong>{i+1}. {row['Tipo de Dívida']}</strong> - 
                        Taxa: {row['Taxa de Juros (%)']}% - 
                        Valor: R$ {row['Valor (R$)']:.2f}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Não há dados de dívidas para análise.")
        else:
            st.markdown("""
            <div class="premium-alert">
                <h4>Análise Detalhada de Dívidas</h4>
                <p>Disponível apenas na versão premium.</p>
                <p>Adquira o plano premium para acessar análises detalhadas de suas dívidas, 
                estratégias de quitação e economia potencial de juros.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Adquirir Plano Premium", key="premium_debt"):
                st.session_state.current_page = "payment"
                st.experimental_rerun()
    
    with tab2:
        st.markdown("<h2>Visão Geral e Saúde Financeira</h2>", unsafe_allow_html=True)
        
        # Calcular métricas de saúde financeira
        income_total = financial_data["income"]["total"]
        expenses_total = financial_data["expenses"]["total"]
        balance = income_total - expenses_total
        assets_total = financial_data["assets"]["total"]
        debts_total = financial_data["debts"]["total"]
        
        # Taxa de poupança
        savings_rate = (balance / income_total) * 100 if income_total > 0 else 0
        
        # Índice de endividamento
        debt_to_income = (debts_total / (income_total * 12)) * 100 if income_total > 0 else 0
        
        # Reserva de emergência (em meses)
        emergency_fund = financial_data["assets"]["savings"]
        emergency_months = emergency_fund / expenses_total if expenses_total > 0 else 0
        
        # Exibir métricas principais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Taxa de Poupança", f"{savings_rate:.1f}%")
        with col2:
            st.metric("Índice de Endividamento", f"{debt_to_income:.1f}%")
        with col3:
            st.metric("Reserva de Emergência", f"{emergency_months:.1f} meses")
        
        # Avaliação das métricas
        st.markdown("<h3>Avaliação de Saúde Financeira</h3>", unsafe_allow_html=True)
        
        # Taxa de poupança
        st.markdown("<h4>Taxa de Poupança</h4>", unsafe_allow_html=True)
        
        if savings_rate >= 20:
            savings_status = "Excelente"
            savings_color = "green"
            savings_message = "Sua taxa de poupança está acima de 20%, o que é excelente! Continue assim."
        elif savings_rate >= 10:
            savings_status = "Boa"
            savings_color = "blue"
            savings_message = "Sua taxa de poupança está entre 10% e 20%, o que é bom. Considere aumentar um pouco mais se possível."
        elif savings_rate > 0:
            savings_status = "Regular"
            savings_color = "orange"
            savings_message = "Sua taxa de poupança está positiva, mas abaixo de 10%. Tente aumentar para melhorar sua segurança financeira."
        else:
            savings_status = "Crítica"
            savings_color = "red"
            savings_message = "Sua taxa de poupança é negativa ou zero. Priorize reduzir despesas ou aumentar receitas."
        
        st.markdown(f"""
        <div class="metric-evaluation {savings_color}">
            <div class="status">{savings_status}</div>
            <p>{savings_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Índice de endividamento
        st.markdown("<h4>Índice de Endividamento</h4>", unsafe_allow_html=True)
        
        if debt_to_income <= 20:
            debt_status = "Excelente"
            debt_color = "green"
            debt_message = "Seu índice de endividamento está abaixo de 20%, o que é excelente! Você tem uma boa margem de segurança."
        elif debt_to_income <= 36:
            debt_status = "Bom"
            debt_color = "blue"
            debt_message = "Seu índice de endividamento está entre 20% e 36%, o que é considerado bom. Evite aumentar suas dívidas."
        elif debt_to_income <= 50:
            debt_status = "Regular"
            debt_color = "orange"
            debt_message = "Seu índice de endividamento está entre 36% e 50%. Considere estratégias para reduzir suas dívidas."
        else:
            debt_status = "Crítico"
            debt_color = "red"
            debt_message = "Seu índice de endividamento está acima de 50%, o que é considerado crítico. Priorize a redução de dívidas."
        
        st.markdown(f"""
        <div class="metric-evaluation {debt_color}">
            <div class="status">{debt_status}</div>
            <p>{debt_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Reserva de emergência
        st.markdown("<h4>Reserva de Emergência</h4>", unsafe_allow_html=True)
        
        if emergency_months >= 6:
            emergency_status = "Excelente"
            emergency_color = "green"
            emergency_message = "Sua reserva de emergência cobre 6 meses ou mais de despesas, o que é excelente! Você está bem preparado para imprevistos."
        elif emergency_months >= 3:
            emergency_status = "Boa"
            emergency_color = "blue"
            emergency_message = "Sua reserva de emergência cobre entre 3 e 6 meses de despesas, o que é bom. Continue aumentando até atingir 6 meses."
        elif emergency_months > 0:
            emergency_status = "Regular"
            emergency_color = "orange"
            emergency_message = "Sua reserva de emergência cobre menos de 3 meses de despesas. Priorize aumentá-la para melhorar sua segurança financeira."
        else:
            emergency_status = "Crítica"
            emergency_color = "red"
            emergency_message = "Você não possui reserva de emergência. Priorize a criação de uma reserva para cobrir pelo menos 3 meses de despesas."
        
        st.markdown(f"""
        <div class="metric-evaluation {emergency_color}">
            <div class="status">{emergency_status}</div>
            <p>{emergency_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Índice de Bem-Estar Financeiro (versão premium)
        if is_premium:
            st.markdown("<h3>Índice de Bem-Estar Financeiro</h3>", unsafe_allow_html=True)
            
            # Calcular índice de bem-estar financeiro (versão mais completa)
            financial_wellbeing = 0
            
            # Fatores positivos
            if savings_rate >= 20:
                financial_wellbeing += 25
            elif savings_rate >= 10:
                financial_wellbeing += 15
            elif savings_rate > 0:
                financial_wellbeing += 5
            
            if debt_to_income <= 20:
                financial_wellbeing += 25
            elif debt_to_income <= 36:
                financial_wellbeing += 15
            elif debt_to_income <= 50:
                financial_wellbeing += 5
            
            if emergency_months >= 6:
                financial_wellbeing += 25
            elif emergency_months >= 3:
                financial_wellbeing += 15
            elif emergency_months > 0:
                financial_wellbeing += 5
            
            # Fator de patrimônio líquido
            if assets_total > 0 and debts_total > 0:
                net_worth_ratio = assets_total / debts_total
                if net_worth_ratio >= 5:
                    financial_wellbeing += 25
                elif net_worth_ratio >= 2:
                    financial_wellbeing += 15
                elif net_worth_ratio > 1:
                    financial_wellbeing += 5
            elif assets_total > 0 and debts_total == 0:
                financial_wellbeing += 25
            
            # Criar gráfico de medidor
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = financial_wellbeing,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Índice de Bem-Estar Financeiro"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#5a67d8"},
                    'steps': [
                        {'range': [0, 30], 'color': "#fc8181"},
                        {'range': [30, 70], 'color': "#f6ad55"},
                        {'range': [70, 100], 'color': "#48bb78"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': financial_wellbeing
                    }
                }
            ))
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretação do índice
            if financial_wellbeing >= 70:
                wellbeing_status = "Excelente"
                wellbeing_message = """
                Seu índice de bem-estar financeiro é excelente! Você está no caminho certo para alcançar seus objetivos financeiros.
                Suas finanças estão bem estruturadas, com boa taxa de poupança, baixo endividamento e reserva de emergência adequada.
                Continue com suas boas práticas financeiras e considere diversificar seus investimentos para maximizar seus retornos.
                """
            elif financial_wellbeing >= 40:
                wellbeing_status = "Bom"
                wellbeing_message = """
                Seu índice de bem-estar financeiro é bom, mas há espaço para melhorias.
                Você está no caminho certo, mas pode fortalecer ainda mais sua posição financeira.
                Foque em aumentar sua taxa de poupança, reduzir dívidas de alto custo e fortalecer sua reserva de emergência.
                """
            elif financial_wellbeing >= 20:
                wellbeing_status = "Regular"
                wellbeing_message = """
                Seu índice de bem-estar financeiro está regular, indicando algumas áreas que precisam de atenção.
                Priorize a redução de dívidas, aumente sua taxa de poupança e comece a construir uma reserva de emergência.
                Considere revisar seu orçamento para identificar oportunidades de redução de despesas.
                """
            else:
                wellbeing_status = "Crítico"
                wellbeing_message = """
                Seu índice de bem-estar financeiro está em nível crítico, indicando a necessidade de ações imediatas.
                Priorize a estabilização do seu fluxo de caixa, reduzindo despesas não essenciais.
                Desenvolva um plano para reduzir dívidas de alto custo e comece a construir uma pequena reserva de emergência.
                Considere buscar orientação financeira especializada para ajudá-lo a desenvolver um plano de recuperação.
                """
            
            st.markdown(f"""
            <div class="wellbeing-interpretation">
                <h4>{wellbeing_status}</h4>
                <p>{wellbeing_message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Indicadores de resiliência financeira
            st.markdown("<h3>Indicadores de Resiliência Financeira</h3>", unsafe_allow_html=True)
            
            # Calcular indicadores
            # Diversificação de receitas
            income_sources = sum(1 for v in [financial_data["income"]["salary"], financial_data["income"]["investments"], financial_data["income"]["other"]] if v > 0)
            
            # Proporção de despesas fixas
            fixed_expenses = financial_data["expenses"]["housing"] + financial_data["expenses"]["utilities"]
            fixed_ratio = (fixed_expenses / expenses_total) * 100 if expenses_total > 0 else 0
            
            # Exibir indicadores
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Fontes de Receita", f"{income_sources}")
                st.markdown("""
                <div class="indicator-note">
                    <p>Mais fontes de receita aumentam sua resiliência financeira.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Proporção de Despesas Fixas", f"{fixed_ratio:.1f}%")
                st.markdown("""
                <div class="indicator-note">
                    <p>Menor proporção de despesas fixas aumenta sua flexibilidade financeira.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-alert">
                <h4>Análise Completa de Saúde Financeira</h4>
                <p>Disponível apenas na versão premium.</p>
                <p>Adquira o plano premium para acessar análises detalhadas de sua saúde financeira, 
                índice de bem-estar financeiro completo e indicadores de resiliência financeira.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Adquirir Plano Premium", key="premium_health"):
                st.session_state.current_page = "payment"
                st.experimental_rerun()
    
    with tab3:
        st.markdown("<h2>Perfil Comportamental</h2>", unsafe_allow_html=True)
        
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
        
        # Relatório Psicológico Completo (versão premium)
        if is_premium:
            st.markdown("<h3>Análise Psicológica Aprofundada</h3>", unsafe_allow_html=True)
            
            # Flashpoints financeiros
            st.markdown("<h4>Flashpoints Financeiros</h4>", unsafe_allow_html=True)
            st.markdown("""
            <p>Flashpoints financeiros são eventos ou situações que desencadeiam reações emocionais 
            intensas relacionadas a dinheiro. Identificar seus flashpoints ajuda a entender e gerenciar 
            melhor suas reações emocionais.</p>
            """, unsafe_allow_html=True)
            
            # Flashpoints específicos baseados no perfil dominante
            if dominant_profile[0] == "evitador":
                flashpoints = [
                    "Conversas sobre planejamento financeiro",
                    "Recebimento de contas ou extratos bancários",
                    "Necessidade de tomar decisões financeiras importantes",
                    "Situações que exigem negociação financeira"
                ]
            elif dominant_profile[0] == "apegado":
                flashpoints = [
                    "Gastos inesperados ou emergências",
                    "Pressão para gastar em situações sociais",
                    "Flutuações no mercado financeiro",
                    "Empréstimos ou doações de dinheiro"
                ]
            elif dominant_profile[0] == "ostentador":
                flashpoints = [
                    "Restrições orçamentárias",
                    "Comparações sociais sobre posses materiais",
                    "Necessidade de economizar para objetivos de longo prazo",
                    "Críticas sobre seus hábitos de consumo"
                ]
            else:  # Planejador
                flashpoints = [
                    "Desvios do plano financeiro estabelecido",
                    "Gastos impulsivos ou não planejados",
                    "Mudanças inesperadas na situação financeira",
                    "Falha em atingir metas financeiras"
                ]
            
            # Exibir flashpoints
            for point in flashpoints:
                st.markdown(f"<div class='flashpoint-item'>• {point}</div>", unsafe_allow_html=True)
            
            # Crenças limitantes e fortalecedoras
            st.markdown("<h4>Crenças sobre Dinheiro</h4>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h5>Crenças Limitantes</h5>", unsafe_allow_html=True)
                
                # Crenças limitantes baseadas no perfil dominante
                if dominant_profile[0] == "evitador":
                    limiting_beliefs = [
                        "Finanças são muito complicadas para eu entender",
                        "Pensar em dinheiro é estressante e deve ser evitado",
                        "Nunca serei bom em gerenciar dinheiro",
                        "É melhor não saber exatamente como estão minhas finanças"
                    ]
                elif dominant_profile[0] == "apegado":
                    limiting_beliefs = [
                        "Nunca se pode ter dinheiro suficiente",
                        "Gastar dinheiro é perigoso e arriscado",
                        "Devo economizar tudo que puder para o futuro",
                        "Não mereço gastar em coisas que me dão prazer"
                    ]
                elif dominant_profile[0] == "ostentador":
                    limiting_beliefs = [
                        "Meu valor pessoal está ligado ao que possuo",
                        "Preciso gastar para impressionar os outros",
                        "Economizar é para pessoas sem visão",
                        "Viver o momento é mais importante que planejar o futuro"
                    ]
                else:  # Planejador
                    limiting_beliefs = [
                        "Qualquer desvio do plano é um fracasso",
                        "Devo controlar cada centavo que gasto",
                        "Imprevistos financeiros são inaceitáveis",
                        "Nunca devo me dar ao luxo de ser espontâneo com dinheiro"
                    ]
                
                # Exibir crenças limitantes
                for belief in limiting_beliefs:
                    st.markdown(f"<div class='belief-item limiting'>• {belief}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<h5>Crenças Fortalecedoras</h5>", unsafe_allow_html=True)
                
                # Crenças fortalecedoras baseadas no perfil dominante
                if dominant_profile[0] == "evitador":
                    empowering_beliefs = [
                        "Posso aprender a gerenciar minhas finanças passo a passo",
                        "Enfrentar minha situação financeira me dá mais controle",
                        "Pequenas ações consistentes levam a grandes resultados",
                        "Pedir ajuda com finanças é um sinal de inteligência"
                    ]
                elif dominant_profile[0] == "apegado":
                    empowering_beliefs = [
                        "Posso encontrar equilíbrio entre poupar e aproveitar o dinheiro",
                        "Gastar em experiências valiosas é um bom investimento",
                        "Segurança financeira permite flexibilidade, não apenas restrição",
                        "Mereço usar parte do meu dinheiro para meu bem-estar"
                    ]
                elif dominant_profile[0] == "ostentador":
                    empowering_beliefs = [
                        "Meu valor não depende do que possuo ou mostro aos outros",
                        "Posso encontrar prazer em experiências que não custam muito",
                        "Equilibrar gastos atuais e poupança futura me traz mais liberdade",
                        "Minhas escolhas financeiras são para meu bem-estar, não para impressionar"
                    ]
                else:  # Planejador
                    empowering_beliefs = [
                        "Flexibilidade é parte de um bom plano financeiro",
                        "Posso adaptar meus planos sem perder o controle",
                        "Equilíbrio entre disciplina e espontaneidade é saudável",
                        "Imprevistos são oportunidades para testar minha resiliência"
                    ]
                
                # Exibir crenças fortalecedoras
                for belief in empowering_beliefs:
                    st.markdown(f"<div class='belief-item empowering'>• {belief}</div>", unsafe_allow_html=True)
            
            # Intervenções comportamentais
            st.markdown("<h4>Intervenções Comportamentais Recomendadas</h4>", unsafe_allow_html=True)
            
            # Intervenções baseadas no perfil dominante
            if dominant_profile[0] == "evitador":
                interventions = [
                    {
                        "title": "Exposição Gradual",
                        "description": "Comece com pequenas tarefas financeiras (como verificar o saldo bancário) e aumente gradualmente para tarefas mais complexas."
                    },
                    {
                        "title": "Diário Financeiro Emocional",
                        "description": "Registre seus sentimentos ao lidar com dinheiro para identificar padrões emocionais."
                    },
                    {
                        "title": "Sistema de Recompensas",
                        "description": "Crie pequenas recompensas para si mesmo após completar tarefas financeiras."
                    },
                    {
                        "title": "Automatização",
                        "description": "Configure pagamentos automáticos e transferências para poupança para reduzir a necessidade de decisões frequentes."
                    }
                ]
            elif dominant_profile[0] == "apegado":
                interventions = [
                    {
                        "title": "Orçamento de Prazer",
                        "description": "Defina uma quantia mensal específica para gastar livremente, sem culpa."
                    },
                    {
                        "title": "Desafio de Gastos Conscientes",
                        "description": "Pratique gastar em algo que realmente valoriza, observando como isso afeta seu bem-estar."
                    },
                    {
                        "title": "Visualização de Objetivos",
                        "description": "Visualize como o dinheiro pode ser uma ferramenta para alcançar seus objetivos de vida, não apenas para acumular."
                    },
                    {
                        "title": "Análise de Valor vs. Custo",
                        "description": "Avalie compras não apenas pelo custo, mas pelo valor que trazem à sua vida."
                    }
                ]
            elif dominant_profile[0] == "ostentador":
                interventions = [
                    {
                        "title": "Período de Reflexão",
                        "description": "Implemente uma regra de espera de 48 horas antes de fazer compras não essenciais."
                    },
                    {
                        "title": "Desafio de Consumo Consciente",
                        "description": "Experimente um mês focando em experiências que não envolvam gastos significativos."
                    },
                    {
                        "title": "Redefinição de Valores",
                        "description": "Identifique e liste seus valores pessoais mais profundos e como eles se relacionam (ou não) com seus hábitos de consumo."
                    },
                    {
                        "title": "Poupança Automática",
                        "description": "Configure transferências automáticas para poupança antes que o dinheiro esteja disponível para gastar."
                    }
                ]
            else:  # Planejador
                interventions = [
                    {
                        "title": "Orçamento Flexível",
                        "description": "Crie um orçamento com categorias flexíveis que permitam ajustes sem sentimento de fracasso."
                    },
                    {
                        "title": "Prática de Gastos Espontâneos",
                        "description": "Reserve uma pequena quantia mensal para gastos totalmente não planejados."
                    },
                    {
                        "title": "Exercícios de Tolerância à Incerteza",
                        "description": "Pratique lidar com pequenas incertezas financeiras para desenvolver resiliência."
                    },
                    {
                        "title": "Revisão de Planos",
                        "description": "Estabeleça revisões regulares de seus planos financeiros, permitindo ajustes sem julgamento."
                    }
                ]
            
            # Exibir intervenções
            for intervention in interventions:
                st.markdown(f"""
                <div class="intervention-card">
                    <h5>{intervention['title']}</h5>
                    <p>{intervention['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-alert">
                <h4>Relatório Psicológico Completo</h4>
                <p>Disponível apenas na versão premium.</p>
                <p>Adquira o plano premium para acessar análises detalhadas de seus padrões psicológicos, 
                flashpoints financeiros, crenças limitantes e fortalecedoras, e intervenções comportamentais personalizadas.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Adquirir Plano Premium", key="premium_psych"):
                st.session_state.current_page = "payment"
                st.experimental_rerun()
    
    with tab4:
        st.markdown("<h2>Plano de Ação</h2>", unsafe_allow_html=True)
        
        # Versão básica do plano de ação (gratuita)
        st.markdown("<h3>Próximos Passos Recomendados</h3>", unsafe_allow_html=True)
        
        # Gerar recomendações básicas com base nos dados financeiros
        recommendations = []
        
        # Verificar taxa de poupança
        income_total = financial_data["income"]["total"]
        expenses_total = financial_data["expenses"]["total"]
        balance = income_total - expenses_total
        savings_rate = (balance / income_total) * 100 if income_total > 0 else 0
        
        if savings_rate < 10:
            recommendations.append({
                "title": "Aumentar Taxa de Poupança",
                "description": "Sua taxa de poupança está abaixo do recomendado. Considere revisar seu orçamento para reduzir despesas ou buscar formas de aumentar sua renda.",
                "priority": "Alta"
            })
        
        # Verificar reserva de emergência
        emergency_fund = financial_data["assets"]["savings"]
        emergency_months = emergency_fund / expenses_total if expenses_total > 0 else 0
        
        if emergency_months < 3:
            recommendations.append({
                "title": "Construir Reserva de Emergência",
                "description": "Sua reserva de emergência está abaixo do recomendado. Priorize acumular pelo menos 3 meses de despesas em uma conta de fácil acesso.",
                "priority": "Alta"
            })
        
        # Verificar dívidas de alto custo
        debts = financial_data["debts"]
        if debts["credit_card"] > 0 and debts["credit_card_rate"] > 15:
            recommendations.append({
                "title": "Quitar Dívidas de Cartão de Crédito",
                "description": "Suas dívidas de cartão de crédito têm juros elevados. Priorize a quitação dessas dívidas para economizar em juros.",
                "priority": "Alta"
            })
        
        # Verificar diversificação de receitas
        income_sources = sum(1 for v in [financial_data["income"]["salary"], financial_data["income"]["investments"], financial_data["income"]["other"]] if v > 0)
        if income_sources < 2:
            recommendations.append({
                "title": "Diversificar Fontes de Renda",
                "description": "Você depende de poucas fontes de renda. Considere explorar formas de diversificar suas receitas para aumentar sua segurança financeira.",
                "priority": "Média"
            })
        
        # Verificar investimentos
        if financial_data["assets"]["investments"] == 0:
            recommendations.append({
                "title": "Iniciar Investimentos",
                "description": "Você ainda não possui investimentos. Considere iniciar uma estratégia de investimentos para fazer seu dinheiro trabalhar para você.",
                "priority": "Média"
            })
        
        # Adicionar recomendação baseada no perfil comportamental
        dominant_profile = max(profile_scores.items(), key=lambda x: x[1])[0]
        
        if dominant_profile == "evitador":
            recommendations.append({
                "title": "Desenvolver Hábitos Financeiros Regulares",
                "description": "Seu perfil indica tendência a evitar questões financeiras. Estabeleça o hábito de revisar suas finanças semanalmente, começando com sessões curtas.",
                "priority": "Média"
            })
        elif dominant_profile == "apegado":
            recommendations.append({
                "title": "Equilibrar Poupança e Qualidade de Vida",
                "description": "Seu perfil indica tendência a economizar excessivamente. Defina um 'orçamento de prazer' mensal para gastar sem culpa em coisas que valoriza.",
                "priority": "Média"
            })
        elif dominant_profile == "ostentador":
            recommendations.append({
                "title": "Implementar Regra de Espera para Compras",
                "description": "Seu perfil indica tendência a gastos impulsivos. Adote uma regra de espera de 48 horas antes de fazer compras não essenciais.",
                "priority": "Média"
            })
        else:  # Planejador
            recommendations.append({
                "title": "Adicionar Flexibilidade ao Planejamento",
                "description": "Seu perfil indica tendência ao planejamento rígido. Inclua uma margem para imprevistos em seu orçamento e permita-se ajustar planos quando necessário.",
                "priority": "Média"
            })
        
        # Exibir recomendações
        for recommendation in recommendations:
            priority_color = "red" if recommendation["priority"] == "Alta" else "orange"
            
            st.markdown(f"""
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <h4>{recommendation["title"]}</h4>
                    <span class="priority-badge {priority_color}">{recommendation["priority"]}</span>
                </div>
                <p>{recommendation["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Plano de Ação Detalhado (versão premium)
        if is_premium:
            st.markdown("<h3>Plano de Ação Estratégico</h3>", unsafe_allow_html=True)
            
            # Metas SMART
            st.markdown("<h4>Metas SMART Personalizadas</h4>", unsafe_allow_html=True)
            
            # Gerar metas SMART com base nos dados financeiros e perfil
            smart_goals = []
            
            # Meta de reserva de emergência
            if emergency_months < 6:
                target_months = 6
                current_fund = emergency_fund
                monthly_expense = expenses_total
                target_fund = monthly_expense * target_months
                missing_fund = target_fund - current_fund
                monthly_contribution = missing_fund / 12  # Em 12 meses
                
                smart_goals.append({
                    "title": "Reserva de Emergência Completa",
                    "specific": f"Acumular R$ {target_fund:.2f} (equivalente a {target_months} meses de despesas) em sua reserva de emergência",
                    "measurable": f"Aumentar de R$ {current_fund:.2f} para R$ {target_fund:.2f}",
                    "achievable": f"Contribuição mensal de R$ {monthly_contribution:.2f} durante 12 meses",
                    "relevant": "Proporciona segurança financeira e tranquilidade em caso de imprevistos",
                    "time_bound": "12 meses"
                })
            
            # Meta de redução de dívidas
            if debts["total"] > 0:
                target_reduction = debts["total"] * 0.5  # Reduzir 50% das dívidas
                monthly_contribution = target_reduction / 12  # Em 12 meses
                
                smart_goals.append({
                    "title": "Redução de Dívidas",
                    "specific": f"Reduzir suas dívidas totais em 50%",
                    "measurable": f"Diminuir de R$ {debts['total']:.2f} para R$ {debts['total'] - target_reduction:.2f}",
                    "achievable": f"Pagamento mensal adicional de R$ {monthly_contribution:.2f} durante 12 meses",
                    "relevant": "Reduz custos com juros e melhora sua saúde financeira geral",
                    "time_bound": "12 meses"
                })
            
            # Meta de investimentos
            if financial_data["assets"]["investments"] < income_total * 12:  # Menos de 1 ano de renda em investimentos
                target_investment = income_total * 0.15 * 12  # 15% da renda mensal durante 12 meses
                
                smart_goals.append({
                    "title": "Crescimento de Investimentos",
                    "specific": f"Aumentar seu portfólio de investimentos em R$ {target_investment:.2f}",
                    "measurable": f"Investir 15% da sua renda mensal regularmente",
                    "achievable": f"Contribuição mensal de R$ {income_total * 0.15:.2f}",
                    "relevant": "Constrói patrimônio e prepara para objetivos de longo prazo",
                    "time_bound": "12 meses"
                })
            
            # Exibir metas SMART
            for goal in smart_goals:
                st.markdown(f"""
                <div class="smart-goal-card">
                    <h5>{goal["title"]}</h5>
                    <div class="smart-criteria">
                        <div class="criterion"><strong>S</strong>pecífico: {goal["specific"]}</div>
                        <div class="criterion"><strong>M</strong>ensurável: {goal["measurable"]}</div>
                        <div class="criterion"><strong>A</strong>lcançável: {goal["achievable"]}</div>
                        <div class="criterion"><strong>R</strong>elevante: {goal["relevant"]}</div>
                        <div class="criterion"><strong>T</strong>emporal: {goal["time_bound"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # SWOT Financeira
            st.markdown("<h4>SWOT Financeira</h4>", unsafe_allow_html=True)
            
            # Gerar SWOT com base nos dados financeiros e perfil
            swot = {
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "threats": []
            }
            
            # Forças
            if savings_rate >= 10:
                swot["strengths"].append("Boa taxa de poupança (acima de 10%)")
            
            if emergency_months >= 3:
                swot["strengths"].append(f"Reserva de emergência adequada ({emergency_months:.1f} meses)")
            
            if financial_data["assets"]["total"] > financial_data["debts"]["total"]:
                swot["strengths"].append("Patrimônio líquido positivo")
            
            if dominant_profile == "planejador":
                swot["strengths"].append("Perfil comportamental orientado ao planejamento")
            
            if dominant_profile == "apegado":
                swot["strengths"].append("Disciplina para economizar")
            
            # Fraquezas
            if savings_rate < 10:
                swot["weaknesses"].append("Taxa de poupança abaixo do recomendado")
            
            if emergency_months < 3:
                swot["weaknesses"].append("Reserva de emergência insuficiente")
            
            if financial_data["debts"]["credit_card"] > 0:
                swot["weaknesses"].append("Dívidas de cartão de crédito com juros altos")
            
            if income_sources < 2:
                swot["weaknesses"].append("Dependência de poucas fontes de renda")
            
            if dominant_profile == "evitador":
                swot["weaknesses"].append("Tendência a evitar questões financeiras")
            
            if dominant_profile == "ostentador":
                swot["weaknesses"].append("Propensão a gastos impulsivos")
            
            # Oportunidades
            if financial_data["assets"]["investments"] == 0:
                swot["opportunities"].append("Potencial para iniciar investimentos")
            
            if financial_data["income"]["investments"] == 0:
                swot["opportunities"].append("Potencial para desenvolver fontes de renda passiva")
            
            swot["opportunities"].append("Possibilidade de refinanciar dívidas a taxas mais baixas")
            swot["opportunities"].append("Desenvolvimento de habilidades financeiras através de educação")
            
            # Ameaças
            if emergency_months < 1:
                swot["threats"].append("Vulnerabilidade a emergências financeiras")
            
            if income_sources < 2:
                swot["threats"].append("Risco de perda da principal fonte de renda")
            
            if financial_data["debts"]["total"] > income_total * 6:
                swot["threats"].append("Alto nível de endividamento")
            
            swot["threats"].append("Inflação e aumento do custo de vida")
            swot["threats"].append("Imprevistos de saúde ou familiares")
            
            # Exibir SWOT
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="swot-card strengths">
                    <h5>Forças</h5>
                    <ul>
                """, unsafe_allow_html=True)
                
                for item in swot["strengths"]:
                    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="swot-card opportunities">
                    <h5>Oportunidades</h5>
                    <ul>
                """, unsafe_allow_html=True)
                
                for item in swot["opportunities"]:
                    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="swot-card weaknesses">
                    <h5>Fraquezas</h5>
                    <ul>
                """, unsafe_allow_html=True)
                
                for item in swot["weaknesses"]:
                    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="swot-card threats">
                    <h5>Ameaças</h5>
                    <ul>
                """, unsafe_allow_html=True)
                
                for item in swot["threats"]:
                    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-alert">
                <h4>Plano de Ação Estratégico</h4>
                <p>Disponível apenas na versão premium.</p>
                <p>Adquira o plano premium para acessar um plano de ação detalhado com metas SMART personalizadas, 
                análise SWOT financeira completa e estratégias específicas para sua situação.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Adquirir Plano Premium", key="premium_plan"):
                st.session_state.current_page = "payment"
                st.experimental_rerun()
    
    # Navegação
    navigation_buttons(prev_page="dashboard", next_page=None)
