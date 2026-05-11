# Traslación en Lights Out

## 1. Concepto

La **traslación** es una transformación geométrica que mueve un objeto de una posición a otra sin cambiar su forma, tamaño ni orientación.  
En `Lights Out` se aplica en **2D**, porque todo el juego ocurre en el plano de la pantalla usando coordenadas `(x, y)`.

En este proyecto la traslación es una de las bases del gameplay, porque casi todo se mueve cambiando su posición:

- `WX-78` se traslada horizontalmente.
- Los objetos caen por traslación vertical.
- Las garras y sombras se trasladan desde los bordes.
- La lluvia se mueve en diagonal.

---

## 2. Base matemática de la traslación en 2D

Si un punto original es `(x, y)` y queremos moverlo por un vector de traslación `(tx, ty)`, la nueva posición es:

```text
x' = x + tx
y' = y + ty
```

Esto significa que:

- `tx` controla cuánto se mueve en el eje horizontal
- `ty` controla cuánto se mueve en el eje vertical

En forma matricial, usando coordenadas homogéneas:

```text
[x']   [1 0 tx] [x]
[y'] = [0 1 ty] [y]
[1 ]   [0 0 1 ] [1]
```

En un videojuego, esta operación se repite constantemente cuadro por cuadro. Por eso la traslación normalmente se implementa actualizando variables como:

```python
self.x += dx
self.y += dy
```

---

## 3. Lógica conceptual en el juego

En `Lights Out`, la traslación no es solo una transformación matemática: también representa la lógica del sistema.

- Si el jugador presiona izquierda o derecha, `WX-78` cambia su coordenada `x`.
- Si un objeto aparece arriba de la pantalla, su coordenada `y` aumenta para simular caída.
- Si una garra entra desde un borde, su coordenada `x` avanza hacia la fogata.
- Si la lluvia está activa, cada gota cambia `x` y `y` para dar la sensación de viento diagonal.

Entonces, en este juego la traslación conecta tres cosas:

1. **Matemática**: suma de desplazamientos
2. **Lógica**: decidir hacia dónde moverse
3. **Renderizado**: dibujar el objeto en su nueva posición

---

## 4. Implementación en el juego

### Caso 1: traslación horizontal de WX-78

Código de `WX78.mover`:

```python
vel = self.velocidad * (1.8 if self.turbo > 0 else 1.0)
mov_x = 0
if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    mov_x -= vel
if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    mov_x += vel
self.x += mov_x
```

### Qué hace

- Si el jugador va a la izquierda, el desplazamiento horizontal es negativo.
- Si va a la derecha, el desplazamiento horizontal es positivo.
- La traslación se aplica sumando `mov_x` a `self.x`.

### Interpretación matemática

```text
x' = x + mov_x
y' = y
```

Aquí solo cambia el eje `x`, por eso se trata de una traslación horizontal.

Además, el personaje se limita a una zona de movimiento:

```python
self.x = max(FOG_X - ZONA_MARGEN, min(FOG_X + ZONA_MARGEN - self.w, self.x))
```

Eso evita que el jugador salga del área jugable.

---

### Caso 2: traslación vertical de objetos que caen

Código de `Objeto.actualizar`:

```python
self.y += self.vel
self.t += dt
```

### Qué hace

- Cada objeto aparece arriba de la pantalla.
- En cada actualización su coordenada `y` aumenta.
- Al aumentar `y`, el objeto baja visualmente.

### Interpretación matemática

```text
x' = x
y' = y + vel
```

Aquí la traslación ocurre solo en el eje vertical.

Los objetos usan esta lógica para caer:

- `leña`
- `carbon`
- `engrane`
- `rayo`

---

### Caso 3: traslación horizontal de garras

Código de `Garra.actualizar`:

```python
if not self.espantada:
    self.x += self.dir * self.velocidad
else:
    self.x -= self.dir * 9
```

### Qué hace

- `self.dir` vale `1` si la garra viene desde la izquierda.
- `self.dir` vale `-1` si viene desde la derecha.
- Mientras avanza hacia la fogata, su posición cambia en `x`.
- Si es espantada, la traslación se invierte y retrocede.

### Interpretación matemática

