import pandas as pd
import numpy as np
import os
import io
import re

def validate_file(uploaded_file):
    """
    Valida o arquivo importado
    
    Args:
        uploaded_file: Arquivo carregado pelo usuário
        
    Returns:
        tuple: (is_valid, message)
    """
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    # Verificar tipo de arquivo
    if file_type not in ['xlsx', 'csv', 'ofx', 'pdf']:
        return False, f"Formato de arquivo não suportado: {file_type}. Por favor, use XLSX, CSV, OFX ou PDF."
    
    # Verificar tamanho do arquivo (limite de 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "Arquivo muito grande. O tamanho máximo permitido é 10MB."
    
    # Verificações específicas por tipo de arquivo
    if file_type == 'xlsx':
        try:
            # Tentar ler o arquivo Excel
            pd.read_excel(uploaded_file)
        except Exception as e:
            return False, f"Erro ao ler arquivo Excel: {str(e)}"
    
    elif file_type == 'csv':
        try:
            # Tentar ler o arquivo CSV
            pd.read_csv(uploaded_file)
        except Exception as e:
            return False, f"Erro ao ler arquivo CSV: {str(e)}"
    
    elif file_type == 'ofx':
        # Verificação básica de arquivo OFX
        try:
            content = uploaded_file.read().decode('utf-8', errors='ignore')
            if '<OFX>' not in content and '<ofx>' not in content:
                return False, "Arquivo OFX inválido. Formato não reconhecido."
            # Resetar o ponteiro do arquivo para o início
            uploaded_file.seek(0)
        except Exception as e:
            return False, f"Erro ao ler arquivo OFX: {str(e)}"
    
    elif file_type == 'pdf':
        # Verificação básica de arquivo PDF
        try:
            content = uploaded_file.read()
            if not content.startswith(b'%PDF-'):
                return False, "Arquivo PDF inválido. Formato não reconhecido."
            # Resetar o ponteiro do arquivo para o início
            uploaded_file.seek(0)
        except Exception as e:
            return False, f"Erro ao ler arquivo PDF: {str(e)}"
    
    return True, "Arquivo válido."

def process_financial_data(uploaded_file):
    """
    Processa os dados financeiros do arquivo importado
    
    Args:
        uploaded_file: Arquivo carregado pelo usuário
        
    Returns:
        dict: Dados financeiros processados
    """
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    # Inicializar estrutura de dados
    financial_data = {
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
        },
        "goals": {
            "short_term_desc": "",
            "short_term_amount": 0,
            "medium_term_desc": "",
            "medium_term_amount": 0,
            "long_term_desc": "",
            "long_term_amount": 0
        }
    }
    
    # Processar conforme o tipo de arquivo
    if file_type == 'xlsx':
        return process_excel(uploaded_file, financial_data)
    
    elif file_type == 'csv':
        return process_csv(uploaded_file, financial_data)
    
    elif file_type == 'ofx':
        return process_ofx(uploaded_file, financial_data)
    
    elif file_type == 'pdf':
        return process_pdf(uploaded_file, financial_data)
    
    return {"processed_data": financial_data}

