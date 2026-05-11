# 🕯️ LIGHTS OUT — Manual Técnico

### _La Prisión de Charlie · WX-78_

---

> _"La oscuridad no te odia, pequeña máquina. Solo tiene hambre. Y tú eres lo único que brilla."_
> — Charlie, Reina de la Oscuridad

---

## 📖 INTRODUCCIÓN

**Lights Out** es un videojuego de supervivencia 2D de tipo _catcher_ desarrollado en Python con la librería `pygame-ce`. Inspirado en el universo de _Don't Starve Together_ de Klei Entertainment, el jugador toma el control de **WX-78**, un robot atrapado en una dimensión oscura controlada por **Charlie**, la Reina de la Oscuridad.

El juego fue desarrollado como proyecto personal/académico, construyendo desde cero todas las mecánicas, visuales y sistemas de dificultad progresiva sin el uso de motores externos ni assets de terceros. Todos los elementos visuales fueron dibujados proceduralmente usando las herramientas de dibujo de Pygame.

El juego cuenta con dos modos de juego: **Modo Normal** (5 noches con final de victoria) y **Modo Endless** (supervivencia infinita), ambos con dificultad escalada por noche.

---

## 🛠️ HERRAMIENTAS USADAS

| Herramienta        | Versión | Uso                                         |
| ------------------ | ------- | ------------------------------------------- |
| **Python**         | 3.12+   | Lenguaje principal de desarrollo            |
| **pygame-ce**      | Latest  | Motor de juego, renderizado y eventos       |
| **math**           | Stdlib  | Cálculos trigonométricos para animaciones   |
| **random**         | Stdlib  | Generación procedural de enemigos y objetos |
| **sys**            | Stdlib  | Control de salida del programa              |
| **VS Code**        | Latest  | Editor de código                            |
| **macOS Terminal** | —       | Ejecución y gestión del proyecto            |

### ¿Por qué `pygame-ce`?

`pygame-ce` es un fork comunitario mantenido activamente de la librería original `pygame`. Ofrece mejor rendimiento, correcciones de bugs modernas y compatibilidad con Python 3.12+. Se instala con:

```bash
pip3 install pygame-ce
```

---

## 🎨 PALETA DE COLORES

La paleta fue diseñada para evocar la atmósfera fría y nocturna de _Don't Starve Together_, con el fuego como único punto de calor y vida en la pantalla.

### Colores Base (Fondo y UI)

| Nombre      | RGB               | Uso                                   |
| ----------- | ----------------- | ------------------------------------- |
| `NEGRO`     | `(9, 9, 15)`      | Fondo principal, oscuridad total      |
| `AZUL_DARK` | `(13, 14, 26)`    | Capas intermedias de oscuridad        |
| `AZUL_MID`  | `(31, 45, 74)`    | Bordes de UI, separadores             |
| `GRIS_AZUL` | `(74, 90, 122)`   | Texto secundario, elementos inactivos |
| `LUNA`      | `(168, 192, 212)` | Texto principal, WX-78 base           |
| `BLANCO_FR` | `(212, 228, 240)` | Títulos, elementos destacados         |

### Colores de Acción (Fuego y Vida)

| Nombre      | RGB              | Uso                          |
| ----------- | ---------------- | ---------------------------- |
| `NARANJA`   | `(212, 116, 42)` | Barra de fogata, leña        |
| `AMBAR`     | `(232, 160, 64)` | Carbón, puntajes altos       |
| `FUEGO`     | `(245, 192, 96)` | Llama central, victoria      |
| `ROJO`      | `(139, 32, 32)`  | Game over, daño crítico      |
| `VERDE`     | `(60, 160, 80)`  | Barra de vida, engranes      |
| `ELECTRICO` | `(80, 180, 255)` | Turbo, invencibilidad, rayos |

### Colores de Enemigos

| Elemento        | RGB               | Descripción                  |
| --------------- | ----------------- | ---------------------------- |
| Garra normal    | `(60, 20, 80)`    | Morado oscuro amenazante     |
| Garra rápida    | `(120, 10, 10)`   | Rojo intenso al acelerar     |
| Garra espantada | `(180, 100, 200)` | Lila al ser repelida         |
| Sombra cuerpo   | `(25, 10, 40)`    | Negro púrpura casi invisible |
| Sombra ojos     | `(180, 80, 220)`  | Violeta brillante            |

