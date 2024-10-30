#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 18:40:26 2024

@author: deivit
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_synthetic_seismogram(param_name, param_values, 
                               ALNGTH=1.0, C=1.0, NMODE=2000, 
                               XSRC=0.2, XRCVR=0.7, TDURAT=1.25, 
                               NTSTEP=500, TAU=0.02):
    """
    Función para calcular y graficar el sismograma sintético variando un solo parámetro.

    Parámetros:
    - param_name: nombre del parámetro a variar (str)
    - param_values: lista de 3 valores para el parámetro a variar (list)
    - ALNGTH: longitud de la cuerda (float)
    - C: velocidad de la onda (float)
    - NMODE: número de modos (int)
    - XSRC: posición de la fuente (float)
    - XRCVR: posición del receptor (float)
    - TDURAT: duración del sismograma (float)
    - NTSTEP: número de pasos de tiempo (int)
    - TAU: término de forma de la fuente (float)
    """

    plt.figure(figsize=(12, 8))

    for value in param_values:
        # Cambiar el parámetro según el nombre
        if param_name == 'ALNGTH':
            ALNGTH = value
        elif param_name == 'C':
            C = value
        elif param_name == 'XSRC':
            XSRC = value
        elif param_name == 'XRCVR':
            XRCVR = value
        elif param_name == 'TDURAT':
            TDURAT = value
        
        # Calcular el paso de tiempo
        DT = TDURAT / NTSTEP
        # Inicializar el desplazamiento
        U = np.zeros(NTSTEP)

        # Loop externo sobre modos
        for N in range(1, NMODE + 1):
            ANPIAL = N * np.pi / ALNGTH
            SXS = np.sin(ANPIAL * XSRC)
            SXR = np.sin(ANPIAL * XRCVR)
            WN = N * np.pi * C / ALNGTH
            DMP = (TAU * WN) ** 2
            SCALE = np.exp(-DMP / 4.0)
            SPACE = SXS * SXR * SCALE

            # Loop interno sobre pasos de tiempo
            for J in range(NTSTEP):
                T = DT * J
                CWT = np.cos(WN * T)
                U[J] += CWT * SPACE

        # Gráfica del desplazamiento U(t)
        time = np.linspace(0, TDURAT, NTSTEP)
        plt.plot(time, U, label=f'{param_name} = {value}')

    # Configuraciones de la gráfica
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Desplazamiento')
    plt.title(f'Sismograma Sintético Variando {param_name}')
    plt.xlim(0, TDURAT)
    plt.ylim(np.min(U), np.max(U))
    plt.grid(True)
    plt.legend()
    plt.show()

# Llamar a la función con los parámetros deseados
# Variar longitud de la cuerda
plot_synthetic_seismogram('ALNGTH', [0.5, 1.0, 1.5])

# Variar velocidad de la onda
plot_synthetic_seismogram('C', [0.5, 1.0, 1.5])

# Variar posición de la fuente
plot_synthetic_seismogram('XSRC', [0.1, 0.2, 0.3])

# Variar posición del receptor
plot_synthetic_seismogram('XRCVR', [0.5, 0.7, 0.9])

# Variar duración del sismograma
plot_synthetic_seismogram('TDURAT', [1.0, 1.25, 1.5])

# Variar término de forma de la fuente
plot_synthetic_seismogram('TAU', [0.01, 0.02, 0.05])
