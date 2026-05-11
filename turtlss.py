import turtle
import math

# Configuración inicial
screen = turtle.Screen()
screen.setup(600, 600)
t = turtle.Turtle()
t.speed(5)
t.pensize(2)

def proyectar(x, y, z):
    """ Convierte coordenadas 3D a 2D usando una proyección caballera """
    # El ángulo de 45 grados da la sensación de profundidad
    angulo = math.radians(45)
    factor = 0.5  # Qué tan "larga" se ve la profundidad
   
    px = x + (z * factor * math.cos(angulo))
    py = y + (z * factor * math.sin(angulo))
    return px, py

def mover_a(x, y, z):
    px, py = proyectar(x, y, z)
    t.goto(px, py)

def dibujar_cubo(tamano):
    # Definimos los 8 vértices (x, y, z)
    # Cara frontal (z=0) y Cara trasera (z=tamano)
    v = [
        (0, 0, 0), (tamano, 0, 0), (tamano, tamano, 0), (0, tamano, 0), # Frontal
        (0, 0, tamano), (tamano, 0, tamano), (tamano, tamano, tamano), (0, tamano, tamano) # Trasera
    ]

    # 1. Dibujar cara frontal (Azul)
    t.color("blue")
    t.penup()
    mover_a(*v[0])
    t.pendown()
    for i in [1, 2, 3, 0]:
        mover_a(*v[i])

    # 2. Dibujar cara trasera (Rojo)
    t.color("red")
    t.penup()
    mover_a(*v[4])
    t.pendown()
    for i in [5, 6, 7, 4]:
        mover_a(*v[i])

    # 3. Unir las esquinas (Conexiones de profundidad - Negro)
    t.color("black")
    for i in range(4):
        t.penup()
        mover_a(*v[i])
        t.pendown()
        mover_a(*v[i+4])

# Ejecutar el dibujo
dibujar_cubo(150)
t.hideturtle()
screen.mainloop()