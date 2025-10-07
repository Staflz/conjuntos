import streamlit as st
from modules import utils
from modules.operations import (
    parse_set,
    operate_binary_by_universe,
    operate_unary_by_universe,
)
from modules.diagram import draw_venn

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

/* Alertas intrusivas superiores */
.alert-banner {
    position: sticky;
    top: 0;
    z-index: 9999;
    padding: 14px 18px;
    border-radius: 10px;
    margin: 0 0 14px 0;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.alert-error {
    background: linear-gradient(135deg, #ef4444, #b91c1c);
    color: #fff;
}
.alert-warning {
    background: linear-gradient(135deg, #f59e0b, #b45309);
    color: #111827;
}
 .alert-success {
     background: linear-gradient(135deg, #22c55e, #15803d);
     color: #fff;
 }
.alert-icon {
    font-size: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

for k in ["u", "a", "b", "s"]:
    st.session_state.setdefault(k, "")
st.session_state.setdefault("alerts", [])
# Reservar contenedor superior para alertas y llenarlo al final
alert_container = st.empty()

def add_alert(message: str, level: str = "error"):
    # level: "error" | "warning"
    st.session_state["alerts"].append({"message": message, "level": level})

def render_alerts(container):
    alerts = st.session_state.get("alerts", [])
    if not alerts:
        container.empty()
        return
    html_blocks = []
    for alert in alerts:
        level = alert.get("level", "error")
        cls = "alert-error" if level == "error" else "alert-warning"
        icon = "🚫" if level == "error" else "⚠️"
        html_blocks.append(
            f'<div class="alert-banner {cls}"><span class="alert-icon">{icon}</span><span>{alert.get("message","")}</span></div>'
        )
    container.markdown("\n".join(html_blocks), unsafe_allow_html=True)
    # limpiar alertas tras mostrarlas para que no persistan en cada rerun
    st.session_state["alerts"] = []

# --- HEADER ---
st.markdown('<h1 class="main-title"> Operaciones con Conjuntos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"> <i> Visualiza y calcula operaciones entre conjuntos de forma interactiva </i> </p>', unsafe_allow_html=True)

# Botón limpiar arriba a la derecha bajo el título
_col_a, _col_b = st.columns([3, 1])
with _col_b:
    if st.button("🧹 Limpiar", use_container_width=True, help="Limpiar todos los campos"):
        st.session_state["u"] = ""
        st.session_state["a"] = ""
        st.session_state["b"] = ""
        st.session_state["s"] = ""
        # mostrar confirmación arriba
        add_alert("Campos limpiados correctamente.", "success")

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


# --- DIAGRAMA DE VENN ---
st.markdown('<h2 style="color:white; margin-top:2rem; font-weight:550;"> Diagrama de Venn</h2>', unsafe_allow_html=True)

# --- LÓGICA ---
def try_parse_inputs():
    """Intenta convertir los textos a conjuntos. Devuelve (u, a, b) o None si hay error."""
    try:
        u = parse_set(st.session_state.get("u", ""))
        a = parse_set(st.session_state.get("a", ""))
        b = parse_set(st.session_state.get("b", ""))
        return u, a, b
    except ValueError as e:
        add_alert(str(e), "error")
        return None


def validate_no_duplicates():
    dup_u = utils.find_duplicates_in_csv(st.session_state.get("u", ""))
    dup_a = utils.find_duplicates_in_csv(st.session_state.get("a", ""))
    dup_b = utils.find_duplicates_in_csv(st.session_state.get("b", ""))
    if dup_u:
        add_alert(f"U contiene elementos repetidos: {', '.join(sorted(dup_u))}", "warning")
    if dup_a:
        add_alert(f"A contiene elementos repetidos: {', '.join(sorted(dup_a))}", "warning")
    if dup_b:
        add_alert(f"B contiene elementos repetidos: {', '.join(sorted(dup_b))}", "warning")
    return not (dup_u or dup_a or dup_b)


def validate_membership(u, a, b):
    not_in_u_a = utils.elements_not_in_universe(u, a)
    not_in_u_b = utils.elements_not_in_universe(u, b)
    if not_in_u_a:
        add_alert(f"Elementos de A que no pertenecen a U: {utils.format_set(not_in_u_a)}", "error")
    if not_in_u_b:
        add_alert(f"Elementos de B que no pertenecen a U: {utils.format_set(not_in_u_b)}", "error")
    return not (not_in_u_a or not_in_u_b)


def update_solution(result_set):
    formatted = utils.format_set(result_set)
    st.session_state["s"] = formatted
    # mantener sincronizado el widget si ya existe
    st.session_state["s_widget"] = formatted


# Validaciones visuales tempranas
validate_no_duplicates()


def on_click_operation(op):
    parsed = try_parse_inputs()
    if not parsed:
        return
    u, a, b = parsed
    if not validate_no_duplicates():
        return
    if not validate_membership(u, a, b):
        return
    # Usar la versión basada en universo para alinear con la lógica Java
    if op == "union":
        update_solution(operate_binary_by_universe(u, a, b, 'union'))
    elif op == "inter":
        update_solution(operate_binary_by_universe(u, a, b, 'inter'))
    elif op == "a_b":
        update_solution(operate_binary_by_universe(u, a, b, 'diff_a_b'))
    elif op == "b_a":
        update_solution(operate_binary_by_universe(u, a, b, 'diff_b_a'))
    elif op == "sym":
        update_solution(operate_binary_by_universe(u, a, b, 'sym'))
    elif op == "comp_a":
        update_solution(operate_unary_by_universe(u, a, 'comp'))
    elif op == "comp_b":
        update_solution(operate_unary_by_universe(u, b, 'comp'))


# Disparar operaciones según clic
if st.session_state.get("union"):
    on_click_operation("union")
if st.session_state.get("inter"):
    on_click_operation("inter")
if st.session_state.get("a_b"):
    on_click_operation("a_b")
if st.session_state.get("b_a"):
    on_click_operation("b_a")
if st.session_state.get("sym"):
    on_click_operation("sym")
if st.session_state.get("comp_a"):
    on_click_operation("comp_a")
if st.session_state.get("comp_b"):
    on_click_operation("comp_b")


# --- CONJUNTO SOLUCIÓN ---
st.markdown('<h3 style="color:white; margin-top:2rem; font-weight:550;"> 📦 Conjunto solución</h3>', unsafe_allow_html=True)
st.text_input(
    "Solución",
    placeholder="Ej: 2,4,6",
    label_visibility="collapsed",
    value=st.session_state.get("s", ""),
    key="s_widget",
)

# Diagrama
parsed_inputs = try_parse_inputs()
if parsed_inputs:
    u, a, b = parsed_inputs
    fig = draw_venn(a, b, labels=("A", "B"))
    st.pyplot(fig, use_container_width=True)

# Renderizar alertas al final del ciclo para asegurar visibilidad inmediata
render_alerts(alert_container)
