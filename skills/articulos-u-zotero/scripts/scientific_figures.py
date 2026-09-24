import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10.5
plt.rcParams['axes.titlesize'] = 11.5
plt.rcParams['figure.titlesize'] = 13

def generate_prisma_2020(output_file, stats=None):
    """
    Genera un diagrama de flujo PRISMA 2020 oficial en alta resolución (300 DPI).
    stats: diccionario opcional con números de cada etapa:
      {'ident_databases': 394, 'ident_registers': 38, 'duplicates': 122, 'screened': 272,
       'excluded_screen': 208, 'assessed': 64, 'excluded_full': 44, 'included': 20}
    """
    if stats is None:
        stats = {
            'ident_databases': 394,
            'ident_registers': 38,
            'duplicates': 122,
            'screened': 272,
            'excluded_screen': 208,
            'assessed': 64,
            'excluded_full': 44,
            'included': 20
        }

    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_card(x, y, w, h, title, body_lines, is_final=False):
        h_color = '#117A65' if is_final else '#1B4F72'
        h_bg = '#D5F5E3' if is_final else '#D4E6F1'
        b_border = '#1E8449' if is_final else '#2980B9'
        
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8",
                                     facecolor='#F8F9F9', edgecolor=b_border, linewidth=1.5)
        ax.add_patch(card)
        
        header_h = 3.8
        header_y = y + h - header_h
        header_patch = patches.FancyBboxPatch((x + 0.3, header_y), w - 0.6, header_h - 0.3,
                                             boxstyle="round,pad=0.4", facecolor=h_bg, edgecolor='none')
        ax.add_patch(header_patch)
        
        ax.text(x + w/2, header_y + header_h/2 - 0.2, title,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=h_color)
        
        body_start_y = header_y - 1.8
        line_spacing = 2.3
        for i, line in enumerate(body_lines):
            curr_y = body_start_y - (i * line_spacing)
            fw = 'bold' if 'Total' in line or '(n =' in line else 'normal'
            if line.startswith('•') or line.startswith('Total') or line.startswith('(n ='):
                ax.text(x + 2.5, curr_y, line, ha='left', va='center', fontsize=8.5, color='#17202A', fontweight=fw)
            else:
                ax.text(x + w/2, curr_y, line, ha='center', va='center', fontsize=8.5, color='#17202A')

    def draw_down_arrow(x, y_start, y_end):
        ax.annotate('', xy=(x, y_end), xytext=(x, y_start),
                    arrowprops=dict(facecolor='#2C3E50', edgecolor='#2C3E50', width=1.8, headwidth=7, shrink=0.08))

    def draw_right_arrow(x_start, x_end, y):
        ax.annotate('', xy=(x_end, y), xytext=(x_start, y),
                    arrowprops=dict(facecolor='#C0392B', edgecolor='#C0392B', width=1.8, headwidth=7, shrink=0.08))

    def draw_phase(y_center, text):
        tab = patches.FancyBboxPatch((2, y_center - 8), 6, 16, boxstyle="round,pad=0.3",
                                     facecolor='#EAECEE', edgecolor='#BDC3C7', linewidth=1)
        ax.add_patch(tab)
        ax.text(5, y_center, text, fontsize=9.5, fontweight='bold', color='#2C3E50', rotation=90, ha='center', va='center')

    draw_phase(87, "IDENTIFICACIÓN")
    draw_phase(64, "TAMIZAJE")
    draw_phase(41, "ELEGIBILIDAD")
    draw_phase(18, "INCLUSIÓN")

    draw_card(14, 78, 44, 18, "Bases de Datos Consultadas", [
        f"• PubMed / MEDLINE / Embase",
        f"• SciELO / LILACS / Latindex",
        f"• Scopus / Web of Science",
        f"Total registros identificados: n = {stats['ident_databases']}"
    ])
    draw_right_arrow(58, 64, 87)
    draw_card(64, 78, 38, 18, "Depuración de Duplicados", [
        "Registros duplicados eliminados:",
        f"• Duplicados exactos / por DOI",
        "",
        f"Total depurados: n = {stats['duplicates']}"
    ])
    draw_down_arrow(36, 78, 71)

    draw_card(14, 54, 44, 17, "Cribado de Títulos y Resúmenes", [
        "Registros cribados por pertinencia",
        f"temática y metodológica (n = {stats['screened']})"
    ])
    draw_right_arrow(58, 64, 62.5)
    draw_card(64, 52, 38, 20, "Registros Excluidos en Cribado", [
        f"Excluidos con justificación (n = {stats['excluded_screen']}):",
        "• Temática no coincidente",
        "• Población o diseño no elegible",
        "• Sin datos clínicos pertinentes"
    ])
    draw_down_arrow(36, 54, 48)

    draw_card(14, 32, 44, 16, "Evaluación a Texto Completo", [
        "Artículos evaluados a texto completo",
        f"para criterios de elegibilidad (n = {stats['assessed']})"
    ])
    draw_right_arrow(58, 64, 40)
    draw_card(64, 30, 38, 20, "Artículos Excluidos a Texto Completo", [
        f"Excluidos con justificación (n = {stats['excluded_full']}):",
        "• Criterios metodológicos no cumplidos",
        "• Rango etario o muestra inadecuada",
        "• Reportes de caso aislados"
    ])
    draw_down_arrow(36, 32, 25)

    draw_card(14, 9, 44, 16, "Estudios Incluidos en la Síntesis", [
        "Estudios clínicos y epidemiológicos",
        "incluidos en la síntesis cuali/cuantitativa",
        f"Total incluidos: n = {stats['included']} estudios"
    ], is_final=True)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Diagrama PRISMA 2020 generado en: {output_file}")

def generate_comparative_bars(output_file, categories, values, title, xlabel, ylabel):
    """
    Genera un gráfico de barras comparativo horizontal o vertical en 300 DPI.
    """
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    y_pos = np.arange(len(categories))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(categories)))[::-1]
    
    bars = ax.barh(y_pos, values, color=colors, edgecolor='#1B2631', linewidth=0.8, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=9.5)
    max_val = max(values) * 1.25 if values else 100
    ax.set_xlim(0, max_val)
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=10)
    ax.set_title(title, fontweight='bold', fontsize=11.5, pad=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.invert_yaxis()
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + (max_val * 0.02), bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=9, fontweight='bold')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfico comparativo generado en: {output_file}")
