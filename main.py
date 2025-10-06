from altair.utils.schemapi import disable_debug_mode
import streamlit as st
from modules import utils

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Operaciones con Conjuntos",
    layout="wide",
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
<style>
.stAppViewContainer {
    background: linear-gradient(0deg, #3c0d7d 0%, #0b0f1a 60%) !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Título principal */
.main-title {
    color: #1e293b;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.2rem;
}
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 4rem;
}

/* Inputs */
.stTextInput>div>div>input {
    border-radius: 10px;
    border: 2px solid #cbd5e1;
    background-color: white;
    font-size: 1.5rem;
    font-weight:700;
    color: #1e293b;
    padding: 1rem;
    transition: all 0.2s ease;
}
.stTextInput>div>div>input:focus {
    border-color: #818cf8;
    box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
}

/* Sección encabezado */
.section-header {
    color: #334155;
    font-size: 1.2rem;
    font-weight: 600;
    border-bottom: 2px solid #818cf8;
    padding-bottom: 0.3rem;
    margin-bottom: 2rem;
}

/* Tabs como texto */
[data-baseweb="tab-list"] {
    justify-content: center;
    gap: 1rem;
}
[data-baseweb="tab"] {
    background: none !important;
    border: none !important;
    color: #475569 !important;
    font-weight: 600;
    padding: 0.5rem 1rem !important;
    border-bottom: 2px solid transparent;
}
[data-baseweb="tab"]:hover {
    color: #3730a3 !important;
    border-bottom: 2px solid #a78bfa;
}
[aria-selected="true"] {
    color: #4f46e5 !important;
    border-bottom: 2px solid #4f46e5 !important;
}

/* Botones */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
    color: white;
    border: none;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(129, 140, 248, 0.4);
}

/* Ocultar elementos por defecto */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

for k in ["u", "a", "b", "s"]:
    st.session_state.setdefault(k, "")

col_icon1, _ = st.columns([0.05, 2])
with col_icon1:
    if st.button("🧹", help="Limpiar todos los campos"):
        st.session_state["u"] = ""
        st.session_state["a"] = ""
        st.session_state["b"] = ""
        st.session_state["s"] = ""

# --- HEADER ---
st.markdown('<h1 class="main-title"> Operaciones con Conjuntos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"> <i> Visualiza y calcula operaciones entre conjuntos de forma interactiva </i> </p>', unsafe_allow_html=True)

# --- INPUTS ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("### 🌐 Conjunto Universal")
    st.text_input("Conjunto U", placeholder="Ej: 1,2,3,4,5,6", label_visibility="collapsed", key="u")

with col2:
    st.markdown("### 🔴 Conjunto A")
    st.text_input("Conjunto A", placeholder="Ej: 1,3,5", label_visibility="collapsed", key="a")
    st.caption("💡Ingresa los elementos separados por comas y selecciona una operación para ver su resultado.")

with col3:
    st.markdown("### 🔵 Conjunto B")
    st.text_input("Conjunto B", placeholder="Ej: 2,4,6", label_visibility="collapsed", key="b")

# --- OPERACIONES ---
st.markdown('<h2 class="section-header"> Selecciona la Operación</h2>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🔗 Básicas", "🔄 Diferencias", "💫 Complementos"])

with tab1:
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.button("➕ A ∪ B", use_container_width=True, key="union")
    with col2:
        st.button("✖️ A ∩ B ", use_container_width=True, key="inter")


with tab2:
    col3, col4, col5 = st.columns(3, gap="medium")
    with col3:
        st.button("➖ A - B", use_container_width=True, key="a_b")
    with col4:
        st.button("➖ B - A", use_container_width=True, key="b_a")
    with col5:
        st.button("➖ A △ B", use_container_width=True, key="sym")

with tab3:
    col6, col7 = st.columns(2, gap="medium")
    with col6:
        st.button("🔴 A' ", use_container_width=True, key="comp_a")
    with col7:
        st.button("🔵 B' ", use_container_width=True, key="comp_b")


# --- CONJUNTO SOLUCIÓN ---

st.markdown('<h3 style="color:white; margin-top:2rem; font-weight:550;"> 📦 Conjunto solución</h3>', unsafe_allow_html=True)
st.text_input("Solución", placeholder="Ej: 2,4,6", label_visibility="collapsed", key="s", disabled=True)

# --- DIAGRAMA DE VENN ---
st.markdown('<h2 style="color:white; margin-top:2rem; font-weight:550;"> Diagrama de Venn</h2>', unsafe_allow_html=True)




