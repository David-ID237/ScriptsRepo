#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 13:20:17 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros físicos
rho1 = 2800  # Densidad del medio 1 (kg/m^3)
rho2 = 3300  # Densidad del medio 2 (kg/m^3)
beta1 = 3900  # Velocidad de ondas SH en el medio 1 (m/s)
beta2 = 4600  # Velocidad de ondas SH en el medio 2 (m/s)

# Definir el rango de ángulos de incidencia (en radianes)
theta1 = np.linspace(0, np.pi/2, 500)  # De 0 a 90 grados

# Ley de Snell: calcular theta2 en función de theta1
# beta1 * sin(theta1) = beta2 * sin(theta2)
sin_theta2 = (beta1 / beta2) * np.sin(theta1)
# Asegurarse de que sin(theta2) no exceda 1 (condición física)
sin_theta2 = np.clip(sin_theta2, -1, 1)
theta2 = np.arcsin(sin_theta2)

# Coeficiente de reflexión R12
R12 = (rho1 * beta1 * np.cos(theta1) - rho2 * beta2 * np.cos(theta2)) / \
      (rho1 * beta1 * np.cos(theta1) + rho2 * beta2 * np.cos(theta2))

# Coeficiente de transmisión T12
T12 = (2 * rho1 * beta1 * np.cos(theta1)) / \
      (rho1 * beta1 * np.cos(theta1) + rho2 * beta2 * np.cos(theta2))

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(np.degrees(theta1), R12, label="Coeficiente de Reflexión $R_{12}$", color='r')
plt.plot(np.degrees(theta1), T12, label="Coeficiente de Transmisión $T_{12}$", color='b')

# Añadir etiquetas y leyenda
plt.xlabel("Ángulo de Incidencia $\Theta_1$ (grados)")
plt.ylabel("Coeficiente")
plt.title("Coeficientes de Reflexión y Transmisión en una interfaz sólido-sólido")
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()
