# Escalamiento en Lights Out

## 1. Concepto

El **escalamiento** es una transformación geométrica que modifica el tamaño de un objeto sin cambiar su posición base ni su forma esencial.  
En `Lights Out` se aplica en **2D**, porque todos los sprites y animaciones se dibujan sobre el plano `(x, y)` de la pantalla.

En este juego, el escalamiento se usa principalmente para:

- adaptar sprites extraídos de `Don't Starve Together` al tamaño del juego
- mantener proporciones visuales coherentes entre personaje, fogata, garras y objetos
- convertir imágenes originales a tamaños jugables sin redibujarlas manualmente

---

## 2. Base matemática del escalamiento en 2D

Si un punto `(x, y)` se escala con factores `sx` y `sy`, la nueva posición relativa de ese punto es:

```text
x' = x * sx
y' = y * sy
```

Esto significa:

- `sx` controla cuánto crece o reduce el objeto en el eje horizontal
- `sy` controla cuánto crece o reduce el objeto en el eje vertical

En forma matricial:

```text
[x']   [sx  0 ] [x]
[y'] = [0   sy] [y]
```

Si `sx = sy`, el escalamiento es **uniforme** y el objeto conserva sus proporciones.  
Si `sx != sy`, el escalamiento es **no uniforme** y el objeto puede verse estirado o aplastado.

En este proyecto se busca casi siempre un escalamiento uniforme para que los sprites mantengan su estilo original.

---

## 3. Lógica conceptual en el juego

En `Lights Out`, el escalamiento no es una mecánica de juego como moverse o atacar; es una transformación de **presentación visual**.

Su función lógica es:

- hacer que los assets importados se vean bien dentro de una ventana de `900x600`
- evitar que un sprite real de DST aparezca demasiado grande o demasiado pequeño
- conservar una jerarquía visual clara: fogata al centro, WX-78 pequeño, objetos recogibles compactos y enemigos legibles

En otras palabras, el escalamiento conecta:

1. **Matemática**: multiplicar dimensiones por un factor
2. **Lógica visual**: decidir qué tamaño debe tener cada elemento
3. **Código**: redimensionar imágenes antes de dibujarlas

---

## 4. Implementación en el juego

### Caso 1: escalamiento de animaciones SCML

La clase `ScmlAnimation` recibe un parámetro `scale`:

```python
def __init__(self, scml_path, animation_name, scale=1.0, padding=0):
```

Dentro de la carga, el escalamiento se aplica tanto a posición como a tamaño:

```python
pos_x = float(obj.get("x", 0.0)) * scale
pos_y = float(obj.get("y", 0.0)) * scale
scale_x = float(obj.get("scale_x", 1.0)) * scale
scale_y = float(obj.get("scale_y", 1.0)) * scale
```

Y después se calculan las nuevas dimensiones del sprite:

```python
ancho = max(1, int(round(sprite.get_width() * abs(scale_x))))
alto = max(1, int(round(sprite.get_height() * abs(scale_y))))
sprite = pygame.transform.smoothscale(sprite, (ancho, alto))
```

### Qué hace

- Multiplica las dimensiones originales por un factor de escala.
- Genera un sprite nuevo ya redimensionado.
- Mantiene las piezas de la animación en proporción para que el personaje o enemigo no se deformen.

### Interpretación matemática

```text
ancho_nuevo = ancho_original * sx
alto_nuevo  = alto_original * sy
```

Aquí `sx` y `sy` vienen del archivo de animación y además se multiplican por el `scale` general definido en el juego.

---

### Caso 2: escalamiento global de la fogata, garra y WX-78

En la parte superior del código se definen factores de escala:

```python
FOGATA_BASE_SCALE = 0.24
FOGATA_LLAMA_SCALE = 0.22
GARRA_SCALE = 0.22
WX_SCALE = 0.22
```

Después se usan al cargar animaciones:

```python
anim_fogata_base = ScmlAnimation(ruta_base, "idle", scale=FOGATA_BASE_SCALE)
anim_fogata_llama = ScmlAnimation(ruta_llama, "level3", scale=FOGATA_LLAMA_SCALE)
anim_garra = ScmlAnimation(ruta_garra, "idle", scale=GARRA_SCALE)
anim_wx_idle = ScmlAnimation(ruta_wx, "idle_wx_side", scale=WX_SCALE)
anim_wx_run = ScmlAnimation(ruta_wx, "run_loop_side", scale=WX_SCALE)
```

### Qué hace

- La fogata se reduce para que encaje en la zona central.
- Las garras se ajustan al tamaño de amenaza lateral.
- WX-78 se escala para que su proporción respecto a la fogata y al escenario sea correcta.

### Lógica

Estos factores no salen de una fórmula física, sino de una decisión visual del diseño del juego.  
Es decir: el escalamiento aquí tiene una base matemática, pero su valor final se decide por equilibrio estético y jugable.

