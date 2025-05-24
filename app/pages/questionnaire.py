import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from components.navigation import navigation_buttons

def show():
    """Página de questionário comportamental com botões de rádio estilizados"""

    # CSS para estilizar os botões de rádio horizontais
    st.markdown("""
    <style>
        div[role=radiogroup] {
            display: flex;
            flex-wrap: nowrap;
            overflow-x: auto;
            gap: 8px;
            padding: 8px 0;
        }
        div[role=radiogroup] label {
            flex: 0 0 auto;
            min-width: 180px;
            text-align: center;
            padding: 8px 12px;
            border-radius: 20px;
            border: 2px solid #4F8BF9;
            cursor: pointer;
            transition: all 0.2s;
        }
        div[role=radiogroup] label:hover {
            background-color: #4F8BF9;
            color: white;
        }
        div[role=radiogroup] input[type=radio] {
            display: none;
        }
        div[role=radiogroup] input[type=radio]:checked + span {
            background-color: #4F8BF9;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Questionário Comportamental</h1>", unsafe_allow_html=True)

    # Opções de resposta com labels completos
    opcoes = {
        1: "Discordo totalmente",
        2: "Discordo moderadamente",
        3: "Discordo um pouco",
        4: "Nem concordo nem discordo",
        5: "Concordo um pouco",
        6: "Concordo moderadamente",
        7: "Concordo totalmente"
    }

    # Inicializar respostas na sessão
    if "question_responses" not in st.session_state:
        st.session_state.question_responses = {}
    

    
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
    
     # Paginação
    questions_per_page = 3
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.get('questionnaire_page', 1)

    start_idx = (current_page - 1) * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions))

    for i in range(start_idx, end_idx):
        question = questions[i]
        st.markdown(f"**Pergunta {i+1}:** {question['text']}")

        # Layout horizontal com botões de rádio estilizados
        cols = st.columns([1, 4, 1])
        with cols[0]:
            st.markdown("<div style='text-align: right; color: #FF4B4B;'>Discordo</div>", unsafe_allow_html=True)
        with cols[1]:
            response = st.radio(
                "",
                options=list(opcoes.keys()),
                format_func=lambda x: opcoes[x],
                index=3,
                key=f"question_{question['id']}",
                label_visibility="collapsed"
            )
            st.session_state.question_responses[question['id']] = response
        with cols[2]:
            st.markdown("<div style='text-align: left; color: #4F8BF9;'>Concordo</div>", unsafe_allow_html=True)

    # Botões de navegação
    col1, col2, col3 = st.columns([1, 1, 1])
    if current_page > 1 and st.button("← Anterior"):
        st.session_state['questionnaire_page'] = current_page - 1
        st.rerun()

    if current_page < total_pages and st.button("Próximo →"):
        st.session_state['questionnaire_page'] = current_page + 1
        st.rerun()

    if current_page == total_pages and st.button("Finalizar Questionário"):
        st.session_state['questionnaire_completed'] = True
        st.session_state['current_page'] = "dashboard"
        st.rerun()

    navigation_buttons()
    
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
