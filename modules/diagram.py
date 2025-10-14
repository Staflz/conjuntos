import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib_venn import venn2
from modules.utils import format_set


def draw_venn(a, b, labels=("A", "B"), universe=None):
    fig, ax = plt.subplots()
    v = venn2([a, b], set_labels=labels, ax=ax)
    # Mostrar elementos en lugar de conteos
    a_only = a - b
    b_only = b - a
    inter = a & b
    lab_10 = v.get_label_by_id("10")
    lab_01 = v.get_label_by_id("01")
    lab_11 = v.get_label_by_id("11")
    if lab_10 is not None:
        lab_10.set_text(format_set(a_only))
    if lab_01 is not None:
        lab_01.set_text(format_set(b_only))
    if lab_11 is not None:
        lab_11.set_text(format_set(inter))
    
    # Añadir bordes a los círculos
    region_ids = ["10", "01", "11"]
    for rid in region_ids:
        p = v.get_patch_by_id(rid)
        if p is not None:
            p.set_edgecolor("#1e293b")  # Color del borde
            p.set_linewidth(2)  # Grosor del borde
    
    # Dibujar contenedor del Universo si se provee
    if universe is not None:
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        outline = Rectangle((-1.55, -1.45), 3.1, 2.9, fill=False, lw=2, ec="#0ea5e9")
        ax.add_patch(outline)
        # Mostrar solo elementos de U que no están en A ni en B
        u_only = set(universe) - (set(a) | set(b))
        # Colocar etiqueta dentro del rectángulo (ligeramente por debajo del borde superior)
        ax.text(-1.5, 1.42, f"U = {format_set(u_only)}", ha="left", va="top", fontsize=10, color="#0ea5e9")
    return fig


def draw_venn_with_highlight(a, b, op=None, labels=("A", "B"), universe=None):
    """Dibuja Venn y resalta la región asociada a la operación seleccionada.

    op puede ser: None | 'union' | 'inter' | 'diff_a_b' | 'diff_b_a' | 'sym' | 'comp_a' | 'comp_b'
    """
    fig, ax = plt.subplots()
    v = venn2([a, b], set_labels=labels, ax=ax)
    # Mostrar elementos en lugar de conteos
    a_only = a - b
    b_only = b - a
    inter = a & b
    lab_10 = v.get_label_by_id("10")
    lab_01 = v.get_label_by_id("01")
    lab_11 = v.get_label_by_id("11")
    if lab_10 is not None:
        lab_10.set_text(format_set(a_only))
    if lab_01 is not None:
        lab_01.set_text(format_set(b_only))
    if lab_11 is not None:
        lab_11.set_text(format_set(inter))

    # Dibujar contenedor del Universo si se provee (antes de resaltar)
    if universe is not None:
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        outline = Rectangle((-1.55, -1.45), 3.1, 2.9, fill=False, lw=2, ec="#0ea5e9", zorder=1)
        ax.add_patch(outline)
        # Mostrar solo elementos de U que no están en A ni en B
        u_only = set(universe) - (set(a) | set(b))
        # Colocar etiqueta dentro del rectángulo (ligeramente por debajo del borde superior)
        ax.text(-1.5, 1.42, f"U = {format_set(u_only)}", ha="left", va="top", fontsize=10, color="#0ea5e9")

    # Colores base suaves
    region_ids = ["10", "01", "11"]
    for rid in region_ids:
        p = v.get_patch_by_id(rid)
        if p is not None:
            p.set_facecolor("#cbd5e1")
            p.set_alpha(0.3)
            # Añadir bordes a los círculos
            p.set_edgecolor("#1e293b")  # Color del borde
            p.set_linewidth(2)  # Grosor del borde

    def highlight_regions(ids, color="#22c55e", alpha=0.6):
        for rid in ids:
            p = v.get_patch_by_id(rid)
            if p is not None:
                p.set_facecolor(color)
                p.set_alpha(alpha)

    if op is None:
        return fig

    if op == "union":
        highlight_regions(["10", "01", "11"], color="#a78bfa", alpha=0.55)
    elif op == "inter":
        highlight_regions(["11"], color="#f59e0b", alpha=0.7)
    elif op == "diff_a_b":
        highlight_regions(["10"], color="#ef4444", alpha=0.6)
    elif op == "diff_b_a":
        highlight_regions(["01"], color="#3b82f6", alpha=0.6)
    elif op == "sym":
        highlight_regions(["10", "01"], color="#14b8a6", alpha=0.6)
    elif op == "comp_a":
        # Complemento de A: resaltar todo (U) y "recortar" A (10 y 11) usando el mismo tono
        comp_color = "#22c55e"
        ax.add_patch(Rectangle((-1.5, -1.5), 3.0, 3.0, color=comp_color, alpha=0.15, zorder=0))
        for rid in ["10", "11"]:
            p = v.get_patch_by_id(rid)
            if p is not None:
                p.set_facecolor("white")
                p.set_alpha(1.0)
        # Mantener B-only visible como parte del complemento
        p_b_only = v.get_patch_by_id("01")
        if p_b_only is not None:
            p_b_only.set_facecolor(comp_color)
            p_b_only.set_alpha(0.5)
    elif op == "comp_b":
        # Complemento de B: resaltar todo (U) y "recortar" B (01 y 11) usando el mismo tono
        comp_color = "#22c55e"
        ax.add_patch(Rectangle((-1.5, -1.5), 3.0, 3.0, color=comp_color, alpha=0.15, zorder=0))
        for rid in ["01", "11"]:
            p = v.get_patch_by_id(rid)
            if p is not None:
                p.set_facecolor("white")
                p.set_alpha(1.0)
        # Mantener A-only visible como parte del complemento
        p_a_only = v.get_patch_by_id("10")
        if p_a_only is not None:
            p_a_only.set_facecolor(comp_color)
            p_a_only.set_alpha(0.5)

    return fig