---

### Caso 3: escalamiento de objetos coleccionables

El juego también ajusta imágenes individuales usando una función dedicada:

```python
def cargar_sprite_ajustado(ruta, tamaño):
    sprite = pygame.image.load(ruta).convert_alpha()
    max_w, max_h = tamaño
    factor = min(max_w / sprite.get_width(), max_h / sprite.get_height())
    ancho = max(1, int(round(sprite.get_width() * factor)))
    alto = max(1, int(round(sprite.get_height() * factor)))
    return pygame.transform.smoothscale(sprite, (ancho, alto))
```

### Qué hace

- Recibe un tamaño máximo permitido.
- Calcula un factor de escala que conserve la proporción original.
- Ajusta el sprite para que quepa dentro de ese espacio.

Los tamaños máximos definidos son:

```python
SPRITE_SIZES = {
    "leña": (50, 26),
    "carbon": (35, 35),
    "engrane": (28, 28),
}
```

### Interpretación matemática

```text
factor = min(max_w / ancho_original, max_h / alto_original)
```

Luego:

```text
ancho_nuevo = ancho_original * factor
alto_nuevo  = alto_original * factor
```

Este método es muy útil porque escala la imagen sin romper su proporción.

---

## 5. Por qué se usa `smoothscale`

El juego utiliza:

```python
pygame.transform.smoothscale(sprite, (ancho, alto))
```

en lugar de un escalado más brusco, porque:

- mejora la calidad visual del sprite redimensionado
- evita bordes demasiado duros o deformaciones fuertes
- hace que los assets integrados se vean más limpios en pantalla

En términos prácticos, `smoothscale` no cambia la matemática del escalamiento; solo mejora cómo se ve el resultado.

---

## 6. Relación entre escalamiento y proporción

En un juego 2D no basta con “hacer más grande” o “hacer más chico” un sprite.  
También hay que cuidar la **proporción**.

Por eso el código usa:

```python
factor = min(max_w / sprite.get_width(), max_h / sprite.get_height())
```

Con esto:

- el sprite nunca rebasa el espacio máximo
- el ancho y el alto cambian con el mismo factor
- se conserva el estilo original del asset

Eso evita errores visuales como:

- fogatas gigantes
- objetos demasiado pequeños para recogerlos
- sprites estirados horizontal o verticalmente

---

## 7. Diferencia entre escalamiento matemático y escalamiento en el juego

### Matemáticamente

El escalamiento consiste en multiplicar coordenadas o dimensiones por un factor:

```text
x' = x * sx
y' = y * sy
```

### En el juego

Se traduce a acciones como:

```python
sprite.get_width() * factor
sprite.get_height() * factor
pygame.transform.smoothscale(sprite, (ancho, alto))
```

La idea es la misma: cambiar el tamaño de un elemento manteniendo control sobre sus proporciones.

---

## 8. Conclusión

El escalamiento en `Lights Out` es una transformación 2D usada para adaptar sprites y animaciones al tamaño visual correcto del juego.  
Matemáticamente se basa en multiplicar dimensiones por factores de escala.  
Lógicamente, se usa para mantener consistencia visual y jugabilidad.  
En código, se implementa con factores como `FOGATA_BASE_SCALE`, `WX_SCALE` y con funciones como `pygame.transform.smoothscale(...)`.

Se aplica sobre todo en:

- la fogata
- la llama
- las garras
- WX-78
- la leña, el carbón y el engrane

Por eso, aunque el escalamiento no mueve objetos ni causa colisiones directamente, sí es clave para que todos los elementos del juego se vean proporcionados y funcionales.

---

## 9. Referencia al código del proyecto

Las partes principales donde se usa escalamiento en `LightsOut.py` son:

- `ScmlAnimation._cargar_desde_scml()`
- `cargar_sprite_ajustado()`
- `cargar_animaciones()`
- `SPRITE_SIZES`
- las constantes de escala visual

Ejemplos directos:

```python
scale_x = float(obj.get("scale_x", 1.0)) * scale
scale_y = float(obj.get("scale_y", 1.0)) * scale
```

```python
sprite = pygame.transform.smoothscale(sprite, (ancho, alto))
```

```python
FOGATA_BASE_SCALE = 0.24
WX_SCALE = 0.22
```

---

## 10. Idea clave para exposición

Si te preguntan “¿cómo se usa el escalamiento en tu juego?”, una respuesta corta sería:

> El escalamiento en mi juego se implementa en 2D para ajustar el tamaño de sprites y animaciones. Matemáticamente se basa en multiplicar las dimensiones originales por un factor de escala. En mi código lo uso para adaptar la fogata, WX-78, las garras y los objetos recolectables al tamaño visual adecuado sin deformar sus proporciones.
