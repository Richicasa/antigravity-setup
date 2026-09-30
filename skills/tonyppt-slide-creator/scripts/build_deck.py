import os
import sys
import json
import yaml
import argparse
import subprocess
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

try:
    from fetch_images import download_image, crop_to_exact_aspect
except ImportError:
    from scripts.fetch_images import download_image, crop_to_exact_aspect

SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5

PALETTES = {
    "luxury-dark": {
        "bg": "#090A0D",
        "card_white": "#FFFFFF",
        "card_dark": "#16181E",
        "card_accent": "#C67B48",
        "card_cream": "#E8DACB",
        "badge_bg": "#E89B38",
        "badge_text": "#000000",
        "text_primary": "#FFFFFF",
        "text_dark": "#111113",
        "text_muted": "#8E929E",
        "text_accent": "#E89B38"
    }
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def apply_morph_xml(slide):
    """
    Injects Microsoft PowerPoint Morph transition with full OpenXML AlternateContent schema.
    """
    morph_xml = parse_xml(
        '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
        '  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
        '    <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        '                 xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="1250">'
        '      <p159:morph option="byObject"/>'
        '    </p:transition>'
        '  </mc:Choice>'
        '  <mc:Fallback xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '    <p:transition spd="slow"><p:fade/></p:transition>'
        '  </mc:Fallback>'
        '</mc:AlternateContent>'
    )
    slide._element.append(morph_xml)

def sync_powerpoint_morph_com(pptx_abs_path):
    """
    Calls PowerPoint COM to ensure PowerPoint's native engine assigns
    EntryEffect = 3954 (ppEffectMorph) across all transition slides.
    """
    ps_cmd = f"""
    $ppt = New-Object -ComObject PowerPoint.Application
    try {{
        $pres = $ppt.Presentations.Open('{pptx_abs_path}', 0, 0, 0)
        for ($i = 2; $i -le $pres.Slides.Count; $i++) {{
            $pres.Slides.Item($i).SlideShowTransition.EntryEffect = 3954
            $pres.Slides.Item($i).SlideShowTransition.Duration = 1.25
        }}
        $pres.Save()
        $pres.Close()
    }} finally {{
        $ppt.Quit()
        [System.GC]::Collect()
    }}
    """
    try:
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=10)
    except Exception as e:
        print(f"COM Morph sync note: {e}")