---

## 🖼️ ESQUEMA VISUAL

```
┌─────────────────────────────────────────────────────────┐
│  ✦ · · ·  NOCHES: 2/5  [=========>   ]  · · · ✦       │  ← HUD superior
│  🔥 FOGATA [████████░░]    Puntos: 340                  │
│  ❤ VIDA   [██████░░░░]                                  │
│  ⚡ TURBO  [███░░░░░░░]                                  │
│                                                         │
│      ⚙  ↓      ⚡ ↓        🪵 ↓                        │  ← Objetos cayendo
│                                                         │
│  👾──────────────────────────────────────────────👾     │  ← Sombras laterales
│                                                         │
│  🖐←←←          🔥🔥🔥          →→→🖐                  │  ← Garras + fogata
│            [  zona de WX-78  ]                          │
│                   🤖                                    │  ← WX-78
│  ◄────────── 200px ──────────►                          │  ← Zona de movimiento
└─────────────────────────────────────────────────────────┘
```

### Capas de renderizado (orden de dibujo)

1. **Fondo negro** — `pantalla.fill(NEGRO)`
2. **Estrellas** — puntos parpadeantes aleatorios
3. **Luz dinámica** — superficie SRCALPHA con gradiente radial
4. **Fogata** — leños, brasas, llamas poligonales animadas
5. **Objetos** — leña, carbón, engranes, rayos
6. **Garras** — entidades laterales con fases
7. **Sombras** — figuras oscuras con aura de peligro
8. **WX-78** — robot con aura de turbo opcional
9. **Mensajes flotantes** — feedback visual de eventos
10. **HUD** — barras e información

---

## 🔤 TIPOGRAFÍA

El juego utiliza **fuentes del sistema** cargadas con `pygame.font.SysFont` para garantizar compatibilidad multiplataforma sin archivos externos.

| Fuente            | Estilo | Tamaño | Uso                            |
| ----------------- | ------ | ------ | ------------------------------ |
| `Belisa Plumilla` | Italic | 72px   | Título principal en menú       |
| `Belisa Plumilla` | Italic | 48px   | Textos de Game Over / Victoria |
| `Belisa Plumilla` | Normal | 28px   | Opciones del menú              |
| `Belisa Plumilla` | Normal | 22px   | Subtítulos e información       |
| `Belisa Plumilla` | Normal | 20px   | HUD durante el juego           |
| `Belisa Plumilla` | Normal | 14px   | Mensajes flotantes, hints      |

**Belisa Plumilla** fue elegida por su carácter serif clásico y levemente oscuro, que evoca la estética gótica/victoriana de _Don't Starve Together_ sin requerir fuentes externas. Su versión itálica en los títulos añade dramatismo narrativo.

---

## 📜 HISTORIA

En el corazón de _La Constante_ existe una dimensión que pocos conocen y de la que ninguno ha regresado: **La Prisión de Charlie**.

WX-78, el autómata de circuitos fríos y lógica implacable, fue capturado por la Reina de la Oscuridad y arrojado a este lugar sin luz, sin norte, sin fin aparente. Una dimensión donde la oscuridad no es ausencia de luz — es una presencia activa, hambrienta, con garras.

Charlie no destruyó a WX-78 de inmediato. En su lugar, lo observa. Lo prueba. Envía sus sombras, sus garras, sus criaturas a consumir lo único que mantiene vivo al robot: **la fogata**.

Los demás supervivientes están en camino. Quizás. WX-78 no tiene certeza. Solo sabe dos cosas:

> _La fogata debe seguir encendida._
> _Charlie no va a parar._

Si WX-78 sobrevive las noches de oscuridad total, la luz de _La Constante_ lo reclamará de vuelta. Si no... Charlie se lleva lo que siempre fue suyo.

---

## 🎯 OBJETIVO

### Modo Normal

Sobrevivir **5 noches completas** (30 segundos cada una) manteniendo la fogata encendida y a WX-78 con vida. Al completar la quinta noche, los supervivientes llegan y WX-78 es liberado.

### Modo Endless

