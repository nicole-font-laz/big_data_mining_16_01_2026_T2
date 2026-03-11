#!/usr/bin/env python3
"""
Generador de dataset sintético de ventas (traducción desde R).
Genera `ventas_2023.csv`, muestra estadísticas básicas, calcula la
correlación entre 'monto' y 'cantidad' y exporta gráficos simples.

Requisitos: pandas, numpy, matplotlib, seaborn (opcional).
"""

import sys

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    missing = str(e).split(" ")[-1]
    print("Falta una dependencia:", e)
    print("Instala dependencias con: pip install -r requirements.txt")
    sys.exit(1)

from datetime import datetime

RANDOM_SEED = 123
np.random.seed(RANDOM_SEED)

# Fechas para todo 2023
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
N = len(fechas)

# Generar monto con estacionalidad (similar a la fórmula R)
base = np.random.normal(loc=1000, scale=200, size=N)
season = 1 + 0.3 * np.sin(2 * np.pi * (np.arange(1, N+1)) / 365)
monto = np.round(base * season, 2)

productos = ["Laptop", "Smartphone", "Tablet", "Smartwatch"]
regiones = ["Norte", "Sur", "Este", "Oeste"]
metodos_pago = ["Crédito", "Débito", "Efectivo"]

producto = np.random.choice(productos, size=N, replace=True)
region = np.random.choice(regiones, size=N, replace=True)
tipo_pago = np.random.choice(metodos_pago, size=N, replace=True)
cantidad = np.random.randint(1, 11, size=N)

ventas = pd.DataFrame({
    'fecha': fechas,
    'monto': monto,
    'producto': producto,
    'region': region,
    'tipo_pago': tipo_pago,
    'cantidad': cantidad
})

# Añadir mes y día de la semana
ventas['mes'] = ventas['fecha'].dt.strftime('%m')
try:
    # Intentar nombre de día en español si la versión de pandas lo permite
    ventas['dia_semana'] = ventas['fecha'].dt.day_name(locale='es')
except Exception:
    ventas['dia_semana'] = ventas['fecha'].dt.day_name()

# Guardar CSV
csv_path = 'ventas_2023.csv'
ventas.to_csv(csv_path, index=False)
print(f"Archivo guardado: {csv_path} (filas={len(ventas)})")

# Estadísticas básicas
total_ventas = ventas['monto'].sum()
promedio_venta = ventas['monto'].mean()
max_venta = ventas['monto'].max()
min_venta = ventas['monto'].min()

print("\nResumen estadístico:")
print(f"Total ventas: {total_ventas:,.2f}")
print(f"Promedio venta: {promedio_venta:,.2f}")
print(f"Máx venta: {max_venta:,.2f}")
print(f"Mín venta: {min_venta:,.2f}")

# Correlación entre monto y cantidad
corr = ventas[['monto', 'cantidad']].corr()
print("\nMatriz de correlación (monto, cantidad):")
print(corr)

# Patrones mensuales
patrones_mensuales = ventas.groupby('mes', sort=False).agg(total_ventas=('monto', 'sum')).reset_index()
# Asegurar orden cronológico
patrones_mensuales['mes'] = patrones_mensuales['mes'].astype(int)
patrones_mensuales = patrones_mensuales.sort_values('mes')

# Plots (se guardan como archivos PNG)
plt.figure(figsize=(8,4))
plt.plot(patrones_mensuales['mes'], patrones_mensuales['total_ventas'], marker='o')
plt.title('Tendencia de Ventas Mensuales')
plt.xlabel('Mes')
plt.ylabel('Total de Ventas')
plt.grid(True)
plt.tight_layout()
plt.savefig('tendencia_mensual.png')
print("Gráfico guardado: tendencia_mensual.png")
plt.close()

# Gráfico de barras
plt.figure(figsize=(8,4))
sns.barplot(x=patrones_mensuales['mes'], y=patrones_mensuales['total_ventas'], color='skyblue')
plt.title('Ventas Totales por Mes')
plt.xlabel('Mes')
plt.ylabel('Total de Ventas')
plt.tight_layout()
plt.savefig('ventas_por_mes.png')
print("Gráfico guardado: ventas_por_mes.png")
plt.close()

print('\nProceso completado.')
