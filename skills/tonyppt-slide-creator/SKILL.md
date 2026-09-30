---
name: tonyppt-slide-creator
description: >-
  Crea presentaciones de diapositivas hiper-estéticas en PowerPoint (.pptx) con estilo Bento Grid y TonyPPT. Aplica una proporción estricta de 85% imágenes de alta resolución y 15% texto/microcopia de alto impacto, eliminando el estilo aburrido tipo Gamma. Incorpora transiciones cinematográficas Morph (Transformación) en PowerPoint, curación automática de fotografías HD y generación nativa con python-pptx. Úsalo cuando el usuario pida crear presentaciones, diapositivas estilo TonyPPT, decks con bento grids, o transformar textos/PDFs en PowerPoint de calidad de agencia.
---

# TonyPPT Slide Creator (Bento Grid & Morph Engine)

Transforma cualquier texto extenso, documento o PDF en una presentación de diapositivas nativa de PowerPoint (`.pptx`) con la estética visual de **TonyPPT**: **85% fotografía cinematográfica de alta calidad** y **15% texto/microcopia de alto impacto** organizada en cuadrículas Bento Grid con transiciones fluidas **Morph**.

---

## 1. Principios Clave de Diseño

1. **Anti-Gamma / Cero AI-Slop:** Quedan estrictamente prohibidas las listas de viñetas, párrafos largos y diapositivas blancas con cajas grises centradas.
2. **Proporción 85/15:** La fotografía y la composición espacial dominan la diapositiva. El texto se reduce a números gigantes, badges tipo pastilla y microcopia concisa (máximo 12 palabras por tarjeta).
3. **Transición Morph Nativa:** Cada cambio de diapositiva utiliza la transición `morph` de PowerPoint con nombres sincronizados (`!!HeroPhoto`, `!!MetricCard1`) para animar tarjetas y fotos con fluidez cinematográfica.

Consulta los manuales detallados de soporte:
- [Catálogo de Arquetipos Bento Grid](references/bento-grid-archetypes.md)
- [Guía de Transiciones Morph y Sincronización](references/morph-transitions-guide.md)
- [Reglas de Calidad Anti-Slop](references/anti-slop-guidelines.md)

---

## 2. Flujo de Trabajo para el Agente

Cuando el usuario te entregue un tema, contexto, artículo o PDF para armar diapositivas, sigue este procedimiento paso a paso:

### Paso 1: Destilación y Storyboard (15% texto)
1. Lee el material del usuario y divídelo en diapositivas clave (típicamente entre 3 y 8 diapositivas).
2. Para cada diapositiva, extrae:
   - **La Idea Heroica:** 1 concepto único.
   - **Métrica Principal:** 1 cifra destacada de gran formato (ej. `$795,000`, `94%`, `42 Storeys`, `10x`).
   - **Badges:** Etiquetas breves de 1 palabra (`FROM`, `NEW`, `LEED GOLD`, `TARGET`).
   - **Descriptor Breve:** Máximo 1 línea de contexto.
3. Asigna a cada diapositiva un arquetipo Bento:
   - `hero-stat-mosaic`: Mosaico con foto al 60% y 3 tarjetas a la derecha.
   - `triad-comparison`: 3 columnas superiores y titular editorial abajo.
   - `quad-bento`: 4 chips de métrica arriba y panel fotográfico dividido abajo.

### Paso 2: Curación de Imágenes High-Res (85% imagen)
1. Para cada slot visual, define un término de búsqueda fotográfico concreto (ej. `"luxury dusk architecture balcony"`, `"modern high-rise glass facade"`, `"minimalist executive workspace"`).
2. Usa el script de búsqueda o URLs directas en alta resolución (1080p o 4K) evitando fotos de stock genéricas.

### Paso 3: Generación del Archivo de Especificación (`deck_spec.yaml`)
Crea un archivo YAML con la configuración de las diapositivas basándote en la plantilla:
`templates/deck_spec_template.yaml`.

### Paso 4: Ejecución del Motor PPTX
Invoca el generador con PowerShell o Python:

```bash
python ~/.gemini/config/skills/tonyppt-slide-creator/scripts/build_deck.py --spec deck_spec.yaml --output mi_presentacion.pptx --theme luxury-dark
```

### Paso 5: Generación de Vista Previa (Opcional)
Para exportar las diapositivas a imágenes PNG y mostrarlas al usuario antes o después de la entrega:

```powershell
powershell -ExecutionPolicy Bypass -File ~/.gemini/config/skills/tonyppt-slide-creator/scripts/render_preview.ps1 -PptxPath mi_presentacion.pptx
```

---

## 3. Comandos y Herramientas del Entorno

| Script | Propósito |
| :--- | :--- |
| `scripts/build_deck.py` | Motor de renderizado `python-pptx` con layouts Bento Grid y Morph XML. |
| `scripts/fetch_images.py` | Descarga y recorte milimétrico con Pillow para evitar distorsiones. |
| `scripts/render_preview.ps1` | Exporta las diapositivas del PPTX a imágenes PNG de 1920x1080 usando la API de PowerPoint. |
