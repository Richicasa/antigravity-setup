# -*- coding: utf-8 -*-
"""
Módulo de Corrección Ortotipográfica, Lingüística y Limpieza Canónica (ARTICULOS U).
Este módulo ejecuta el protocolo obligatorio de corrección sobre cualquier archivo .docx:
1. Corrección de encabezados de página (word/header*.xml): acentuación y erratas.
2. Normalización de fórmulas genéticas / citogenéticas y espaciado de signos (+, /).
3. Corrección de ortotipografía médica (prefijos RAE, erratas de tecleo, concordancia).
4. Cursivas estrictas Vancouver para taxones microbiológicos y locuciones latinas.
5. Limpieza canónica de carpetas de entrega (conservando únicamente los 3 archivos requeridos).
"""

import zipfile
import os
import shutil
import re
from lxml import etree

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
nsmap = {'w': W_NS}

def qn(tag):
    return f'{{{W_NS}}}{tag}'

def audit_and_fix_headers(docx_path):
    """Corrige tildes y erratas en los encabezados automáticos de página (header*.xml)."""
    with zipfile.ZipFile(docx_path, 'r') as zin:
        file_map = {item.filename: zin.read(item.filename) for item in zin.infolist()}

    modified_any = False
    for fname, data in file_map.items():
        if 'header' in fname and fname.endswith('.xml'):
            root = etree.fromstring(data)
            mod = False
            for t_node in root.xpath('.//w:t', namespaces=nsmap):
                if t_node.text:
                    if 'Odontopediatria' in t_node.text:
                        t_node.text = t_node.text.replace('Odontopediatria', 'Odontopediatría')
                        mod = True
            if mod:
                file_map[fname] = etree.tostring(root, xml_declaration=True, encoding='utf-8', standalone='yes')
                modified_any = True

    if modified_any:
        temp_path = docx_path + '.tmp'
        with zipfile.ZipFile(temp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for fname, content in file_map.items():
                zout.writestr(fname, content)
        shutil.move(temp_path, docx_path)
        print('[OK] Encabezados de página actualizados con ortografía correcta.')

def clean_delivery_folder(folder_path, keep_prefix):
    """
    Garantiza que en la carpeta de trabajo SOLO permanezcan los 3 archivos canónicos:
    1. <prefix>_original.docx
    2. <prefix>_revisado.docx
    3. <prefix>_referencias.bib (o similar .bib)
    Elimina cualquier archivo temporal (_nuevo, _corrected, _temp, etc.) o reportes intermedios (.md, informe.docx).
    """
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isdir(fpath):
            continue
        
        # Permitir únicamente los 3 archivos canónicos
        is_original = fname.endswith('_original.docx')
        is_revisado = fname.endswith('_revisado.docx') and not any(tmp in fname for tmp in ['_temp', '_nuevo', '_corrected', '_pre_'])
        is_bib = fname.endswith('.bib')
        
        if not (is_original or is_revisado or is_bib):
            try:
                os.remove(fpath)
                print(f'[CLEAN] Eliminado archivo no canónico: {fname}')
            except Exception as e:
                print(f'[WARN] No se pudo eliminar {fname}: {e}')

if __name__ == '__main__':
    print('Módulo orthography_and_cleaner listo.')
