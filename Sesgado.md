# Sesgado en Lights Out

## 1. Concepto

El **sesgado** o **shearing** es una transformación geométrica que inclina o deforma un objeto desplazando sus puntos en un eje de acuerdo con su posición en el otro eje.

En otras palabras, el objeto no solo se mueve, rota o cambia de tamaño: se **deforma inclinándose**.

En `Lights Out` aplica en **2D**, porque el juego se dibuja en una pantalla con coordenadas `(x, y)`. No se usa sesgado 3D porque no hay profundidad, cámara 3D ni modelos tridimensionales.

---

## 2. Base matemática del sesgado en 2D

El sesgado puede aplicarse en el eje `x` o en el eje `y`.

### Sesgado horizontal

El eje `x` cambia dependiendo del valor de `y`:

```text
x' = x + shx * y
y' = y
```

Matriz:

```text
[x']   [1  shx] [x]
[y'] = [0   1 ] [y]
```

### Sesgado vertical

El eje `y` cambia dependiendo del valor de `x`:

```text
x' = x
y' = y + shy * x
```

Matriz:

```text
[x']   [1   0 ] [x]
[y'] = [shy 1 ] [y]
```

Donde:

- `shx` es el factor de sesgado horizontal
- `shy` es el factor de sesgado vertical
- si el factor es positivo, la inclinación va hacia un lado
- si el factor es negativo, la inclinación va hacia el lado contrario

---

## 3. Lógica conceptual en el juego

En `Lights Out`, el sesgado se usa de forma **visual y manual**, no como una transformación directa sobre sprites completos.

El caso más claro es la **lluvia**:

- una gota podría dibujarse como una línea vertical
- pero el juego desplaza el punto final hacia la izquierda
- eso hace que la gota se vea inclinada, como si el viento la estuviera empujando

Esa inclinación visual funciona como un sesgado porque el extremo inferior de la línea cambia su coordenada `x` con respecto al extremo superior.

---

## 4. Implementación real en el juego

### Caso principal: lluvia sesgada por viento

Código usado en `dibujar_lluvia`:

```python
pygame.draw.line(
    capa,
    (150, 190, 255, 120),
    (int(x), int(y)),
    (int(x - 6), int(y + largo)),
    2
)
```

### Qué hace

La gota se dibuja desde:

```text
(x, y)
```

hasta:

```text
(x - 6, y + largo)
```

Si la gota fuera totalmente vertical, terminaría en:

```text
(x, y + largo)
```

Pero como el código usa `x - 6`, el extremo inferior se desplaza horizontalmente. Eso produce una línea inclinada.

---

## 5. Relación matemática con el sesgado

Para una gota vertical, podemos pensar en dos puntos:

```text
punto superior = (x, y)
punto inferior = (x, y + largo)
```

Después del sesgado visual:

```text
punto superior = (x, y)
punto inferior = (x - 6, y + largo)
```

Esto se puede interpretar como un sesgado horizontal relativo:

```text
x' = x + shx * distancia_y
```

En este caso:

```text
distancia_y = largo
desplazamiento_x = -6
shx = -6 / largo
```

Entonces, si una gota tiene `largo = 20`:

```text
shx = -6 / 20
shx = -0.3
```

Eso significa que la gota se inclina hacia la izquierda. Mientras más grande sea el desplazamiento horizontal, más fuerte se ve el sesgado.

---

## 6. Sesgado y movimiento de lluvia

La lluvia también se mueve de forma diagonal en `actualizar_lluvia`:

```python
gota[0] -= 160 * dt
gota[1] += gota[3] * dt
```

Esto no es sesgado por sí solo; eso es **traslación diagonal**.

La diferencia es:

- `actualizar_lluvia` mueve toda la gota
- `dibujar_lluvia` inclina visualmente la gota

Por eso, la lluvia combina dos transformaciones:

- **traslación**: cambia la posición general de la gota
- **sesgado visual**: inclina la forma de la gota

---

## 7. Por qué no se usa una función directa de sesgado

`pygame` incluye transformaciones comunes como:

- `rotate`
- `scale`
- `smoothscale`
- `flip`

Pero no tiene una función simple integrada como:

```python
pygame.transform.shear(...)
```

Por eso, en este juego el sesgado se implementa manualmente modificando coordenadas.  
En el caso de la lluvia, en lugar de transformar una imagen completa, se dibuja una línea ya inclinada desde el inicio.

---

## 8. Posible implementación general de sesgado

Si se quisiera aplicar sesgado a puntos de una figura manualmente, se podría usar una función como esta:

```python
def sesgar_punto(x, y, shx=0.0, shy=0.0):
    nuevo_x = x + shx * y
    nuevo_y = y + shy * x
    return nuevo_x, nuevo_y
```

Para sesgar un polígono completo:

```python
puntos_sesgados = [
    sesgar_punto(x, y, shx=-0.3)
    for x, y in puntos_originales
]
```

Esta sería la versión matemática directa del sesgado.  
En el juego actual no se necesita para todos los sprites porque la lluvia se resuelve de forma más simple y eficiente.

---

## 9. Diferencia entre sesgado, rotación y traslación

El sesgado puede parecer una rotación porque inclina el objeto, pero no son lo mismo.

### Traslación

Mueve el objeto completo:

```text
x' = x + tx
y' = y + ty
```

### Rotación

Gira el objeto alrededor de un punto:

```text
x' = x cos(theta) - y sin(theta)
y' = x sin(theta) + y cos(theta)
```

### Sesgado

Inclina el objeto deformando sus coordenadas:

```text
x' = x + shx * y
y' = y
```

En la lluvia de `Lights Out`, la gota no solo se mueve: también se dibuja inclinada, por eso se puede justificar como un sesgado visual.

---

## 10. Conclusión

El sesgado en `Lights Out` se aplica de manera 2D y visual, principalmente en la lluvia.  
Matemáticamente, el sesgado consiste en modificar una coordenada dependiendo de la otra, por ejemplo:

```text
x' = x + shx * y
```

En el código del juego se representa inclinando cada gota:

```python
(int(x), int(y)) -> (int(x - 6), int(y + largo))
```

Esto hace que la lluvia no caiga como líneas rectas verticales, sino con una inclinación que sugiere viento y movimiento.  
Aunque no se usa una función directa de sesgado sobre sprites, la lógica matemática sí aparece en la forma en que se calculan los puntos de dibujo.

---

## 11. Referencia al código del proyecto

Las partes principales relacionadas con sesgado en `LightsOut.py` son:

- `dibujar_lluvia()`
- `actualizar_lluvia()`

Ejemplo directo:

```python
pygame.draw.line(capa, color, (int(x), int(y)), (int(x - 6), int(y + largo)), 2)
```

Este fragmento desplaza el punto inferior de la gota hacia la izquierda, generando una inclinación visual equivalente a un sesgado horizontal.

---

## 12. Idea clave para exposición

Si te preguntan “¿cómo se usa el sesgado en tu juego?”, una respuesta corta sería:

> En mi juego el sesgado se aplica de forma visual en la lluvia. Matemáticamente, el sesgado modifica una coordenada dependiendo de la otra, como `x' = x + shx * y`. En el código dibujo cada gota como una línea inclinada, desplazando su punto inferior hacia la izquierda. Así la lluvia parece afectada por el viento sin necesitar una función especial de sesgado.
