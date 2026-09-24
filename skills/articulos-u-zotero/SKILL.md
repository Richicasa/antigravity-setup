---
name: articulos-u-zotero
description: >-
  Pipeline integral de redacción, curaduría de literatura médica, des-plagio y compilación de artículos científicos, revisiones sistemáticas y capítulos de libros. Especializado en odontología, pediatría y biomedicina con integración total a Zotero Desktop (puerto 23119, SQLite local zotero.sqlite), inyección de campos dinámicos nativos en Word (w:fldSimple / ADDIN ZOTERO_ITEM y ZOTERO_BIBL en Vancouver), generación de figuras a 300 DPI (diagramas PRISMA 2020, algoritmos terapéuticos, gráficos epidemiológicos) y control editorial anti-plagio (máximo 3 palabras consecutivas de fuentes originales).
---

# Artículos Científicos, Revisiones Sistemáticas e Integración Zotero (ARTICULOS U)

Esta habilidad proporciona el flujo de trabajo completo, riguroso y automatizado desarrollado en el ecosistema **ARTICULOS U** para investigar, redactar, ilustrar, citar y compilar manuscritos biomédicos con estándar de publicación internacional (Scopus Q1/Q2, PubMed, SciELO).

---

## 1. Arquitectura de Integración con Zotero

A diferencia de los procesadores que generan simple texto plano con números entre corchetes, esta habilidad implementa la **tríada de integración nativa con Zotero**:

### A. Inyección Directa vía Zotero Connector API
* **Endpoint local:** `http://127.0.0.1:23119/connector/saveItems`
* **Comportamiento:** Si Zotero Desktop está abierto, el agente inyecta los metadatos completos de los artículos (título, autores, revista, año, volumen, páginas, DOI, resumen, etiquetas) directamente a la colección activa de Zotero sin que el usuario deba importar manualmente archivos `.ris` o `.bib`.
* **Script de soporte:** `scripts/zotero_api.py` (`ensure_zotero_running()`, `inject_items_to_zotero()`).

### B. Inspección Local de la Base de Datos SQLite
* **Ubicación:** `%USERPROFILE%\Zotero\zotero.sqlite` (o `~/Zotero/zotero.sqlite`)
* **Modo de conexión:** `file:<ruta_zotero>/zotero.sqlite?mode=ro&nolock=1` (seguro contra bloqueos de concurrencia).
* **Función:** Recupera las claves maestras (`key`, `itemID`) asignadas por Zotero a cada estudio para enlazarlas de forma unívoca con el documento de Microsoft Word.

### C. Campos Dinámicos Vivos en Microsoft Word (`w:fldSimple`)
* **Mecanismo:** Word y Zotero se comunican mediante campos OpenXML (`w:fldSimple`) con la instrucción `ADDIN ZOTERO_ITEM` y `ADDIN ZOTERO_BIBL` que encapsula la especificación CSL-JSON (*Citation Style Language*).
* **Resultado:** Al abrir el archivo `.docx` resultante en Microsoft Word con el plugin oficial de Zotero instalado:
  1. Las citas numéricas (`[1]`, `[2,3]`, `[1-5]`) son **campos dinámicos grises / interactivos**.
  2. El botón **Refresh** o **Document Preferences** de Zotero en Word actualiza, reordena y cambia estilos (de Vancouver a APA o viceversa) con un solo clic.
  3. La sección de **Referencias** se genera bajo el control del gestor bibliográfico.
* **Script de soporte:** `scripts/zotero_word_engine.py`.

---

## 2. Protocolo de Curaduría y Calidad de Evidencia

1. **Jerarquía de Fuentes:**
   - Revisiones sistemáticas y metanálisis (Cochrane, PRISMA).
   - Ensayos clínicos aleatorizados (CONSORT).
   - Estudios observacionales de cohortes y casos-controles (STROBE).
   - Consensos internacionales de sociedades científicas (AAP, EFP, IAPD, ALOP).
2. **Bases de Datos Obligatorias:** PubMed / MEDLINE, Scopus, SciELO, LILACS, Latindex, Web of Science.
3. **Regla de Cero Reducción:** Nunca eliminar citas en revisiones de capítulos o artículos para resolver inconsistencias. Siempre reemplazar quirúrgicamente fuentes dudosas o comerciales por literatura indexada de alto factor de impacto con correspondencia temática exacta.

---

## 3. Humanización, Estilo y Anti-Plagio

* **Regla de Plagio:** No permitir más de 3 palabras consecutivas idénticas a la fuente original. Aplicar paráfrasis médica profunda, síntesis conceptual y reconstrucción sintáctica.
* **Erradicación del 'Cantinfleo':** Prohibir muletillas vacías, redundancias (*«en el ámbito de»*, *«a nivel de la cavidad bucal»* $\rightarrow$ *«en la cavidad bucal»* o *«manifestaciones orales»*) y fórmulas acartonadas de IA (*«En conclusión, es importante destacar que...»*).
* **Fórmula de Citación Integrada:** Sustituir giros arcaicos como `según Gómez (cols)(1)` por narrativa biomédica fluida con corchetes enlazados: *«Gómez y colaboradores demostraron que la terapia periodontal disminuye la carga patógena en pacientes pediátricos [1].»*

