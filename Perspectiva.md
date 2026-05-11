# Perspectiva en Lights Out

## 1. Concepto

La **perspectiva** es una forma de representar profundidad en una imagen.  
En gráficos por computadora, sirve para que los objetos parezcan estar más cerca o más lejos del observador.

En un entorno **3D**, la perspectiva normalmente depende de la profundidad `z`: los objetos más cercanos se ven más grandes y los lejanos más pequeños.  
En `Lights Out`, el juego es **2D**, así que no se usa perspectiva 3D real. En su lugar, se usa una **perspectiva visual 2D** o **pseudo-perspectiva**.

Esto significa que el juego crea sensación de profundidad usando:

- posición en pantalla
- orden de dibujo por capas
- luz y oscuridad
- tamaño visual de sprites
- ubicación de la fogata como punto central

---

## 2. Base matemática de la perspectiva 3D

En perspectiva 3D, un punto del mundo `(x, y, z)` se proyecta sobre una pantalla 2D. Una forma común de expresarlo es:

```text
x_pantalla = f * (x / z)
y_pantalla = f * (y / z)
```

Donde:

- `x` y `y` son las coordenadas del punto en el mundo
- `z` es la profundidad
- `f` es la distancia focal o intensidad de la perspectiva

La idea principal es:

```text
entre mayor sea z, más pequeño se ve el objeto
```

Por eso en 3D:

- objetos cercanos: `z` pequeño, se ven grandes
- objetos lejanos: `z` grande, se ven pequeños

---

## 3. Por qué no se usa perspectiva 3D en este juego

`Lights Out` no maneja coordenada `z`, cámara 3D ni modelos tridimensionales.  
Todos los elementos se dibujan directamente en una ventana 2D usando coordenadas:

```text
(x, y)
```

Eso corresponde más a una proyección ortográfica 2D:

```text
x_pantalla = x
y_pantalla = y
```

En esta proyección, no hay división entre profundidad. Los objetos no cambian de tamaño automáticamente por estar “más lejos”; su tamaño se decide manualmente mediante escalamiento y diseño visual.

---

## 4. Lógica conceptual en el juego

Aunque no hay perspectiva 3D real, el juego sí construye una sensación de espacio.

La escena está organizada así:

- fondo oscuro con estrellas
- fogata al centro como punto visual principal
- zona de movimiento horizontal de `WX-78`
- objetos que caen desde arriba
- garras y sombras que entran desde los lados
- lluvia y HUD por encima de la escena

Esta organización genera una perspectiva 2D porque el jugador entiende qué está al fondo, qué está en la zona jugable y qué elementos están encima de otros.

---

## 5. Implementación mediante coordenadas

El juego define puntos base para organizar la escena:

```python
FOG_X = ANCHO // 2
FOG_Y = ALTO // 2 + 40
ZONA_Y = FOG_Y - 10
ZONA_MARGEN = 200
```

### Qué hace

- `FOG_X` coloca la fogata en el centro horizontal.
- `FOG_Y` la coloca ligeramente debajo del centro vertical.
- `ZONA_Y` define la línea donde se mueve `WX-78`.
- `ZONA_MARGEN` limita la zona jugable alrededor de la fogata.

Esto crea una composición visual con profundidad 2D: la fogata funciona como centro de la escena y los peligros se acercan desde los bordes hacia ella.

---

## 6. Implementación mediante orden de renderizado

Una parte importante de la perspectiva 2D es el orden en que se dibujan los elementos.

Código principal de dibujo:

```python
pantalla.fill(NEGRO)
dibujar_estrellas(pantalla, timer)
dibujar_luz(pantalla, FOG_X, FOG_Y, radio_luz, timer)
pantalla.blit(zs, (FOG_X - ZONA_MARGEN, ZONA_Y - 30))
dibujar_fogata(pantalla, FOG_X, FOG_Y, timer)
for obj in objetos:
    obj.dibujar(pantalla)
for g in garras:
    g.dibujar(pantalla)
for s in sombras:
    s.dibujar(pantalla)
wx.dibujar(pantalla, timer)
dibujar_lluvia(pantalla, lluvia)
```

### Qué hace

El render se organiza por capas:

1. fondo
2. estrellas
3. luz/oscuridad
4. zona jugable
5. fogata
6. objetos
7. enemigos
8. `WX-78`
9. lluvia
10. HUD

Esto genera una perspectiva visual porque los elementos dibujados después aparecen por encima de los anteriores.

---

## 7. Implementación mediante luz y oscuridad

La perspectiva del juego también depende de la visibilidad.  
La fogata funciona como el centro visual y su radio de luz cambia según el estado del juego:

