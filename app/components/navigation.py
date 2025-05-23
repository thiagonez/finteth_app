import streamlit as st

def navigation_buttons(prev_page=None, next_page=None, prev_label="Anterior", next_label="Próximo"):
    """
    Componente para botões de navegação entre páginas
    
    Args:
        prev_page (str, optional): Nome da página anterior
        next_page (str, optional): Nome da página seguinte
        prev_label (str, optional): Texto do botão anterior
        next_label (str, optional): Texto do botão próximo
    """
    cols = st.columns([1, 1, 1])
    
    with cols[0]:
        if prev_page:
            if st.button(f"← {prev_label}", key="btn_prev"):
                st.session_state.current_page = prev_page
                st.experimental_rerun()
    
    with cols[2]:
        if next_page:
            if st.button(f"{next_label} →", key="btn_next"):
                st.session_state.current_page = next_page
                st.experimental_rerun()
