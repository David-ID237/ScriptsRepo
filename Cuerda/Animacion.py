#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 18:38:47 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros
x = np.linspace(0, 1, 500)  # Dominio espacial
t_values = np.linspace(0, 2, 100)  # Valores de tiempo
A = 1.0  # Amplitud de la onda

# Configuración de la figura para la animación
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 1)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], lw=2)

# Títulos y etiquetas
plt.grid(True)
ax.set_title(r'Animación de $u(x,t) = A\cos(\pi t - 2\pi x)$')
ax.set_xlabel('Posición (x)')
ax.set_ylabel('Desplazamiento u(x,t)')

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de animación
def animate(t):
    u_xt = A * np.cos(np.pi * t - 2 * np.pi * x)
    line.set_data(x, u_xt)
    return line,

# Creación de la animación
ani = animation.FuncAnimation(fig, animate, frames=t_values, init_func=init, blit=True)

# Guardar la animación como un archivo GIF
ani.save('animacion_onda.gif', writer='imagemagick')

# Mostrar la animación
plt.show()

# Gráfica de u(x,t)
plt.figure(figsize=(10, 6))
plt.plot(x, A * np.cos(np.pi * 1 - 2 * np.pi * x), label='t=1s')
plt.xlabel('Posición (x)')
plt.ylabel('Desplazamiento u(x,t)')
plt.title('Gráfica de $u(x,t)$ en t=1s')
plt.grid(True)
plt.legend()
plt.show()
