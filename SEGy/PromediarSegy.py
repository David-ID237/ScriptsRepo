#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:16:48 2024

@author: deivit
"""
import obspy
import numpy as np

# Cargar archivos SEG-Y
segy_files = ["Dato1.sgy", "Daton.sgy"]  # Lista de archivos SEG-Y

# Leer todos los archivos SEG-Y como Streams de ObsPy
streams = [obspy.read(file) for file in segy_files]

# Asegurarse de que todos los archivos tengan el 
#mismo número de trazas y puntos de tiempo
num_traces = len(streams[0])
num_points = len(streams[0][0].data)

# Crear una matriz para almacenar los datos de cada disparo
data_sum = np.zeros((num_traces, num_points))

# Sumar los datos de cada disparo
for stream in streams:
    for i, trace in enumerate(stream):
        data_sum[i] += trace.data

# Promediar dividiendo por el número de disparos
data_promedio = data_sum / len(segy_files)

# Crear un nuevo Stream con las trazas promediadas
stream_promedio = obspy.Stream()
# Usamos las trazas del primer archivo para crear las nuevas
for i, trace in enumerate(streams[0]):  
    new_trace = trace.copy()  # Copiar la estructura de la traza original
    
    # Convertir los datos promediados a float32 para asegurar compatibilidad
    new_trace.data = data_promedio[i].astype(np.float32)
    
    # Establecer la codificación como IEEE_FLOAT_32 (código 5)
    new_trace.stats.segy = {"trace_header": obspy.io.segy.segy.SEGYTraceHeader()}
    new_trace.stats.segy.trace_header.data_encoding = 5  # IEEE_FLOAT_32
    
    # Agregar la nueva traza al stream promedio
    stream_promedio.append(new_trace)

# Guardar el archivo promedio como un archivo SEG-Y
stream_promedio.write("disparo_promedio3.sgy", format="SEGY")