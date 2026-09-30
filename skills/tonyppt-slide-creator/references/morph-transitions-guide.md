# Guía de Transiciones Morph (Transformación) en PowerPoint

El efecto más llamativo del estilo TonyPPT es la fluidez cinematográfica entre diapositivas. En PowerPoint, esto se logra mediante la transición nativa **Morph (Transformación)** combinada con nombres de formas sincronizados.

---

## 1. Cómo Funciona Morph en PowerPoint OpenXML

PowerPoint 2019, 2021 y Microsoft 365 implementan la transición Morph en el esquema XML de cada diapositiva (`ppt/slides/slideN.xml`):

```xml
<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" 
              xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/roamingSettings" 
              spd="med" advClick="1">
    <p15:prstTrans prst="morph"/>
</p:transition>
```

Cuando PowerPoint encuentra esta instrucción, no desvanece ni corta la pantalla: **anima la posición, escala, recorte y color de los objetos** de la diapositiva anterior a la nueva.

---

## 2. El Secreto del Emparejamiento: Prefijo `!!`

Para forzar a PowerPoint a animar un objeto específico entre dos diapositivas (incluso si cambia de tamaño o forma), PowerPoint utiliza la convención de doble signo de exclamación:

```python
# Diapositiva 1
hero_photo.name = "!!HeroPhoto"       # Ocupa 60% izquierda (7.5" x 6.5")
metric_card.name = "!!MetricCard1"    # Tarjeta blanca arriba a la derecha

# Diapositiva 2
tower_photo.name = "!!HeroPhoto"      # Ocupa slot pequeño abajo a la derecha (2.3" x 3.1")
headline_card.name = "!!MetricCard1"  # Se expande a tarjeta panorámica abajo (6.5" x 3.1")
```

**Resultado visual al presentar:**
* La foto heroica gigante se encoge y vuela suavemente hacia la esquina inferior derecha.
* La tarjeta blanca de métrica se expande suavemente y se convierte en el titular editorial.
* Da la sensación de una interfaz interactiva de aplicación moderna, no de diapositivas estáticas.

---

## 3. Reglas de Continuidad
1. Mantén la misma paleta de fondo entre diapositivas consecutivas para evitar parpadeos.
2. Cada diapositiva a partir de la Diapositiva 2 debe tener inyectado el nodo `p:transition` con `prst="morph"`.
3. Empareja al menos 1 fotografía y 1 contenedor de tarjeta entre diapositivas adyacentes para garantizar la continuidad del movimiento.