---

## 4. Protocolo Obligatorio de Corrección Ortotipográfica, Lingüística y de Estilo

Este paso es **estrictamente obligatorio y permanente** en toda revisión o redacción de libros y artículos científicos:

1. **Corrección Ortotipográfica y Diacrítica Integral:**
   * Detección y corrección de palabras mal escritas, erratas de tecleo y términos truncados heredados del borrador original (ej. *involicran* $\rightarrow$ *involucran*, *elelmentos* $\rightarrow$ *elementos*, *pacie.* $\rightarrow$ *pacientes.*).
   * Restitución rigurosa de tildes omitidas en palabras llanas terminadas en consonante distinta de n/s (*fértil*), esdrújulas médicas (*endodónticas*), hiatos acentuales (*ametropías*, *cardiopatía*) y agudas (*también*).
2. **Concordancia Gramatical y Sintáctica Biomédica:**
   * Armonización estricta de género y número entre artículos, sustantivos y adjetivos (ej. *las leucemias mieloblásticas agudas*, *las maloclusiones* en una sola palabra).
   * Corrección de concordancia de número en construcciones pasivas o impersonales (ej. *se conocen varios factores*, no *se conoce varios factores*).
   * Supresión de comas criminales entre sujeto y verbo (ej. *Down denominó*, no *Down, denominó*).
3. **Limpieza Mecánica y Espaciado:**
   * Eliminación sistemática de espacios antes de puntos o comas (` .` $\rightarrow$ `.`, ` ,` $\rightarrow$ `,`).
   * Eliminación de espacios dobles o triples repetidos a lo largo de los párrafos.
   * Fusión ortográfica correcta de prefijos según la RAE (ej. *hiperinervación*, *megacolon*, *malposición*, *miorrelajante* con doble r).
4. **Norma Tipográfica Vancouver en Biomedicina:**
   * **Nomenclatura Binomial en Cursiva:** Bacterias, virus y hongos siempre en cursiva (*Aggregatibacter actinomycetemcomitans*, *Tannerella forsythia*, *Prevotella intermedia*, *Bacteroides melaninogenicus*, *Streptococcus mutans*).
   * **Locuciones Latinas:** Cursiva obligatoria (*cor pulmonale*, *in vitro*, *in vivo*, *et al.*).
   * **Cero Cursivas en Datos Numéricos:** Estadísticas, prevalencias, tasas y porcentajes siempre en redonda/normal (nunca en cursiva).

---

## 5. Generación Gráfica Científica a 300 DPI

Todo artículo o capítulo debe contar con soporte visual propio de alta resolución compilado en la carpeta del proyecto:

1. **Figura 1: Diagrama de Flujo PRISMA 2020**
   - Etapas: Identificación, Tamizaje (Cribado), Elegibilidad e Inclusión con conteos exactos ($n$) y motivos formales de exclusión.
2. **Figura 2: Gráficos Epidemiológicos o Distribución Fenotípica**
   - Gráficos de barras comparativas o mapas de calor de prevalencia, patógenos periodontales o distribución anatómica.
3. **Figura 3: Algoritmo Terapéutico o Evaluación de Riesgo de Sesgo**
   - Árbol de decisiones clínicas (conservación vs exodoncia, cierre ortodóncico vs implante) o semáforo RoB-2 / ROBINS-I.
* **Script de soporte:** `scripts/scientific_figures.py`.

---

## 6. Estándar de Almacenamiento y Entregables

Cada nuevo proyecto o artículo se organiza de forma estricta en el Escritorio del usuario:
📁 `%USERPROFILE%\Desktop\todo\articulos\<Nombre_Articulo>\`
o en su caso:
📁 `%USERPROFILE%\Desktop\todo\libro\<Nombre_Capitulo>\`

### Paquete Canónico de Entregables (Regla Estricta de 3 Archivos):
En la carpeta final de cada capítulo o artículo SOLO deben existir 3 archivos limpios y definitivos:
1. `<Capitulo>_original.docx`: Copia de seguridad inmutable del original.
2. `<Capitulo>_revisado.docx`: Manuscrito final definitivo con tablas formateadas, encabezados de página corregidos (`Odontopediatría`), fórmulas citogenéticas normalizadas, ortotipografía impecable, figuras intactas al 100% y **campos dinámicos Zotero Live**.
3. `<capitulo>_referencias.bib`: Base de datos exportada para Zotero con las referencias curadas.

* **Regla de Limpieza:** Todos los archivos temporales (`_nuevo`, `_corrected`, `_pre_ortografia`, etc.) y reportes intermedios (`.md`, `.docx` de informe) DEBEN eliminarse automáticamente de la carpeta de trabajo antes de notificar al usuario.