No hay victoria posible. El objetivo es acumular el mayor puntaje posible sobreviviendo la mayor cantidad de noches. La dificultad escala infinitamente.

### Condiciones de derrota

- La barra de **fogata llega a 0** — Charlie entra sin restricciones
- La barra de **vida de WX-78 llega a 0** — el robot cae

---

## ⚙️ MECÁNICAS

### Mecánicas de Movimiento

**WX-78** se mueve horizontalmente con las teclas `←` / `→` o `A` / `D`, restringido a una zona de **200px a cada lado de la fogata**. Esta restricción obliga al jugador a tomar decisiones: ¿me acerco al peligro de la izquierda o agarro el combustible de la derecha?

```python
self.x = max(FOG_X - ZONA_MARGEN, min(FOG_X + ZONA_MARGEN - self.w, self.x))
```

### Mecánicas de la Fogata

La fogata consume combustible constantemente a una tasa de `3.0 + nivel × 0.4` unidades por segundo. El radio de luz visible en pantalla es proporcional al nivel de fogata:

```python
radio_luz = int(80 + (fogata / fogata_max) * 140)
```

Cuando la fogata está al máximo el radio es 220px. Cuando está casi vacía, cae a 80px — haciendo el juego casi completamente oscuro.

### Objetos que Caen

Caen desde la parte superior dentro de la zona de movimiento de WX-78:

| Objeto         | Efecto                       | Puntos | Desde   |
| -------------- | ---------------------------- | ------ | ------- |
| 🪵 **Leña**    | +25 fogata                   | +10    | Noche 1 |
| 🪨 **Carbón**  | +40 fogata                   | +20    | Noche 1 |
| ⚙️ **Engrane** | +25 vida                     | +15    | Noche 1 |
| ⚡ **Rayo**    | Turbo 4s + Invencibilidad 4s | +10    | Noche 2 |

La velocidad de caída escala con el nivel: `vel = random.uniform(2.5, 4.0) + nivel × 0.25`

El intervalo entre spawns decrece por noche hasta un mínimo de 0.7 segundos.

### Garras de Charlie

Las garras emergen desde los bordes izquierdo y derecho de la pantalla y avanzan hacia la fogata en **dos fases**:

**Fase lenta** (primeros 2 segundos): `vel = 0.6 + nivel × 0.05`
→ Da tiempo al jugador de reaccionar y posicionarse

**Fase rápida** (después de 2 segundos): `vel = 3.5 + nivel × 0.4`
→ Se vuelven rojas con indicador `!` como advertencia visual

```python
if self.fase == "lenta" and self.fase_timer >= 2.0:
    self.fase = "rapida"
    self.velocidad = self.vel_rapida
```

**Interacción con WX-78:**

- Tocarlas las **espanta** (retroceden) pero hacen daño: `10 + nivel × 2` HP
- Con turbo activo el daño se reduce a la mitad
- Si llegan a la fogata sin ser espantadas: `-18` fogata

Desde noche 3 hay 40% de probabilidad de que aparezcan **2 garras simultáneas**.

### Sombras de Charlie

Aparecen desde noche 2 avanzando lentamente desde los costados:

| Noche | Cantidad máxima simultánea |
| ----- | -------------------------- |
| 2     | 1 sombra                   |
| 3     | hasta 2 sombras            |
| 4+    | hasta 3 sombras            |

**Comportamiento:**

- Se mueven hacia la fogata sin detenerse
- Si **tocan a WX-78**: `-8` vida, WX queda aturdido 0.4s, sombra desaparece
- Si **llegan a la fogata**: `-12` fogata, sombra desaparece
- Con **invencibilidad activa**: no hacen daño pero igual desaparecen al contacto

### Sistema de Turbo e Invencibilidad

Al agarrar un rayo `⚡`:

- Velocidad de WX-78 multiplicada por **×1.8** durante 4 segundos
- **Invencibilidad completa** durante 4 segundos (garras y sombras no dañan)
- El aura azul eléctrica indica visualmente el estado activo
- Una barra de turbo en el HUD muestra el tiempo restante

### Sistema de Daño y Cooldowns

Para evitar que el daño sea injusto e instantáneo, cada fuente de daño tiene su propio cooldown:

