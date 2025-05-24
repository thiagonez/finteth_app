import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from components.navigation import navigation_buttons

def load_custom_radio_css():
    """Carrega CSS customizado para os radio buttons do questionário"""
    st.markdown("""
    <style>
    /* Ocultar completamente radio buttons padrão */
    div[role="radiogroup"] input[type="radio"] {
        appearance: none !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        position: absolute;
        opacity: 0;
        width: 0;
        height: 0;
        margin: 0;
        padding: 0;
        border: none;
        background: none;
    }
    
    /* Remover TODOS os pseudo-elementos padrão */
    div[role="radiogroup"] input[type="radio"]::before,
    div[role="radiogroup"] input[type="radio"]::after {
        display: none !important;
        content: none !important;
    }
    
    /* Container dos radio buttons */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    /* Estilo base dos círculos */
    div[role="radiogroup"] label {
        cursor: pointer;
        margin: 0 !important;
        position: relative;
    }
    
    /* Ocultar textos dos labels */
    div[role="radiogroup"] label > div:last-child {
        display: none !important;
    }
    
    /* Círculos customizados - LIMPOS sem bolinha */
    div[role="radiogroup"] label > div:first-child {
        border-radius: 50% !important;
        border: 3px solid;
        display: flex !important;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: all 0.3s ease;
        background-color: transparent !important;
        cursor: pointer;
        /* IMPORTANTE: Remover qualquer conteúdo padrão */
        content: none !important;
    }
    
    /* Remover TODOS os pseudo-elementos das divs também */
    div[role="radiogroup"] label > div:first-child::before,
    div[role="radiogroup"] label > div:first-child::after {
        display: none !important;
        content: none !important;
    }
    
    /* Tamanhos e cores específicos para cada opção */
    /* Opção 1 - Verde muito grande */
    div[role="radiogroup"] label:nth-child(1) > div:first-child {
        width: 60px;
        height: 60px;
        border-color: #10B981;
    }
    
    /* Opção 2 - Verde grande */
    div[role="radiogroup"] label:nth-child(2) > div:first-child {
        width: 50px;
        height: 50px;
        border-color: #34D399;
    }
    
    /* Opção 3 - Verde menor */
    div[role="radiogroup"] label:nth-child(3) > div:first-child {
        width: 40px;
        height: 40px;
        border-color: #6EE7B7;
    }
    
    /* Opção 4 - Cinza pequeno (Neutro) */
    div[role="radiogroup"] label:nth-child(4) > div:first-child {
        width: 30px;
        height: 30px;
        border-color: #6B7280;
    }
    
    /* Opção 5 - Roxo menor */
    div[role="radiogroup"] label:nth-child(5) > div:first-child {
        width: 40px;
        height: 40px;
        border-color: #C084FC;
    }
    
    /* Opção 6 - Roxo grande */
    div[role="radiogroup"] label:nth-child(6) > div:first-child {
        width: 50px;
        height: 50px;
        border-color: #A855F7;
    }
    
    /* Opção 7 - Roxo muito grande */
    div[role="radiogroup"] label:nth-child(7) > div:first-child {
        width: 60px;
        height: 60px;
        border-color: #8B5CF6;
    }
    
    /* HOVER - Preenchimento SEM bolinha, apenas com check */
    div[role="radiogroup"] label:nth-child(1):hover > div:first-child {
        background-color: #10B981 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(2):hover > div:first-child {
        background-color: #34D399 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(3):hover > div:first-child {
        background-color: #6EE7B7 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(110, 231, 183, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(4):hover > div:first-child {
        background-color: #6B7280 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(107, 114, 128, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(5):hover > div:first-child {
        background-color: #C084FC !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(192, 132, 252, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(6):hover > div:first-child {
        background-color: #A855F7 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
    }
    
    div[role="radiogroup"] label:nth-child(7):hover > div:first-child {
        background-color: #8B5CF6 !important;
        transform: scale(1.05);
        border-width: 4px;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Check no hover - APENAS quando hover */
    div[role="radiogroup"] label:hover > div:first-child::after {
        content: "✓" !important;
        color: white !important;
        font-weight: bold;
        font-size: 16px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        z-index: 10;
        display: block !important;
    }
    
    /* Estados SELECIONADOS - preenchimento COMPLETO SEM bolinha */
    div[role="radiogroup"] label:nth-child(1) input[type="radio"]:checked + div {
        background-color: #10B981 !important;
        border-color: #10B981 !important;
    }
    
    div[role="radiogroup"] label:nth-child(2) input[type="radio"]:checked + div {
        background-color: #34D399 !important;
        border-color: #34D399 !important;
    }
    
    div[role="radiogroup"] label:nth-child(3) input[type="radio"]:checked + div {
        background-color: #6EE7B7 !important;
        border-color: #6EE7B7 !important;
    }
    
    div[role="radiogroup"] label:nth-child(4) input[type="radio"]:checked + div {
        background-color: #6B7280 !important;
        border-color: #6B7280 !important;
    }
    
    div[role="radiogroup"] label:nth-child(5) input[type="radio"]:checked + div {
        background-color: #C084FC !important;
        border-color: #C084FC !important;
    }
    
    div[role="radiogroup"] label:nth-child(6) input[type="radio"]:checked + div {
        background-color: #A855F7 !important;
        border-color: #A855F7 !important;
    }
    
    div[role="radiogroup"] label:nth-child(7) input[type="radio"]:checked + div {
        background-color: #8B5CF6 !important;
        border-color: #8B5CF6 !important;
    }
    
    /* Check quando SELECIONADO - APENAS o check, sem bolinha */
    div[role="radiogroup"] input[type="radio"]:checked + div::after {
        content: "✓" !important;
        color: white !important;
        font-weight: bold;
        font-size: 18px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        z-index: 10;
        display: block !important;
    }
    
    /* Garantir que não apareça check quando selecionado E com hover */
    div[role="radiogroup"] input[type="radio"]:checked + div:hover::after {
        content: "✓" !important;
        font-size: 18px !important;
        opacity: 1 !important;
    }
    
    /* Responsividade para dispositivos móveis */
    @media (max-width: 768px) {
        div[role="radiogroup"] {
            gap: 10px;
        }
        
        div[role="radiogroup"] label > div:first-child {
            transform: scale(0.8);
        }
    }
    
    /* Melhorar acessibilidade - foco por teclado */
    div[role="radiogroup"] input[type="radio"]:focus + div {
        outline: 3px solid #3B82F6;
        outline-offset: 2px;
    }
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
    
    # Configurações de paginação
    if 'questionnaire_page' not in st.session_state:
        st.session_state.questionnaire_page = 1
    if 'question_responses' not in st.session_state:
        st.session_state.question_responses = {}

    questions_per_page = 5
    total_pages = len(questions) // questions_per_page + (1 if len(questions) % questions_per_page > 0 else 0)
    current_page = st.session_state.questionnaire_page

    st.markdown(f"<h4 style='text-align: center;'>Etapa {current_page} de {total_pages}</h4>", unsafe_allow_html=True)

    # Exibir perguntas da página atual - SEÇÃO CORRIGIDA
    start_idx = (current_page - 1) * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions))

    # IMPORTANTE: Todo este bloco deve estar DENTRO da função show()
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

    # Botões de navegação
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