```python
radio_luz = int(80 + (fogata / fogata_max) * 140)
dibujar_luz(pantalla, FOG_X, FOG_Y, radio_luz, timer)
```

### Qué hace

- Si la fogata tiene mucha energía, el radio de luz es mayor.
- Si la fogata se apaga, el radio se reduce.
- La oscuridad cubre más pantalla y los enemigos se sienten más cercanos o peligrosos.

Esto no es perspectiva 3D, pero sí es perspectiva ambiental: el jugador percibe profundidad y amenaza por cómo la luz revela u oculta partes del escenario.

---

## 8. Implementación mediante pseudo-profundidad

En un juego 2D, la profundidad puede sugerirse con reglas visuales.

En `Lights Out`, se usa:

- `y` para ubicar personajes y amenazas dentro de una franja jugable
- capas para decidir qué se ve encima
- luz para separar primer plano y fondo
- lluvia como capa atmosférica superior

Por ejemplo, la lluvia se dibuja después de `WX-78`:

```python
wx.dibujar(pantalla, timer)
if lluvia_activa():
    dibujar_lluvia(pantalla, lluvia)
```

Eso hace que la lluvia parezca estar frente a la cámara o por encima de toda la escena.

---

## 9. Diferencia entre perspectiva real y perspectiva usada en el juego

### Perspectiva 3D real

Usa profundidad:

```text
x_pantalla = f * (x / z)
y_pantalla = f * (y / z)
```

Requiere:

- eje `z`
- cámara
- proyección
- cambio de tamaño según distancia

### Perspectiva de `Lights Out`

Usa una organización 2D:

```text
x_pantalla = x
y_pantalla = y
```

Y simula profundidad con:

- orden de dibujo
- posición en pantalla
- iluminación
- escalamiento manual
- composición visual

---

## 10. Relación con otros conceptos

La perspectiva del juego se apoya en transformaciones ya usadas en el proyecto:

- **traslación**: mueve objetos, enemigos y lluvia por la pantalla
- **escalamiento**: ajusta el tamaño de sprites para que tengan proporción visual
- **rotación**: orienta garras y anima engranes
- **sesgado**: inclina visualmente la lluvia

La perspectiva no reemplaza esas transformaciones; las organiza para que la escena tenga profundidad visual.

---

## 11. Conclusión

La perspectiva en `Lights Out` se implementa como una **pseudo-perspectiva 2D**, no como una perspectiva 3D real.

Matemáticamente, una perspectiva 3D usaría:

```text
x_pantalla = f * (x / z)
y_pantalla = f * (y / z)
```

Pero el juego usa coordenadas 2D directas:

```text
x_pantalla = x
y_pantalla = y
```

La profundidad se logra mediante:

- capas de dibujo
- posición de los elementos
- fogata como centro visual
- radio dinámico de luz
- lluvia y HUD como capas superiores

Por lo tanto, la perspectiva en este proyecto es principalmente visual y de composición. Sirve para que el jugador entienda qué elementos están al fondo, cuáles pertenecen al área jugable y cuáles aparecen encima de la escena.

---

## 12. Referencia al código del proyecto

Las partes principales relacionadas con perspectiva en `LightsOut.py` son:

- constantes de composición: `FOG_X`, `FOG_Y`, `ZONA_Y`, `ZONA_MARGEN`
- función `dibujar_luz()`
- bloque principal de renderizado
- orden de dibujo de fogata, objetos, enemigos, jugador y lluvia

Ejemplos directos:

```python
FOG_X = ANCHO // 2
FOG_Y = ALTO // 2 + 40
ZONA_Y = FOG_Y - 10
```

```python
radio_luz = int(80 + (fogata / fogata_max) * 140)
```

```python
dibujar_fogata(pantalla, FOG_X, FOG_Y, timer)
for obj in objetos:
    obj.dibujar(pantalla)
for g in garras:
    g.dibujar(pantalla)
for s in sombras:
    s.dibujar(pantalla)
wx.dibujar(pantalla, timer)
```

---

## 13. Idea clave para exposición

Si te preguntan “¿cómo se usa la perspectiva en tu juego?”, una respuesta corta sería:

> Mi juego no usa perspectiva 3D real porque es un juego 2D. En lugar de eso usa pseudo-perspectiva: organiza la escena por capas, posiciones y luz. La fogata funciona como centro visual, los enemigos entran desde los bordes, la lluvia se dibuja encima y el radio de luz crea profundidad ambiental. Matemáticamente, no uso división por `z`; uso coordenadas directas `(x, y)` y composición visual.