def process_excel(uploaded_file, financial_data):
    """
    Processa arquivo Excel
    
    Args:
        uploaded_file: Arquivo Excel carregado pelo usuário
        financial_data: Estrutura de dados financeiros
        
    Returns:
        dict: Dados financeiros processados e DataFrames para visualização
    """
    # Tentar ler o arquivo Excel
    try:
        # Verificar se há múltiplas planilhas
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        
        # Inicializar DataFrames para visualização
        income_df = None
        expenses_df = None
        
        # Processar cada planilha
        for sheet_name in sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            # Tentar identificar o tipo de dados na planilha
            if 'receita' in sheet_name.lower() or 'renda' in sheet_name.lower() or 'income' in sheet_name.lower():
                # Processar como receitas
                income_df = df
                
                # Tentar mapear colunas para categorias de receita
                for col in df.columns:
                    col_lower = col.lower()
                    if 'salário' in col_lower or 'salario' in col_lower or 'salary' in col_lower:
                        financial_data["income"]["salary"] = df[col].sum()
                    elif 'investimento' in col_lower or 'investment' in col_lower:
                        financial_data["income"]["investments"] = df[col].sum()
                    elif 'outro' in col_lower or 'other' in col_lower:
                        financial_data["income"]["other"] = df[col].sum()
            
            elif 'despesa' in sheet_name.lower() or 'gasto' in sheet_name.lower() or 'expense' in sheet_name.lower():
                # Processar como despesas
                expenses_df = df
                
                # Tentar mapear colunas para categorias de despesa
                for col in df.columns:
                    col_lower = col.lower()
                    if 'moradia' in col_lower or 'aluguel' in col_lower or 'housing' in col_lower:
                        financial_data["expenses"]["housing"] = df[col].sum()
                    elif 'alimentação' in col_lower or 'alimentacao' in col_lower or 'food' in col_lower:
                        financial_data["expenses"]["food"] = df[col].sum()
                    elif 'transporte' in col_lower or 'transportation' in col_lower:
                        financial_data["expenses"]["transportation"] = df[col].sum()
                    elif 'conta' in col_lower or 'utilidade' in col_lower or 'utility' in col_lower:
                        financial_data["expenses"]["utilities"] = df[col].sum()
                    elif 'lazer' in col_lower or 'leisure' in col_lower:
                        financial_data["expenses"]["leisure"] = df[col].sum()
                    elif 'outro' in col_lower or 'other' in col_lower:
                        financial_data["expenses"]["other"] = df[col].sum()
        
        # Calcular totais
        financial_data["income"]["total"] = (
            financial_data["income"]["salary"] + 
            financial_data["income"]["investments"] + 
            financial_data["income"]["other"]
        )
        
        financial_data["expenses"]["total"] = (
            financial_data["expenses"]["housing"] + 
            financial_data["expenses"]["food"] + 
            financial_data["expenses"]["transportation"] + 
            financial_data["expenses"]["utilities"] + 
            financial_data["expenses"]["leisure"] + 
            financial_data["expenses"]["other"]
        )
        
        # Se não conseguiu identificar as planilhas específicas, tentar processar genericamente
        if income_df is None and expenses_df is None and len(sheet_names) > 0:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_names[0])
            
            # Criar DataFrames genéricos para visualização
            income_df = pd.DataFrame({
                "Categoria": ["Não categorizado"],
                "Valor": [df[df > 0].sum().sum()]
            })
            
            expenses_df = pd.DataFrame({
                "Categoria": ["Não categorizado"],
                "Valor": [abs(df[df < 0].sum().sum())]
            })
            
            # Atualizar dados financeiros
            financial_data["income"]["other"] = df[df > 0].sum().sum()
            financial_data["income"]["total"] = financial_data["income"]["other"]
            
            financial_data["expenses"]["other"] = abs(df[df < 0].sum().sum())
            financial_data["expenses"]["total"] = financial_data["expenses"]["other"]
        
        return {
            "processed_data": financial_data,
            "income_df": income_df,
            "expenses_df": expenses_df
        }
    
    except Exception as e:
        # Em caso de erro, retornar dados vazios
        return {"processed_data": financial_data}

def process_csv(uploaded_file, financial_data):
    """
    Processa arquivo CSV
    
    Args:
        uploaded_file: Arquivo CSV carregado pelo usuário
        financial_data: Estrutura de dados financeiros
        
    Returns:
        dict: Dados financeiros processados e DataFrames para visualização
    """
    # Tentar ler o arquivo CSV
    try:
        df = pd.read_csv(uploaded_file)
        
        # Inicializar DataFrames para visualização
        income_df = None
        expenses_df = None
        
        # Tentar identificar colunas relevantes
        date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
        value_cols = [col for col in df.columns if 'valor' in col.lower() or 'value' in col.lower() or 'amount' in col.lower()]
        desc_cols = [col for col in df.columns if 'desc' in col.lower() or 'categoria' in col.lower() or 'category' in col.lower()]
        
        # Se encontrou colunas relevantes
        if len(value_cols) > 0:
            value_col = value_cols[0]
            
            # Separar receitas e despesas
            if df[value_col].dtype in [np.float64, np.int64]:
                receitas = df[df[value_col] > 0]
                despesas = df[df[value_col] < 0]
                
                # Criar DataFrames para visualização
                if len(desc_cols) > 0:
                    desc_col = desc_cols[0]
                    
                    # Agrupar por categoria
                    income_df = receitas.groupby(desc_col)[value_col].sum().reset_index()
                    income_df.columns = ["Categoria", "Valor"]
                    
                    expenses_df = despesas.groupby(desc_col)[value_col].sum().reset_index()
                    expenses_df.columns = ["Categoria", "Valor"]
                    expenses_df["Valor"] = expenses_df["Valor"].abs()
                else:
                    # Sem categoria, criar DataFrame simples
                    income_df = pd.DataFrame({
                        "Categoria": ["Receitas"],
                        "Valor": [receitas[value_col].sum()]
                    })
                    
                    expenses_df = pd.DataFrame({
                        "Categoria": ["Despesas"],
                        "Valor": [despesas[value_col].abs().sum()]
                    })
                
                # Atualizar dados financeiros
                financial_data["income"]["other"] = receitas[value_col].sum()
                financial_data["income"]["total"] = financial_data["income"]["other"]
                
                financial_data["expenses"]["other"] = despesas[value_col].abs().sum()
                financial_data["expenses"]["total"] = financial_data["expenses"]["other"]
        
        return {
            "processed_data": financial_data,
            "income_df": income_df,
            "expenses_df": expenses_df
        }
    
    except Exception as e:
        # Em caso de erro, retornar dados vazios
        return {"processed_data": financial_data}

