#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:59:00 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt

# Definición de parámetros
W0 = 1.0  # Frecuencia natural
Xi_values = np.linspace(0.1, 2.1, 15)  # Valores de amortiguamiento

# Rango de frecuencias
omega = np.linspace(0, 2*W0, 500)

# Configuración de la figura
plt.figure(figsize=(14, 6))

# Gráfica del espectro de amplitud
plt.subplot(1, 2, 1)
for Xi in Xi_values:
    amplitude_spectrum = 1 / np.sqrt((omega**2 - W0**2)**2 + (2 * Xi * omega)**2)
    plt.plot(omega, amplitude_spectrum, label=f'Xi = {Xi:.2f}')
plt.title('Espectro de Amplitud |Y(w)| para diferentes Xi')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$|Y(\omega)|$')
plt.legend()
plt.grid(True)

# Gráfica del espectro de fase
plt.subplot(1, 2, 2)
for Xi in Xi_values:
    phase_spectrum = np.arctan2(-2 * Xi * omega, omega**2 - W0**2)
    #phase_spectrum = np.arctan((-2 * Xi * omega)/ (omega**2 - W0**2))
    plt.plot(omega, phase_spectrum, label=f'Xi = {Xi:.2f}')
plt.title('Espectro de Fase Φ(w) para diferentes Xi')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi(\omega)$ (radianes)')
#plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
