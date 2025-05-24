import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from components.navigation import navigation_buttons

def show():
    """Página de questionário comportamental"""
    
    # CSS para botões verticais com cores específicas
    st.markdown("""
    <style>
        /* Container dos radio buttons vertical */
        div[role=radiogroup] {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 20px 0;
        }
        
        /* Cada label do radio button */
        div[role=radiogroup] label {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            border-radius: 25px;
            border: 2px solid;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        /* Estilizar as bolinhas dos radio buttons */
        div[role=radiogroup] label div:first-child {
            margin-right: 10px;
            transform: scale(1.2);
        }
        
        /* Botões de Discordo (roxo) - posições 1, 2, 3 */
        div[role=radiogroup] label:nth-child(1),
        div[role=radiogroup] label:nth-child(2),
        div[role=radiogroup] label:nth-child(3) {
            border-color: #8B5A96;
            background-color: #F8F5F9;
        }
        
        div[role=radiogroup] label:nth-child(1) input[type="radio"],
        div[role=radiogroup] label:nth-child(2) input[type="radio"],
        div[role=radiogroup] label:nth-child(3) input[type="radio"] {
            accent-color: #8B5A96;
        }
        
        /* Botão Neutro (cinza e menor) - posição 4 */
        div[role=radiogroup] label:nth-child(4) {
            border-color: #9E9E9E;
            background-color: #F5F5F5;
            transform: scale(0.9);
        }
        
        div[role=radiogroup] label:nth-child(4) input[type="radio"] {
            accent-color: #9E9E9E;
        }
        
        /* Botões de Concordo (verde) - posições 5, 6, 7 */
        div[role=radiogroup] label:nth-child(5),
        div[role=radiogroup] label:nth-child(6),
        div[role=radiogroup] label:nth-child(7) {
            border-color: #4CAF50;
            background-color: #F1F8E9;
        }
        
        div[role=radiogroup] label:nth-child(5) input[type="radio"],
        div[role=radiogroup] label:nth-child(6) input[type="radio"],
        div[role=radiogroup] label:nth-child(7) input[type="radio"] {
            accent-color: #4CAF50;
        }
        
        /* Efeito hover */
        div[role=radiogroup] label:hover {
            transform: scale(1.02);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Neutro mantém tamanho menor no hover */
        div[role=radiogroup] label:nth-child(4):hover {
            transform: scale(0.92);
        }
        
        /* Estilo quando selecionado */
        div[role=radiogroup] label:has(input[type="radio"]:checked) {
            font-weight: bold;
            transform: scale(1.05);
        }
        
        /* Neutro selecionado mantém tamanho menor */
        div[role=radiogroup] label:nth-child(4):has(input[type="radio"]:checked) {
            transform: scale(0.95);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Questionário Comportamental</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-container">
        <p>Responda com sinceridade para obter resultados mais precisos.</p>
        <p>Selecione a opção que melhor representa sua opinião.</p>
    </div>
    """, unsafe_allow_html=True)

    # Opções com labels completos
    opcoes = [
        "Discordo totalmente",
        "Discordo moderadamente", 
        "Discordo um pouco",
        "Nem concordo nem discordo",
        "Concordo um pouco",
        "Concordo moderadamente",
        "Concordo totalmente"
    ]
# Inicializar respostas
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
    
    
    
    
    
    # Configuração de paginação
    questions_per_page = 3
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.get('questionnaire_page', 1)

    # Barra de progresso
    progress = (current_page - 1) / total_pages
    st.progress(progress)
    st.markdown(f"<p>Etapa {current_page} de {total_pages}</p>", unsafe_allow_html=True)

    # Exibir perguntas
    start_idx = (current_page - 1) * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions))
    
    for i in range(start_idx, end_idx):
        question = questions[i]
        
        with st.container():
            st.markdown(f"**Pergunta {i+1}:** {question['text']}")
            
            # Radio buttons verticais com cores
            response = st.radio(
                label=f"Resposta {i+1}",
                options=opcoes,
                key=f"question_{i}",
                label_visibility="collapsed"
            )
            
            # Converter resposta para número (1-7)
            response_value = opcoes.index(response) + 1
            st.session_state.question_responses[question["id"]] = response_value
            
            st.markdown("---")

    # Botões de navegação
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_page > 1 and st.button("← Anterior"):
            st.session_state.questionnaire_page -= 1
            st.rerun()
    
    with col3:
        if current_page < total_pages and st.button("Próximo →"):
            st.session_state.questionnaire_page += 1
            st.rerun()
        elif current_page == total_pages and st.button("Finalizar Questionário"):
            st.session_state.questionnaire_completed = True
            st.session_state.current_page = "dashboard"
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