def process_ofx(uploaded_file, financial_data):
    """
    Processa arquivo OFX
    
    Args:
        uploaded_file: Arquivo OFX carregado pelo usuário
        financial_data: Estrutura de dados financeiros
        
    Returns:
        dict: Dados financeiros processados e DataFrames para visualização
    """
    # Implementação simplificada para o MVP
    # Em uma versão completa, usaríamos a biblioteca ofxparse
    
    try:
        content = uploaded_file.read().decode('utf-8', errors='ignore')
        
        # Extrair transações usando expressões regulares simples
        transactions = []
        
        # Padrão para encontrar transações
        pattern = r'<STMTTRN>(.*?)</STMTTRN>'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            # Extrair valor
            amount_match = re.search(r'<TRNAMT>(.*?)</TRNAMT>', match)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', '.'))
                
                # Extrair descrição
                desc_match = re.search(r'<MEMO>(.*?)</MEMO>', match)
                desc = desc_match.group(1) if desc_match else "Sem descrição"
                
                transactions.append({"description": desc, "amount": amount})
        
        # Separar receitas e despesas
        receitas = [t for t in transactions if t["amount"] > 0]
        despesas = [t for t in transactions if t["amount"] < 0]
        
        # Criar DataFrames para visualização
        income_df = pd.DataFrame(receitas)
        if not income_df.empty:
            income_df.columns = ["Descrição", "Valor"]
        
        expenses_df = pd.DataFrame(despesas)
        if not expenses_df.empty:
            expenses_df.columns = ["Descrição", "Valor"]
            expenses_df["Valor"] = expenses_df["Valor"].abs()
        
        # Atualizar dados financeiros
        financial_data["income"]["other"] = sum(t["amount"] for t in receitas)
        financial_data["income"]["total"] = financial_data["income"]["other"]
        
        financial_data["expenses"]["other"] = sum(abs(t["amount"]) for t in despesas)
        financial_data["expenses"]["total"] = financial_data["expenses"]["other"]
        
        return {
            "processed_data": financial_data,
            "income_df": income_df,
            "expenses_df": expenses_df
        }
    
    except Exception as e:
        # Em caso de erro, retornar dados vazios
        return {"processed_data": financial_data}

def process_pdf(uploaded_file, financial_data):
    """
    Processa arquivo PDF
    
    Args:
        uploaded_file: Arquivo PDF carregado pelo usuário
        financial_data: Estrutura de dados financeiros
        
    Returns:
        dict: Dados financeiros processados e DataFrames para visualização
    """
    # Implementação simplificada para o MVP
    # Em uma versão completa, usaríamos bibliotecas como PyPDF2 ou pdfplumber
    
    # Para o MVP, retornar dados vazios com mensagem informativa
    return {
        "processed_data": financial_data,
        "income_df": pd.DataFrame({"Categoria": ["Não processado"], "Valor": [0]}),
        "expenses_df": pd.DataFrame({"Categoria": ["Não processado"], "Valor": [0]})
    }