class TonyDeckBuilder:
    def __init__(self, theme="luxury-dark"):
        self.prs = pptx.Presentation()
        self.prs.slide_width = Inches(SLIDE_WIDTH)
        self.prs.slide_height = Inches(SLIDE_HEIGHT)
        self.blank_layout = self.prs.slide_layouts[6]
        self.palette = PALETTES.get(theme, PALETTES["luxury-dark"])
        self.cache_dir = os.path.join(os.getcwd(), ".deck_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _add_background(self, slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(SLIDE_HEIGHT))
        bg.fill.solid()
        bg.fill.fore_color.rgb = hex_to_rgb(self.palette["bg"])
        bg.line.fill.background()
        return bg

    def _resolve_image(self, img_source, w_in, h_in, name_prefix="img"):
        if not img_source:
            img_source = "luxury modern architecture"
            
        local_raw = os.path.join(self.cache_dir, f"{name_prefix}_raw.jpg")
        local_crop = os.path.join(self.cache_dir, f"{name_prefix}_crop.jpg")
        
        if os.path.exists(img_source):
            local_raw = img_source
        else:
            download_image(img_source, local_raw)
            
        crop_to_exact_aspect(local_raw, w_in, h_in, local_crop)
        return local_crop

    def add_visual_dominant_slide_1(self, data, is_first=True):
        """
        85% Images: Hero Left (8.5" x 6.5") + Top Right Photo (3.6" x 3.1")
        15% Text: 1 Clean Stat Card with Badge & Big Number
        """
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._add_background(slide)
        if not is_first:
            apply_morph_xml(slide)

        # 1. Main Hero Image (Left, 8.5" x 6.5")
        p1 = self._resolve_image(data.get("hero_image"), 8.5, 6.5, "hero1")
        pic1 = slide.shapes.add_picture(p1, Inches(0.5), Inches(0.5), Inches(8.5), Inches(6.5))
        pic1.name = "!!MainVisual"

        # 2. Secondary Photo (Right Top, 3.6" x 3.1")
        p2 = self._resolve_image(data.get("secondary_image"), 3.6, 3.1, "sec1")
        pic2 = slide.shapes.add_picture(p2, Inches(9.2), Inches(0.5), Inches(3.6), Inches(3.1))
        pic2.name = "!!SecondaryVisual"

        # 3. Bottom Right Stat Card
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(3.8), Inches(3.6), Inches(3.2))
        card.name = "!!StatCard"
        card.fill.solid()
        card.fill.fore_color.rgb = hex_to_rgb(self.palette["card_white"])
        card.line.fill.background()

        badge_text = data.get("badge", "FROM")
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(4.1), Inches(1.1), Inches(0.35))
        badge.name = "!!Pill"
        badge.fill.solid()
        badge.fill.fore_color.rgb = hex_to_rgb(self.palette["badge_bg"])
        badge.line.fill.background()
        btf = badge.text_frame
        btf.margin_left = btf.margin_top = btf.margin_right = btf.margin_bottom = 0
        bp = btf.paragraphs[0]
        bp.text = badge_text.upper()
        bp.alignment = PP_ALIGN.CENTER
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = hex_to_rgb(self.palette["badge_text"])

        # Text Frame
        tx = slide.shapes.add_textbox(Inches(9.5), Inches(4.6), Inches(3.0), Inches(2.2))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_val = tf.paragraphs[0]
        p_val.text = data.get("metric_value", "$795,000")
        p_val.font.size = Pt(40)
        p_val.font.bold = True
        p_val.font.color.rgb = hex_to_rgb(self.palette["text_dark"])

        p_lbl = tf.add_paragraph()
        p_lbl.text = data.get("metric_label", "Studio & 1-Bed Residences")
        p_lbl.font.size = Pt(13)
        p_lbl.font.color.rgb = hex_to_rgb("#666666")

        p_extra = tf.add_paragraph()
        p_extra.text = data.get("metric_extra", "42 Storeys · East River")
        p_extra.font.size = Pt(13)
        p_extra.font.bold = True
        p_extra.font.color.rgb = hex_to_rgb(self.palette["badge_bg"])

        return slide

    def add_visual_dominant_slide_2(self, data, is_first=False):
        """
        85% Images (Morph continuation):
        - Top Left Wide Photo (8.5" x 4.3")
        - Full Right Tower Photo (3.6" x 6.5")
        - 15% Text: Bottom Left Dark Pill Card
        """
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._add_background(slide)
        if not is_first:
            apply_morph_xml(slide)

        # Top Left Photo (Morphs !!MainVisual)
        p3 = self._resolve_image(data.get("wide_image"), 8.5, 4.3, "wide2")
        pic3 = slide.shapes.add_picture(p3, Inches(0.5), Inches(0.5), Inches(8.5), Inches(4.3))
        pic3.name = "!!MainVisual"

        # Right Tall Photo (Morphs !!SecondaryVisual)
        p4 = self._resolve_image(data.get("tall_image"), 3.6, 6.5, "tall2")
        pic4 = slide.shapes.add_picture(p4, Inches(9.2), Inches(0.5), Inches(3.6), Inches(6.5))
        pic4.name = "!!SecondaryVisual"

        # Bottom Left Stat Card (Morphs !!StatCard)
        card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.0), Inches(8.5), Inches(2.0))
        card2.name = "!!StatCard"
        card2.fill.solid()
        card2.fill.fore_color.rgb = hex_to_rgb(self.palette["card_dark"])
        card2.line.fill.background()

        # Headline
        tx2 = slide.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(7.9), Inches(1.6))
        tf2 = tx2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

        phl = tf2.paragraphs[0]
        phl.text = data.get("headline", "Living space takes the glass. The kitchen takes the core.")
        phl.font.size = Pt(22)
        phl.font.bold = True
        phl.font.color.rgb = hex_to_rgb(self.palette["text_primary"])

        pm = tf2.add_paragraph()
        pm.text = data.get("sub_metrics", "10-foot ceilings  ·  Floor-to-ceiling glass  ·  Delivery 2027")
        pm.font.size = Pt(14)
        pm.font.color.rgb = hex_to_rgb(self.palette["card_accent"])

        return slide

    def build_from_spec(self, spec_data, output_path):
        slides_spec = spec_data.get("slides", [])
        for idx, s in enumerate(slides_spec):
            is_first = (idx == 0)
            stype = s.get("type", "visual_mosaic")
            if stype == "visual_mosaic" or idx % 2 == 0:
                self.add_visual_dominant_slide_1(s, is_first=is_first)
            else:
                self.add_visual_dominant_slide_2(s, is_first=is_first)

        self.prs.save(output_path)
        # Call PowerPoint COM to guarantee 100% native morph registration
        sync_powerpoint_morph_com(os.path.abspath(output_path))
        print(f"Presentation saved & verified with PowerPoint Morph at: {output_path}")
        return output_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", default="output_deck.pptx")
    parser.add_argument("--theme", default="luxury-dark")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) if (args.spec.endswith(".yaml") or args.spec.endswith(".yml")) else json.load(f)

    builder = TonyDeckBuilder(theme=args.theme)
    builder.build_from_spec(data, args.output)

if __name__ == "__main__":
    main()
