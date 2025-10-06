import matplotlib.pyplot as plt
from matplotlib_venn import venn2

def draw_venn(a, b, labels=('A', 'B')):
    fig, ax = plt.subplots()
    venn2([a, b], set_labels=labels, ax=ax)
    return fig
