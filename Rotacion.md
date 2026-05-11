# Rotación en Lights Out

## 1. Concepto

La **rotación** es una transformación geométrica que cambia la orientación de un objeto alrededor de un punto de referencia. En este juego aplica en **2D**, porque todos los elementos se dibujan sobre el plano de la pantalla usando coordenadas `(x, y)`.

En `LightsOut.py` la rotación se usa de dos formas:

1. **Rotación continua**
   Se usa en el `engrane` para simular que está girando.
2. **Rotación fija de orientación**
   Se usa en las `garras` para reutilizar el mismo sprite y apuntarlo hacia la izquierda o hacia la derecha.

---

## 2. Base matemática de la rotación en 2D

Si un punto `(x, y)` gira un ángulo `theta` alrededor del origen `(0, 0)`, sus nuevas coordenadas son:

```text
x' = x cos(theta) - y sin(theta)
y' = x sin(theta) + y cos(theta)
```

Esto puede expresarse con la matriz de rotación:

```text
[x']   [ cos(theta)  -sin(theta) ] [x]
[y'] = [ sin(theta)   cos(theta) ] [y]
```

Si el giro no ocurre alrededor del origen sino alrededor de un centro `(cx, cy)`, primero se traslada el punto al origen, luego se rota y al final se regresa a su posición:

```text
x1 = x - cx
y1 = y - cy

x2 = x1 cos(theta) - y1 sin(theta)
y2 = x1 sin(theta) + y1 cos(theta)

x' = x2 + cx
y' = y2 + cy
```

En el juego no hacemos esta operación manual para cada píxel, porque `pygame` ya ofrece funciones como `pygame.transform.rotate(...)`, pero matemáticamente eso es lo que está ocurriendo.

---

## 3. Lógica conceptual en el juego

En `Lights Out` la rotación no se usa para mover al personaje en círculo, sino para mejorar la lectura visual de los objetos:

- El `engrane` gira para comunicar que es un objeto mecánico y energético.
- La `garra` rota para que el mismo recurso visual sirva desde ambos lados de la pantalla.

Eso significa que la rotación en este juego es principalmente una transformación de **renderizado**, no una mecánica de movimiento del mundo.

---

## 4. Implementación real en el juego

### Caso 1: rotación continua del engrane

Código usado en `Objeto.dibujar`:

```python
rotado = pygame.transform.rotate(sprite, self.t * 90)
rect = rotado.get_rect(center=(cx, cy))
surf.blit(rotado, rect)
```

### Qué hace

- `self.t` es el tiempo acumulado del objeto.
- `self.t * 90` significa que el engrane gira a una velocidad angular de **90 grados por segundo**.
- `pygame.transform.rotate` genera una nueva superficie ya rotada.
- `get_rect(center=(cx, cy))` vuelve a centrar la imagen, porque al rotarla cambia su caja contenedora.

### Relación matemática

Aquí se está usando la idea:

```text
angulo = velocidadAngular * tiempo
theta = 90 * t
```

Es decir, el ángulo depende del tiempo transcurrido. Mientras más tiempo pasa, más gira el objeto.

---

### Caso 2: rotación fija de las garras

Código usado en `Garra.dibujar`:

```python
angulo = -90 if self.desde_izq else 90
frame = pygame.transform.rotate(frame, angulo)
frame_rect = frame.get_rect(center=(cx, cy))
surf.blit(frame, frame_rect)
```

### Qué hace

- Si la garra entra desde la izquierda, rota `-90` grados.
- Si entra desde la derecha, rota `90` grados.
- Después se recentra con `get_rect(center=(cx, cy))`.

### Lógica

Aquí la rotación no depende del tiempo, sino del **estado del enemigo**. La variable `self.desde_izq` decide hacia qué lado debe orientarse el sprite.

En otras palabras:

- **rotación dinámica**: depende del tiempo
- **rotación condicional**: depende del lado o del estado del objeto

---

## 5. Por qué hay que recentrar el sprite

Cuando una imagen rota en 2D, su rectángulo envolvente cambia de tamaño. Por eso, si se dibuja sin corregir su posición, puede parecer que “salta” o se mueve aunque solo esté girando.

La solución usada en el juego es:

```python
rect = rotado.get_rect(center=(cx, cy))
```

Eso conserva el mismo centro visual del objeto después de la rotación.

Este detalle es importante porque evita errores visuales y mantiene estable la posición del engrane y de las garras.

---

## 6. Diferencia entre rotación matemática y rotación en Pygame

### Rotación matemática pura

- Se calcula punto por punto con seno y coseno.
- Da control total sobre la transformación.
- Es útil para motores gráficos, física o álgebra lineal.

### Rotación usada en este juego

- Se delega a `pygame.transform.rotate`.
- Es más práctica para un proyecto 2D.
- La base matemática sigue siendo la misma, pero la librería ya realiza el proceso internamente.

---

## 7. Conclusión

La rotación en `Lights Out` es una transformación 2D usada para dar claridad visual, reutilizar sprites y reforzar la sensación de movimiento. Matemáticamente se basa en seno, coseno y matrices de rotación; en código se implementa con `pygame.transform.rotate(...)` y una corrección de centrado con `get_rect(center=...)`.

En este proyecto se aplica principalmente en:

- el **engrane**, con rotación continua en función del tiempo
- las **garras**, con rotación fija según el lado de aparición

Por lo tanto, la rotación sí forma parte del juego tanto a nivel matemático como lógico y visual, aunque no sea una mecánica principal de movimiento del personaje.

---

## 8. Referencia directa al código del proyecto

Las partes donde se aplica rotación en `LightsOut.py` son:

- `Objeto.dibujar()` para el `engrane`
- `Garra.dibujar()` para orientar las garras

Ejemplos:

```python
rotado = pygame.transform.rotate(sprite, self.t * 90)
```

```python
angulo = -90 if self.desde_izq else 90
frame = pygame.transform.rotate(frame, angulo)
```

---

## 9. Idea clave para exposición

Si tu profesor te pregunta “¿cómo se usa la rotación en tu juego?”, la respuesta corta sería:

> La rotación en mi juego se implementa en 2D. Matemáticamente se basa en las funciones seno y coseno, que permiten girar puntos alrededor de un centro. En la práctica, en `pygame` uso `transform.rotate` para rotar sprites. Lo aplico en el engrane para que gire con el tiempo y en las garras para orientarlas según el lado de donde aparecen.