Cuando avanza:

```text
x' = x + dir * velocidad
```

Cuando retrocede:

```text
x' = x - dir * 9
```

Este es un buen ejemplo de cómo la traslación depende del **estado lógico** del enemigo.

---

### Caso 4: traslación horizontal de sombras

Código de `Sombra.actualizar`:

```python
self.x += self.dir * self.vel
```

### Qué hace

- Las sombras aparecen fuera de pantalla.
- Después avanzan hacia el centro.
- Igual que las garras, usan una dirección positiva o negativa según el lado.

### Interpretación matemática

```text
x' = x + dir * vel
```

Este movimiento es simple, pero muy importante porque genera presión lateral constante sobre el jugador.

---

### Caso 5: traslación diagonal de la lluvia

Código de `actualizar_lluvia`:

```python
y += vel * dt
x -= vel * 0.35 * dt
```

### Qué hace

- La gota baja porque `y` aumenta.
- La gota también se desplaza horizontalmente, simulando viento.
- Por eso la trayectoria no es recta vertical, sino diagonal.

### Interpretación matemática

```text
x' = x + tx
y' = y + ty
```

En este caso:

```text
tx = -vel * 0.35 * dt
ty =  vel * dt
```

Este es el ejemplo más claro de traslación bidimensional en el juego, porque cambian `x` y `y` al mismo tiempo.

---

## 5. Relación con colisiones

La traslación no solo mueve sprites; también cambia las colisiones del juego.

Cada entidad tiene un rectángulo de colisión:

```python
def rect(self):
    return pygame.Rect(self.x, self.y, self.w, self.h)
```

Cuando `x` o `y` cambian por traslación, ese rectángulo también cambia de posición.  
Eso permite detectar si:

- `WX-78` recoge un objeto
- una `garra` toca al jugador
- una `sombra` entra en contacto

Por eso la traslación afecta directamente la mecánica de juego, no solo la parte visual.

---

## 6. Diferencia entre traslación matemática y traslación en código

### Matemáticamente

La traslación es una suma entre la posición actual y un vector de desplazamiento:

```text
(x, y) -> (x + tx, y + ty)
```

### En el juego

Eso se traduce a instrucciones como:

```python
self.x += mov_x
self.y += self.vel
self.x += self.dir * self.vel
```

La idea es la misma: cambiar coordenadas para mover un objeto en el plano.

---

## 7. Conclusión

La traslación en `Lights Out` es una transformación 2D esencial para el funcionamiento del juego.  
Se implementa moviendo entidades por medio de sumas sobre sus coordenadas `x` y `y`.

Se aplica en:

- el movimiento horizontal de `WX-78`
- la caída vertical de los objetos
- el avance lateral de garras y sombras
- el movimiento diagonal de la lluvia

Matemáticamente, todo se basa en:

```text
x' = x + tx
y' = y + ty
```

Lógicamente, la dirección y la velocidad dependen del estado del juego.  
En código, esto se refleja en actualizaciones continuas de posición dentro de los métodos `mover` y `actualizar`.

Por lo tanto, la traslación es una de las transformaciones más importantes del proyecto, porque sostiene el movimiento, las colisiones y el ritmo de la jugabilidad.

---

## 8. Referencia al código del proyecto

Las partes principales donde se usa traslación en `LightsOut.py` son:

- `WX78.mover()`
- `Objeto.actualizar()`
- `Garra.actualizar()`
- `Sombra.actualizar()`
- `actualizar_lluvia()`

Ejemplos directos:

```python
self.x += mov_x
```

```python
self.y += self.vel
```

```python
self.x += self.dir * self.velocidad
```

```python
y += vel * dt
x -= vel * 0.35 * dt
```

---

## 9. Idea clave para exposición

Si te preguntan “¿cómo se usa la traslación en tu juego?”, una respuesta corta sería:

> La traslación en mi juego se aplica en 2D y consiste en mover objetos cambiando sus coordenadas `x` y `y`. Matemáticamente se basa en sumar un vector de desplazamiento a la posición original. En mi código la uso para mover a WX-78, hacer caer objetos, desplazar garras y sombras, y animar la lluvia en diagonal.
