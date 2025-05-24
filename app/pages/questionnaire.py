import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from components.navigation import navigation_buttons

def load_custom_radio_css():
    """Carrega CSS customizado para os radio buttons do questionário"""
    st.markdown("""
    <style>
    /* CSS completo fornecido acima */
    </style>
    """, unsafe_allow_html=True)

def show():
    """Página de questionário comportamental"""
    # Carregar CSS customizado PRIMEIRO
    load_custom_radio_css()
    
    st.markdown("""
    <h2 style='text-align: center; color: #1f77b4;'>📊 Questionário Comportamental</h2>
    
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 30px;'>
        <p style='color: white; text-align: center; margin: 0; font-size: 16px;'>
            Este questionário ajudará a identificar seu perfil comportamental em relação ao dinheiro.
            Responda com sinceridade para obter resultados mais precisos.
        </p>
        <p style='color: #E8F4FF; text-align: center; margin: 10px 0 0 0; font-size: 14px;'>
            Não existem respostas certas ou erradas. O objetivo é entender sua relação única com o dinheiro.
        </p>
    </div>
    """, unsafe_allow_html=True)



    
    
    # Definir perguntas
    questions = [
        {
            "id": "q1",
            "text": "Você está sempre buscando oportunidades que ajudam a alcançar seus objetivos de longo prazo.",
            "category": "planejador"
        },
        {
            "id": "q2",
            "text": "Você tende a perder o entusiasmo por objetivos de longo prazo depois de alguns meses.",
            "category": "evitador"
        },
        {
            "id": "q3",
            "text": "Você consegue identificar com precisão suas emoções específicas conforme as experimenta.",
            "category": "planejador"
        },
        {
            "id": "q4",
            "text": "Você consegue se acalmar rapidamente quando se sente chateado ou com raiva.",
            "category": "planejador"
        },
        {
            "id": "q5",
            "text": "Você acha fácil adaptar seus planos quando enfrenta obstáculos inesperados.",
            "category": "planejador"
        },
        {
            "id": "q6",
            "text": "Você está frequentemente insatisfeito com o próprio desempenho, mesmo quando é elogiado.",
            "category": "apegado"
        },
        {
            "id": "q7",
            "text": "Você prefere economizar dinheiro do que gastá-lo em prazeres imediatos.",
            "category": "apegado"
        },
        {
            "id": "q8",
            "text": "Você frequentemente compra coisas por impulso.",
            "category": "ostentador"
        },
        {
            "id": "q9",
            "text": "Você se preocupa constantemente com sua situação financeira.",
            "category": "evitador"
        },
        {
            "id": "q10",
            "text": "Você gosta de impressionar os outros com suas posses.",
            "category": "ostentador"
        },
        {
            "id": "q11",
            "text": "Você evita verificar seu saldo bancário quando está preocupado com dinheiro.",
            "category": "evitador"
        },
        {
            "id": "q12",
            "text": "Você tem um plano financeiro claro para os próximos 5 anos.",
            "category": "planejador"
        }
    ]
    
    
    
    
    
    # Configurações de paginação (mantém igual)
    if 'questionnaire_page' not in st.session_state:
        st.session_state.questionnaire_page = 1
    if 'question_responses' not in st.session_state:
        st.session_state.question_responses = {}

    questions_per_page = 5
    total_pages = len(questions) // questions_per_page + (1 if len(questions) % questions_per_page > 0 else 0)
    current_page = st.session_state.questionnaire_page

    st.markdown(f"<h4 style='text-align: center;'>Etapa {current_page} de {total_pages}</h4>", unsafe_allow_html=True)

    # Exibir perguntas da página atual - SEÇÃO MODIFICADA
    start_idx = (current_page - 1) * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions))

    for i in range(start_idx, end_idx):
        question = questions[i]
        
        # Pergunta centralizada
        st.markdown(f"<h3 style='text-align: center; margin-bottom: 10px;'>{question['text']}</h3>", unsafe_allow_html=True)
        
        # Labels de Concordo e Discordo
        cols_labels = st.columns([1, 6, 1])
        with cols_labels[0]:
            st.markdown("<p style='text-align: center; color: #10B981; font-weight: bold; margin-bottom: 5px;'>Concordo</p>", unsafe_allow_html=True)
        
        with cols_labels[2]:
            st.markdown("<p style='text-align: center; color: #8B5CF6; font-weight: bold; margin-bottom: 5px;'>Discordo</p>", unsafe_allow_html=True)
        
        # Radio buttons customizados
        response = st.radio(
            f"Pergunta {i+1}",
            options=[1, 2, 3, 4, 5, 6, 7],
            index=st.session_state.question_responses.get(question["id"], 4) - 1,
            horizontal=True,
            label_visibility="collapsed",
            key=f"question_{question['id']}"
        )
        
        # Armazenar resposta
        st.session_state.question_responses[question["id"]] = response
        
        # Espaçamento entre perguntas
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # Botões de navegação (mantém igual)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_page > 1:
            if st.button("← Anterior"):
                st.session_state.questionnaire_page -= 1
                st.rerun()
    
    with col3:
        if current_page < total_pages:
            if st.button("Próximo →"):
                st.session_state.questionnaire_page += 1
                st.rerun()
        else:
            if st.button("Finalizar Questionário"):
                st.session_state.questionnaire_completed = True
                st.session_state.current_page = "dashboard"
                st.rerun()





    
    
    # Exibir resultados parciais se todas as perguntas foram respondidas
    if len(st.session_state.question_responses) == len(questions) and current_page == total_pages:
        st.markdown("<h2>Resultados Parciais</h2>", unsafe_allow_html=True)
        
        profile_scores = calculate_profile(st.session_state.question_responses)
        
        # Criar gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 6))
        profiles = list(profile_scores.keys())
        scores = list(profile_scores.values())
        
        ax.bar(profiles, scores, color=['#5a67d8', '#38b2ac', '#f6ad55', '#fc8181'])
        ax.set_ylabel('Pontuação (%)')
        ax.set_title('Seu Perfil de Comportamento com o Dinheiro')
        
        # Rotacionar rótulos do eixo x para melhor visualização
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        st.pyplot(fig)
        
        st.markdown("""
        <div class="note">
            <p>Este é apenas um resultado parcial. Complete o questionário para ver sua análise completa 
            e receber recomendações personalizadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navegação
    navigation_buttons(
        prev_page="financial_input", 
        next_page="dashboard" if st.session_state.get("questionnaire_completed", False) else None
    )

def calculate_profile(responses):
    """
    Calcula o perfil comportamental com base nas respostas do questionário
    
    Args:
        responses (dict): Dicionário com as respostas do questionário
        
    Returns:
        dict: Pontuações para cada perfil comportamental
    """
    # Definir categorias e inicializar pontuações
    categories = {
        "evitador": {"count": 0, "sum": 0},
        "apegado": {"count": 0, "sum": 0},
        "ostentador": {"count": 0, "sum": 0},
        "planejador": {"count": 0, "sum": 0}
    }
    
    # Mapear perguntas para categorias
    question_categories = {
        "q1": "planejador",
        "q2": "evitador",
        "q3": "planejador",
        "q4": "planejador",
        "q5": "planejador",
        "q6": "apegado",
        "q7": "apegado",
        "q8": "ostentador",
        "q9": "evitador",
        "q10": "ostentador",
        "q11": "evitador",
        "q12": "planejador"
    }
    
    # Calcular pontuações
    for question_id, response in responses.items():
        category = question_categories.get(question_id)
        if category:
            # Algumas perguntas são invertidas (maior valor = menor pontuação)
            if question_id in ["q2", "q6", "q8", "q9", "q10", "q11"]:
                value = 8 - response  # Inverter escala (7 -> 1, 1 -> 7)
            else:
                value = response
            
            categories[category]["sum"] += value
            categories[category]["count"] += 1
    
    # Calcular percentuais
    profile_scores = {}
    for category, data in categories.items():
        if data["count"] > 0:
            # Calcular percentual (0-100%)
            max_possible = data["count"] * 7  # 7 é o valor máximo da escala
            percentage = (data["sum"] / max_possible) * 100
            profile_scores[category] = round(percentage)
        else:
            profile_scores[category] = 0
    
    return profile_scores
