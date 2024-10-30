import numpy as np
import matplotlib.pyplot as plt

# Parámetros
Alpha = 6.8  # Velocidad de la onda P en km/s
Beta = 4.0   # Velocidad de la onda SV en km/s

# Definimos el rango de ángulos incidentes en grados
theta_incidente = np.linspace(0, 90, 500)  # Ángulos de 0 a 90 grados

# Convertimos ángulos de grados a radianes
theta_rad = np.radians(theta_incidente)

# Parámetro de rayo
p = np.sin(theta_rad) / Alpha

# Lentitudes verticales
eta_alpha = np.sqrt(1 / Alpha**2 - p**2)
eta_beta = np.sqrt(1 / Beta**2 - p**2)

# Coeficientes de reflexión RP y RSV
RP = (4 * p**2 * eta_alpha * eta_beta - (eta_beta**2 - p**2)**2) / \
     (4 * p**2 * eta_alpha * eta_beta + (eta_beta**2 - p**2)**2)

RSV = (4 * p * eta_alpha * (p**2 - eta_beta**2)) / \
      (4 * p**2 * eta_alpha * eta_beta + (eta_beta**2 - p**2)**2)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(theta_incidente, RP, label='Reflexión P', color='b', lw=2)
plt.plot(theta_incidente, RSV, label='Reflexión SV', color='r', lw=2)

plt.title('Coeficientes de Reflexión en función del Ángulo de Incidencia Para Ondas P-SV')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Coeficiente de Reflexión')
plt.axhline(0, color='gray', lw=0.5)
plt.legend(loc='best')
plt.grid(True)
plt.show()
