import html
import json
import random
import string
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn

def get_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def build_csl_citation_json(citation_indices, citation_str, studies_data):
    """
    Construye el payload CSL-JSON requerido por Zotero para un campo dinámico de cita.
    """
    citation_id = get_random_id(8)
    citation_items = []
    
    for idx in citation_indices:
        if idx <= len(studies_data):
            s = studies_data[idx - 1]
            csl_item_data = {
                "id": s.get("id", idx),
                "type": "article-journal",
                "title": s.get("title", ""),
                "container-title": s.get("journal", ""),
                "volume": s.get("volume", ""),
                "issue": s.get("issue", ""),
                "page": s.get("pages", ""),
                "DOI": s.get("doi", ""),
                "abstract": s.get("abstract", "")
            }
            if s.get("year"):
                try:
                    year_int = int(str(s["year"])[:4])
                    csl_item_data["issued"] = {"date-parts": [[year_int]]}
                except ValueError:
                    pass
                    
            z_key = s.get("zotero_key", f"ITEM{idx:03d}")
            c_item = {
                "id": s.get("id", idx),
                "uris": [f"http://zotero.org/users/local/0/items/{z_key}"],
                "itemData": csl_item_data
            }
            citation_items.append(c_item)
            
    csl_dict = {
        "citationID": citation_id,
        "properties": {
            "formattedCitation": citation_str,
            "plainCitation": citation_str,
            "dontUpdate": False,
            "noteIndex": 0
        },
        "citationItems": citation_items,
        "schema": "https://github.com/citation-style-language/schema/raw/master/csl-citation.json"
    }
    return json.dumps(csl_dict, ensure_ascii=False)

def add_zotero_live_citation(paragraph, citation_indices, citation_str, studies_data, color_rgb="1B4F72", bold=True):
    """
    Inserta un campo dinámico de Word (<w:fldSimple w:instr=" ADDIN ZOTERO_ITEM ... ">)
    en el párrafo especificado. En Microsoft Word con Zotero instalado, se reconoce como cita activa.
    """
    csl_json = build_csl_citation_json(citation_indices, citation_str, studies_data)
    escaped_instr = f' ADDIN ZOTERO_ITEM {html.escape(csl_json)} '
    
    bold_tag = "<w:b/>" if bold else ""
    fld_xml = f'''
    <w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="{escaped_instr}">
        <w:r>
            <w:rPr>
                <w:rStyle w:val="ZoteroIn-TextCitation"/>
                <w:color w:val="{color_rgb}"/>
                {bold_tag}
            </w:rPr>
            <w:t>{citation_str}</w:t>
        </w:r>
    </w:fldSimple>
    '''
    paragraph._p.append(parse_xml(fld_xml))

def add_zotero_bibliography(doc, formatted_references):
    """
    Inserta el bloque de bibliografía dinámica de Zotero (<w:fldSimple w:instr=" ADDIN ZOTERO_BIBL ... ">).
    """
    csl_bibl_dict = {"uncited": [], "omitted": [], "custom": []}
    escaped_instr = f' ADDIN ZOTERO_BIBL {html.escape(json.dumps(csl_bibl_dict))} CSL_BIBLIOGRAPHY '
    
    for ref_text in formatted_references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        
        fld_xml = f'''
        <w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="{escaped_instr}">
            <w:r>
                <w:rPr><w:rStyle w:val="ZoteroBibliography"/></w:rPr>
                <w:t>{html.escape(ref_text)}</w:t>
            </w:r>
        </w:fldSimple>
        '''
        p_ref._p.append(parse_xml(fld_xml))

def setup_academic_document_style(doc):
    """
    Configura márgenes, tipografía base e interlineado para un artículo científico de alto impacto.
    """
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

def add_styled_heading(doc, text, level=1):
    h = doc.add_heading(level=level)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.bold = True
    if level == 1:
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r.font.size = Pt(13.5)
        r.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)
    elif level == 2:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(0x28, 0x74, 0xA6)
    else:
        h.paragraph_format.space_before = Pt(6)
        h.paragraph_format.space_after = Pt(2)
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x17, 0x20, 0x2A)
    return h
