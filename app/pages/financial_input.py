import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from components.navigation import navigation_buttons
from utils.file_import import validate_file, process_financial_data

# Upload de arquivo considerar Real do Brasil
def parse_brl_to_float(valor_str):
    """Converte string no formato brasileiro para float."""
    if valor_str:
        try:
            return float(valor_str.replace('.', '').replace(',', '.'))
        except ValueError:
            return None
    return None


def show():
    """Página de entrada de dados financeiros"""
    
    st.markdown("<h1>Seus Dados Financeiros</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-container">
        <p>Forneça informações sobre sua situação financeira atual. Estas informações serão usadas para 
        gerar análises personalizadas e recomendações específicas para você.</p>
        <p>Você pode inserir os dados manualmente ou importar de arquivos financeiros.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para diferentes métodos de entrada
    tab1, tab2 = st.tabs(["Entrada Manual", "Importar Arquivo"])
    
    with tab1:
        st.markdown("<h2>Entrada Manual de Dados</h2>", unsafe_allow_html=True)
        
        with st.form("financial_data_form"):
            # Receitas
            st.markdown("<h3>Receitas Mensais</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                salary = st.number_input("Salário", min_value=0.0, format="%.2f", step=100.0)
            with col2:
                investments_income = st.number_input("Renda de Investimentos", min_value=0.0, format="%.2f", step=100.0)
            other_income = st.number_input("Outras Receitas", min_value=0.0, format="%.2f", step=100.0)
            
            # Despesas
            st.markdown("<h3>Despesas Mensais</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                housing = st.number_input("Moradia (aluguel/financiamento)", min_value=0.0, format="%.2f", step=100.0)
                food = st.number_input("Alimentação", min_value=0.0, format="%.2f", step=100.0)
                transportation = st.number_input("Transporte", min_value=0.0, format="%.2f", step=100.0)
            with col2:
                utilities = st.number_input("Contas (água, luz, internet, etc.)", min_value=0.0, format="%.2f", step=100.0)
                leisure = st.number_input("Lazer e Entretenimento", min_value=0.0, format="%.2f", step=100.0)
                other_expenses = st.number_input("Outras Despesas", min_value=0.0, format="%.2f", step=100.0)
            
            # Ativos
            st.markdown("<h3>Ativos</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                savings = st.number_input("Poupança/Reserva de Emergência", min_value=0.0, format="%.2f", step=1000.0)
                investments = st.number_input("Investimentos", min_value=0.0, format="%.2f", step=1000.0)
            with col2:
                real_estate = st.number_input("Imóveis", min_value=0.0, format="%.2f", step=10000.0)
                other_assets = st.number_input("Outros Ativos", min_value=0.0, format="%.2f", step=1000.0)
            
            # Dívidas
            st.markdown("<h3>Dívidas</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                credit_card = st.number_input("Cartão de Crédito", min_value=0.0, format="%.2f", step=100.0)
            with col2:
                credit_card_rate = st.number_input("Taxa de Juros do Cartão (%)", min_value=0.0, max_value=100.0, format="%.2f", step=0.1)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                loans = st.number_input("Empréstimos", min_value=0.0, format="%.2f", step=100.0)
            with col2:
                loans_rate = st.number_input("Taxa de Juros dos Empréstimos (%)", min_value=0.0, max_value=100.0, format="%.2f", step=0.1)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                other_debts = st.number_input("Outras Dívidas", min_value=0.0, format="%.2f", step=100.0)
            with col2:
                other_debts_rate = st.number_input("Taxa de Juros de Outras Dívidas (%)", min_value=0.0, max_value=100.0, format="%.2f", step=0.1)
            
            # Botão de envio
            submitted = st.form_submit_button("Salvar Dados Financeiros")
            
            if submitted:
                # Calcular totais
                income_total = salary + investments_income + other_income
                expenses_total = housing + food + transportation + utilities + leisure + other_expenses
                assets_total = savings + investments + real_estate + other_assets
                debts_total = credit_card + loans + other_debts
                
                # Armazenar dados na sessão
                st.session_state.financial_data = {
                    "income": {
                        "salary": salary,
                        "investments": investments_income,
                        "other": other_income,
                        "total": income_total
                    },
                    "expenses": {
                        "housing": housing,
                        "food": food,
                        "transportation": transportation,
                        "utilities": utilities,
                        "leisure": leisure,
                        "other": other_expenses,
                        "total": expenses_total
                    },
                    "assets": {
                        "savings": savings,
                        "investments": investments,
                        "real_estate": real_estate,
                        "other": other_assets,
                        "total": assets_total
                    },
                    "debts": {
                        "credit_card": credit_card,
                        "credit_card_rate": credit_card_rate,
                        "loans": loans,
                        "loans_rate": loans_rate,
                        "other": other_debts,
                        "other_rate": other_debts_rate,
                        "total": debts_total
                    }
                }
                
                st.session_state.financial_data_submitted = True
                st.success("Dados financeiros salvos com sucesso!")
                
                # Avançar para a próxima página
                st.session_state.current_page = "questionnaire"
                st.rerun()
    
    with tab2:
        st.markdown("<h2>Importar Dados Financeiros</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="instruction-container">
            <p>Você pode importar seus dados financeiros de arquivos nos seguintes formatos:</p>
            <ul>
                <li>Excel (.xlsx)</li>
                <li>CSV (.csv)</li>
                <li>OFX (.ofx) - Extratos bancários</li>
                <li>PDF (.pdf) - Extratos bancários</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload de arquivo
        uploaded_file = st.file_uploader("Escolha um arquivo", type=["xlsx", "csv", "ofx", "pdf"])
        
        if uploaded_file is not None:
            # Validar arquivo
            is_valid, message = validate_file(uploaded_file)
            
            if is_valid:
                st.success(f"Arquivo válido: {uploaded_file.name}")
                
                # Processar dados
                result = process_financial_data(uploaded_file)
                processed_data = result.get("processed_data")
                
                # Exibir dados processados
                if "income_df" in result and result["income_df"] is not None:
                    st.markdown("<h3>Receitas Identificadas</h3>", unsafe_allow_html=True)
                    st.dataframe(result["income_df"])
                
                if "expenses_df" in result and result["expenses_df"] is not None:
                    st.markdown("<h3>Despesas Identificadas</h3>", unsafe_allow_html=True)
                    st.dataframe(result["expenses_df"])
                
                # Botão para confirmar dados
                if st.button("Confirmar e Continuar"):
                    st.session_state.financial_data = processed_data
                    st.session_state.financial_data_submitted = True
                    
                    # Avançar para a próxima página
                    st.session_state.current_page = "questionnaire"
                    st.rerun()
            else:
                st.error(message)
    
    # Exibir resumo dos dados (se já submetidos)
    if st.session_state.financial_data_submitted:
        st.markdown("<h2>Resumo dos Dados Financeiros</h2>", unsafe_allow_html=True)
        
        financial_data = st.session_state.financial_data
        
        # Calcular métricas principais
        income_total = financial_data["income"]["total"]
        expenses_total = financial_data["expenses"]["total"]
        balance = income_total - expenses_total
        assets_total = financial_data["assets"]["total"]
        debts_total = financial_data["debts"]["total"]
        net_worth = assets_total - debts_total
        
        # Exibir métricas em colunas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Receitas Mensais", f"R$ {income_total:.2f}")
        with col2:
            st.metric("Despesas Mensais", f"R$ {expenses_total:.2f}")
        with col3:
            st.metric("Saldo Mensal", f"R$ {balance:.2f}", delta=f"{(balance/income_total)*100:.1f}%" if income_total > 0 else "0%")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Ativos", f"R$ {assets_total:.2f}")
        with col2:
            st.metric("Total de Dívidas", f"R$ {debts_total:.2f}")
        with col3:
            st.metric("Patrimônio Líquido", f"R$ {net_worth:.2f}")
        
        # Gráfico de receitas vs despesas
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = ['Receitas', 'Despesas']
        values = [income_total, expenses_total]
        ax.bar(categories, values, color=['#48bb78', '#fc8181'])
        ax.set_ylabel('Valor (R$)')
        ax.set_title('Receitas vs Despesas Mensais')
        
        # Adicionar valores nas barras
        for i, v in enumerate(values):
            ax.text(i, v + 50, f'R$ {v:.2f}', ha='center')
        
        st.pyplot(fig)
    
    # Navegação
    navigation_buttons(prev_page="onboarding", next_page="questionnaire" if st.session_state.financial_data_submitted else None)
