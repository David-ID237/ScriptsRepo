#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 22:09:45 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Constantes
betha1 = 3.9  # km/s
betha2 = 4.6  # km/s
rho1 = 2.8  # g/cm^3
rho2 = 3.3  # g/cm^3
h = 40  # km

# Periodos
T_values = np.array([5, 10, 30])  # segundos

# c_x como vector de 3.9 a 4.6
c_x_values = np.linspace(3.9, 4.6, 1000)

# Definir constantes adicionales
mu1 = rho1 * betha1**2
mu2 = rho2 * betha2**2

# Definir omega para cada T
omega_values = 2 * np.pi / T_values

# Definir funciones xi, tan(omega*xi) y la ecuación de dispersión
def xi(c_x, betha1, h):
    # Definimos xi usando números complejos
    return (h / c_x) * np.sqrt(c_x**2 / betha1**2 - 1)

def tan_omega_xi(omega, xi):
    # Función tangente para omega*xi
    return np.tan(omega * xi)

def dispersion_eq(c_x, betha2, mu1, mu2, h):
    # Ecuación de dispersión de la onda de Love
    r_betha2 = np.sqrt(1 - c_x**2 / betha2**2)
    return ((mu2 * r_betha2) / mu1) * (h / (c_x * xi(c_x, betha1, h)))

# Función para encontrar la intersección entre las dos curvas, considerando el límite de dispersión
def find_intersections(omega, c_x_values, betha1, betha2, mu1, mu2, h):
    xi_values = xi(c_x_values, betha1, h)
    tan_values = tan_omega_xi(omega, xi_values)
    dispersion_values = dispersion_eq(c_x_values, betha2, mu1, mu2, h)

    # Definir una función que es la diferencia entre las dos curvas
    diff = lambda c_x: tan_omega_xi(omega, xi(c_x, betha1, h)) - dispersion_eq(c_x, betha2, mu1, mu2, h)

    # Encontrar los puntos donde la diferencia es cercana a 0
    intersections = []
    for i in range(len(c_x_values) - 1):
        # Verificamos que la ecuación de dispersión no caiga a cero (lo que significa que no existe solución)
        if dispersion_values[i] > 1e-3:  # Excluir valores muy pequeños
            if np.sign(tan_values[i] - dispersion_values[i]) != np.sign(tan_values[i + 1] - dispersion_values[i + 1]):
                # Encontrar el punto de intersección entre estos dos valores
                root = fsolve(diff, c_x_values[i])
                intersections.append(root[0])
        else:
            # Si la ecuación de dispersión es muy pequeña, dejamos de buscar intersecciones
            break

    return intersections

# Evaluar y graficar las funciones para cada periodo
for T, omega in zip(T_values, omega_values):
    xi_values = xi(c_x_values, betha1, h)
    tan_values = tan_omega_xi(omega, xi_values)
    dispersion_values = dispersion_eq(c_x_values, betha2, mu1, mu2, h)

    # Encontrar las intersecciones
    intersections = find_intersections(omega, c_x_values, betha1, betha2, mu1, mu2, h)

    # Crear figura y ejes
    fig, ax1 = plt.subplots()

    # Graficar las funciones en el primer eje (c_x)
    ax1.plot(c_x_values, tan_values, label=r'tan($\omega \xi$)', color='blue')
    ax1.plot(c_x_values, dispersion_values, label=r'Ec. dispersión', color='green')

    # Añadir etiquetas y leyendas al primer eje
    ax1.set_xlabel(r'$c_x$ (km/s)')
    ax1.set_ylabel('Valor')
    ax1.legend(loc='upper right')
    ax1.grid(True)

    # Establecer los límites en el eje y
    plt.ylim(-10, 10)
    plt.xlim(3.9, 4.6)

    # Crear segundo eje X para xi
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())  # Asegurar que ambos ejes X se alineen
    ax2.set_xticks(c_x_values[::100])  # Definir algunas marcas para el segundo eje
    ax2.set_xticklabels([f'{xi_value:.2f}' for xi_value in xi(c_x_values[::100], betha1, h)])
    ax2.set_xlabel(r'$\xi$')

    # Marcar las intersecciones en ambas curvas
    for root in intersections:
        ax1.plot(root, tan_omega_xi(omega, xi(root, betha1, h)), 'ro')

    # Mostrar el gráfico
    plt.title(f'Dispersión de Love - Periodo {T} s')
    plt.show()

    # Imprimir las intersecciones (modos)
    print(f"Intersecciones (modos) para el periodo {T} s: {intersections}")