| Fuente              | Daño         | Cooldown |
| ------------------- | ------------ | -------- |
| Garra (contacto)    | 10 + nivel×2 | 0.5s     |
| Sombra (proximidad) | 8 HP         | 1.5s     |
| Garra en fogata     | 18 fogata    | —        |
| Sombra en fogata    | 12 fogata    | —        |

### Dificultad Progresiva

| Noche | Novedades                                            |
| ----- | ---------------------------------------------------- |
| 1     | Leña, carbón, engranes, garras básicas               |
| 2     | Rayos, sombras (1 a la vez), garras más rápidas      |
| 3     | Hasta 2 sombras, posibilidad de 2 garras simultáneas |
| 4     | Hasta 3 sombras, garras muy agresivas                |
| 5     | Todo al máximo, fogata se consume más rápido         |

---

## 📋 INSTRUCCIONES

### Instalación

```bash
# 1. Instalar Python 3.12+
# https://www.python.org/downloads/

# 2. Instalar pygame-ce
pip3 install pygame-ce

# 3. Ejecutar el juego
python3 LightsOut.py
```

### Controles

| Tecla     | Acción                          |
| --------- | ------------------------------- |
| `←` o `A` | Mover WX-78 a la izquierda      |
| `→` o `D` | Mover WX-78 a la derecha        |
| `↑` / `↓` | Navegar en el menú              |
| `ENTER`   | Confirmar selección / continuar |

### Cómo jugar

1. Desde el menú elige **Modo Normal** o **Modo Endless**
2. WX-78 aparece centrado frente a la fogata
3. **Atrapa** la leña y el carbón que caen para mantener la fogata encendida
4. **Recoge engranes** para recuperar tu vida
5. **Intercepta las garras** antes de que lleguen a la fogata — pero cuidado, te harán daño al tocarlas
6. **Evita las sombras** o activa el turbo con un rayo para atravesarlas sin daño
7. En Modo Normal: sobrevive las 5 noches para ganar

### Lectura del HUD

```
🔥 FOGATA  [████████░░]  ← Si llega a 0, game over
❤  VIDA    [██████░░░░]  ← Si llega a 0, game over
⚡ TURBO   [███░░░░░░░]  ← Solo aparece cuando está activo

         Noche 2/5  [=======>   ]
                    ↑ Progreso de la noche actual
```

---

## 🏁 FINALES

### Victoria — Modo Normal

> _"WX-78 sobrevivió."_

Al completar las 5 noches, la pantalla muestra el mensaje de victoria con la fogata encendida al máximo. Los supervivientes llegaron. WX-78 regresa a La Constante.

**Condición:** `noche_actual > noches_normal (5)`

### Derrota — Fogata Apagada

> _"La fogata se apagó..."_

La barra de fogata llegó a cero. Charlie entró sin restricciones. La oscuridad ganó.

**Condición:** `fogata <= 0`

### Derrota — WX-78 Cayó

> _"WX-78 cayó..."_

Las garras y sombras acumularon suficiente daño para destruir al robot.

**Condición:** `wx.vida <= 0`

### Modo Endless — No hay final

En Modo Endless no existe victoria. El contador de noches sube indefinidamente, la dificultad escala sin límite y el puntaje es la única métrica de éxito. El juego termina únicamente por derrota.

---

## 📊 RESUMEN DE VARIABLES CLAVE

| Variable           | Valor inicial | Descripción                      |
| ------------------ | ------------- | -------------------------------- |
| `fogata`           | 100.0         | Energía de la fogata             |
| `wx.vida`          | 100           | Vida de WX-78                    |
| `noche_duracion`   | 30.0s         | Duración de cada noche           |
| `noches_normal`    | 5             | Noches para ganar en modo normal |
| `spawn_intervalo`  | 2.0s          | Tiempo entre objetos (decrece)   |
| `garra_intervalo`  | 5.0s          | Tiempo entre garras (decrece)    |
| `sombra_intervalo` | 8.0s          | Tiempo entre sombras (decrece)   |
| `ZONA_MARGEN`      | 200px         | Radio de movimiento de WX-78     |

---

_Lights Out — Desarrollado con Python + pygame-ce_
_Fan concept inspirado en Don't Starve Together © Klei Entertainment_

---

> ✦ &nbsp; _Que la hoguera no se apague_ &nbsp; ✦
