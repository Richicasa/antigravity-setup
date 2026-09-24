# Especificación Técnica de Campos Dinámicos OpenXML para Zotero

## 1. Campo de Cita en el Texto (In-Text Citation)

En Microsoft Word, una cita viva de Zotero se almacena dentro de un elemento `<w:fldSimple>` con el atributo `w:instr` que contiene la instrucción `ADDIN ZOTERO_ITEM` seguida del CSL-JSON escapado en HTML.

### Estructura XML:

```xml
<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr=" ADDIN ZOTERO_ITEM {&quot;citationID&quot;:&quot;a8f1x9b2&quot;,&quot;properties&quot;:{&quot;formattedCitation&quot;:&quot;[1]&quot;,&quot;plainCitation&quot;:&quot;[1]&quot;,&quot;dontUpdate&quot;:false,&quot;noteIndex&quot;:0},&quot;citationItems&quot;:[{&quot;id&quot;:306,&quot;uris&quot;:[&quot;http://zotero.org/users/local/0/items/5F4EVA82&quot;],&quot;itemData&quot;:{&quot;id&quot;:306,&quot;type&quot;:&quot;article-journal&quot;,&quot;title&quot;:&quot;Título del estudio&quot;,&quot;container-title&quot;:&quot;Revista NLM&quot;,&quot;volume&quot;:&quot;45&quot;,&quot;issue&quot;:&quot;1&quot;,&quot;page&quot;:&quot;12-20&quot;,&quot;DOI&quot;:&quot;10.1111/j.1234&quot;,&quot;issued&quot;:{&quot;date-parts&quot;:[[2024]]}}}],&quot;schema&quot;:&quot;https://github.com/citation-style-language/schema/raw/master/csl-citation.json&quot;} ">
    <w:r>
        <w:rPr>
            <w:rStyle w:val="ZoteroIn-TextCitation"/>
            <w:color w:val="1B4F72"/>
            <w:b/>
        </w:rPr>
        <w:t>[1]</w:t>
    </w:r>
</w:fldSimple>
```

### Reglas Críticas:
1. El contenido del atributo `w:instr` debe empezar con ` ADDIN ZOTERO_ITEM ` (con espacio al inicio y al final).
2. Las comillas dobles `"` dentro del JSON deben estar escapadas como `&quot;` o mediante `html.escape()`.
3. El ID del ítem (`id`) y el URI (`http://zotero.org/users/local/0/items/<key>`) deben corresponder a un registro real en Zotero para permitir la sincronización automática bidireccional. Si se genera un documento antes de que Zotero tenga el ítem, se incluye el objeto `itemData` completo como fallback embebido.

---

## 2. Campo de Bibliografía Dinámica

La bibliografía viva se encapsula con `ADDIN ZOTERO_BIBL`:

```xml
<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr=" ADDIN ZOTERO_BIBL {&quot;uncited&quot;:[],&quot;omitted&quot;:[],&quot;custom&quot;:[]} CSL_BIBLIOGRAPHY ">
    <w:r>
        <w:rPr>
            <w:rStyle w:val="ZoteroBibliography"/>
        </w:rPr>
        <w:t>1. Caton JG, Armitage G, Berglundh T, et al. A new classification scheme... J Clin Periodontol. 2018;45 Suppl 20:S1-S8.</w:t>
    </w:r>
</w:fldSimple>
```

Cuando el usuario hace clic en **Zotero -> Document Preferences** o **Refresh** en Word, el motor de Zotero procesa este campo y actualiza toda la lista de forma instantánea.
