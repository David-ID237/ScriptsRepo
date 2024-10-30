import numpy as np
import matplotlib.pyplot as plt

# Definición de parámetros
rho1 = 2800  # kg/m^3, densidad medio 1
rho2 = 3300  # kg/m^3, densidad medio 2
beta1 = 3900  # m/s, velocidad de ondas SH en medio 1
beta2 = 4600  # m/s, velocidad de ondas SH en medio 2

# Rango de ángulos de incidencia (0 a 89 grados)
j1d = np.linspace(0, 89, 100)  # hasta 89 para evitar sin(theta2) > 1
j1r = np.radians(j1d)

# Cálculo de ángulos de transmisión usando la Ley de Snell
sin_j2 = (beta2 / beta1) * np.sin(j1r)
# Evitar valores fuera del rango [-1, 1] para arcsin
sin_j2 = np.clip(sin_j2, -1, 1)
j2 = np.arcsin(sin_j2)

# Cálculo de cosenos
cos_j1 = np.cos(j1r)
cos_j2 = np.cos(j2)

# Coeficientes de transmisión y reflexión para ondas SH
T12 = (2 * rho1 * beta1 * cos_j1) / (rho1 * beta1 * cos_j1 + rho2 * beta2 * cos_j2)
R12 = (rho1 * beta1 * cos_j1 - rho2 * beta2 * cos_j2) \
    / (rho1 * beta1 * cos_j1 + rho2 * beta2 * cos_j2)

# Gráfica para ondas SH
plt.figure(figsize=(12, 6))
plt.plot(j1d, R12, label='Coeficiente de Reflexión R12', color='red')
plt.plot(j1d, T12, label='Coeficiente de Transmisión T12', color='blue')
plt.title('Coeficientes de Reflexión y Transmisión para Ondas SH')
plt.xlabel('Ángulo de Incidencia (°)')
plt.ylabel('Coeficientes')
plt.xlim(0, 90)
plt.ylim(-0.5, 2.1)
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(90, color='black', lw=0.5, ls='--')
plt.legend()
plt.grid()
plt.show()
