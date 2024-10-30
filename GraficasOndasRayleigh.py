#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:04:30 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Grafica del desplazamiento en funcion de la profundidad
# Parámetros
A_x = 1  # Amplitud de la onda
k_x = 2 * np.pi  # Número de onda
omega = 2 * np.pi  # Frecuencia angular
z = np.linspace(0, 3, 1500)  # Profundidad normalizada con la longitud de onda
t = 0  # Tiempo fijo para esta gráfica

# Ecuaciones de desplazamiento en función de la profundidad normalizada
u_x_z = A_x * (np.exp(-0.85 * k_x * z) - 0.58 * np.exp(-0.39 * k_x * z))
u_z_z = A_x * (-0.85 * np.exp(-0.85 * k_x * z) + 1.47 * np.exp(-0.39 * k_x * z))

# Gráfica
plt.figure(figsize=(6, 10))
plt.plot(u_x_z, z, label=r"$u_x$ (Desplazamiento horizontal)")
plt.plot(u_z_z, z, "--",label=r"$u_z$ (Desplazamiento vertical)")
plt.gca().invert_yaxis()  # Invertir eje y para que aumente con la profundidad
plt.title(r"Desplazamientos $u_x$ y $u_z$ en función de la profundidad normalizada")
plt.xlabel("Desplazamientos")
plt.ylabel(r"Profundidad normalizada $z/\lambda_x$")
plt.legend()
plt.grid(True)
plt.show()

#Animacion del movimiento eliptico
# Parámetros de la animación
A_x = 1  # Amplitud
omega = 2 * np.pi  # Frecuencia angular
t_values = np.linspace(0, 2 * np.pi, 500)

# Desplazamientos ajustados para movimiento elíptico retrógrado
u_x_surface = 0.42 * A_x * np.sin(omega * t_values)
u_z_surface = -0.62 * A_x * np.cos(omega * t_values)

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(5, 6))

# Trayectoria completa (línea punteada)
ax.plot(u_x_surface, u_z_surface, 'r--', label="Trayectoria completa")

# Línea que muestra solo una pequeña porción del movimiento
line, = ax.plot([], [], 'o-', lw=2, label="Movimiento actual")

# Configuración del gráfico
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.7, 0.7)
ax.set_xlabel(r'$U_x$')
ax.set_ylabel(r'$U_z$')
ax.grid(True)
ax.legend()

# Función de inicialización
def init():
    line.set_data([], [])
    return line,

# Función de actualización
tail_length = 10  # Longitud de la "cola" visible del movimiento

def update(frame):
    start = max(0, frame - tail_length)  # Calcula el inicio de la "cola"
    x = u_x_surface[start:frame]
    y = u_z_surface[start:frame]
    line.set_data(x, y)
    return line,

# Creación de la animación
ani = animation.FuncAnimation(fig, update, frames=len(t_values), \
                              init_func=init, blit=True, interval=50)

# Guardar la animación en formato GIF
ani.save('Rayleigthelipse_circuloload_dashed.gif', writer='pillow')

#Desplazamiento en funcion del tiempo
# Desplazamientos Ux y Uz en función del tiempo
u_x_time = 0.42 * A_x * np.sin(omega * t_values)
u_z_time = 0.62 * A_x * np.cos(omega * t_values)

# Gráfica
plt.figure(figsize=(8, 6))
plt.plot(t_values, u_x_time, label=r"$u_x$")
plt.plot(t_values, u_z_time,"--", label=r"$u_z$")
plt.title(r"Desplazamientos $u_x$ y $u_z$ en función del tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Desplazamientos")
plt.legend()
plt.grid(True)
plt.show()