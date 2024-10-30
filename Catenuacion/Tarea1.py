# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
from scipy.optimize import curve_fit
import os

# Ruta de la carpeta que contiene los archivos CSV
ruta_archivos = '/home/deivit/Scripts/Python/Catenuacion/Datos/'

# Inicializar listas para almacenar envolventes y promedios de picos
envolventes_ax = []
envolventes_ay = []
envolventes_az = []
picos_ax = []
picos_ay = []
picos_az = []

# Leer y procesar los archivos
for n in range(1, 11):
    filename = os.path.join(ruta_archivos, f'Dato{n}.csv')
    data = pd.read_csv(filename)

    # Extraer componentes
    ax = data['ax (m/s^2)']
    ay = data['ay (m/s^2)']
    az = data['az (m/s^2)']

    # Calcular la envolvente usando la transformada de Hilbert
    envol_ax = np.abs(hilbert(ax))
    envol_ay = np.abs(hilbert(ay))
    envol_az = np.abs(hilbert(az))

    # Guardar las envolventes en las listas correspondientes
    envolventes_ax.append(envol_ax)
    envolventes_ay.append(envol_ay)
    envolventes_az.append(envol_az)

    # Calcular los máximos en las envolventes, excluyendo la muestra 5
    if n != 11:
        maximos_ax, _ = find_peaks(envol_ax)
        maximos_ay, _ = find_peaks(envol_ay)
        maximos_az, _ = find_peaks(envol_az)

        # Excluir los últimos 300 datos
        maximos_ax = maximos_ax[maximos_ax < len(envol_ax) - 300]
        maximos_ay = maximos_ay[maximos_ay < len(envol_ay) - 300]
        maximos_az = maximos_az[maximos_az < len(envol_az) - 300]

        # Obtener las amplitudes de los picos
        amplitudes_ax = envol_ax[maximos_ax]
        amplitudes_ay = envol_ay[maximos_ay]
        amplitudes_az = envol_az[maximos_az]

        # Crear listas de tuplas (posición, amplitud)
        picos_con_amplitudes_ax = list(zip(maximos_ax, amplitudes_ax))
        picos_con_amplitudes_ay = list(zip(maximos_ay, amplitudes_ay))
        picos_con_amplitudes_az = list(zip(maximos_az, amplitudes_az))

        # Seleccionar los 20 picos con mayor amplitud
        picos_con_amplitudes_ax = sorted(picos_con_amplitudes_ax, key=lambda x: x[1], reverse=True)[:20]
        picos_con_amplitudes_ay = sorted(picos_con_amplitudes_ay, key=lambda x: x[1], reverse=True)[:20]
        picos_con_amplitudes_az = sorted(picos_con_amplitudes_az, key=lambda x: x[1], reverse=True)[:20]

        # Ordenar los picos seleccionados por posición en la señal
        picos_con_amplitudes_ax = sorted(picos_con_amplitudes_ax, key=lambda x: x[0])
        picos_con_amplitudes_ay = sorted(picos_con_amplitudes_ay, key=lambda x: x[0])
        picos_con_amplitudes_az = sorted(picos_con_amplitudes_az, key=lambda x: x[0])

        # Extraer solo las amplitudes de los picos
        picos_ax.append([pico[1] for pico in picos_con_amplitudes_ax])
        picos_ay.append([pico[1] for pico in picos_con_amplitudes_ay])
        picos_az.append([pico[1] for pico in picos_con_amplitudes_az])

# Convertir listas a arrays para facilitar el cálculo de promedios
picos_ax = np.array(picos_ax)
picos_ay = np.array(picos_ay)
picos_az = np.array(picos_az)

print(picos_az)

# Calcular el promedio de los picos para cada posición (1º, 2º, ... 20º)
promedios_maximos_ax = np.mean(picos_ax, axis=0)
promedios_maximos_ay = np.mean(picos_ay, axis=0)
promedios_maximos_az = np.mean(picos_az, axis=0)

# Definir la función exponencial para el ajuste
def exponencial(x, A, B, C):
    return A * np.exp(-B * x) + C

# Distancias correspondientes (0.2, 0.4, ..., 4.0 metros)
distancias = np.arange(0.2, 4.2, 0.2)  # En metros

# Ajuste exponencial, asegurando B > 0
try:
    params_ax, _ = curve_fit(exponencial, distancias, promedios_maximos_ax, p0=[1, 0.01, 0], bounds=(0, [np.inf, np.inf, np.inf]))
    params_ay, _ = curve_fit(exponencial, distancias, promedios_maximos_ay, p0=[1, 0.01, 0], bounds=(0, [np.inf, np.inf, np.inf]))
    params_az, _ = curve_fit(exponencial, distancias, promedios_maximos_az, p0=[1, 0.01, 0], bounds=(0, [np.inf, np.inf, np.inf]))

    # Generar datos ajustados
    ajuste_ax = exponencial(distancias, *params_ax)
    ajuste_ay = exponencial(distancias, *params_ay)
    ajuste_az = exponencial(distancias, *params_az)

    # Graficar las envolventes de todos los archivos en gráficos separados
    plt.figure(figsize=(15, 20))

    # Gráfico de las envolventes de ax
    for i in range(10):
        plt.subplot(10, 3, i * 3 + 1)
        plt.plot(envolventes_ax[i], label=f'Envolvente de ax (Muestra {i + 1})', color='b')
        plt.title(f'Envolvente de ax (Muestra {i + 1})')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud (m/s²)')
        plt.grid()
        plt.legend()

    # Gráfico de las envolventes de ay
    for i in range(10):
        plt.subplot(10, 3, i * 3 + 2)
        plt.plot(envolventes_ay[i], label=f'Envolvente de ay (Muestra {i + 1})', color='g')
        plt.title(f'Envolvente de ay (Muestra {i + 1})')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud (m/s²)')
        plt.grid()
        plt.legend()

    # Gráfico de las envolventes de az
    for i in range(10):
        plt.subplot(10, 3, i * 3 + 3)
        plt.plot(envolventes_az[i], label=f'Envolvente de az (Muestra {i + 1})', color='r')
        plt.title(f'Envolvente de az (Muestra {i + 1})')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud (m/s²)')
        plt.grid()
        plt.legend()

    plt.tight_layout()
    plt.show()

    # Graficar las amplitudes promedio y el ajuste exponencial
    plt.figure(figsize=(10, 6))
    plt.plot(distancias, promedios_maximos_ax, label='ax', marker='o', color='b')
    plt.plot(distancias, ajuste_ax, label='Ajuste Exponencial (ax)', color='b', linestyle='--')
    plt.plot(distancias, promedios_maximos_ay, label='ay', marker='o', color='g')
    plt.plot(distancias, ajuste_ay, label='Ajuste Exponencial (ay)', color='g', linestyle='--')
    plt.plot(distancias, promedios_maximos_az, label='az', marker='o', color='r')
    plt.plot(distancias, ajuste_az, label='Ajuste Exponencial (az)', color='r', linestyle='--')

    # Configuración de la gráfica
    plt.title('Amplitudes promedio de las envolventes y ajuste exponencial respecto a la distancia')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Amplitud (m/s²)')
    plt.xticks(distancias)  # Para asegurarse de que las etiquetas se muestren en las posiciones correctas
    plt.grid()
    plt.legend()
    plt.show()

except RuntimeError as e:
    print(f"Error en el ajuste exponencial: {e}")

