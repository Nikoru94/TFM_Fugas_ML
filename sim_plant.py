# -*- coding: utf-8 -*-
"""
@author: Yanes Pérez, Nicolás
@version: v0.0
---------------------------------------------------------------------------------------
SIMULACIÓN DE LA PLANTA

Por medio de la simulación y creando el control de la planta
---------------------------------------------------------------------------------------
"""

import json
import matplotlib
import subprocess

from tank import *
from plant import *

with open('tanks.json') as f:
  data_tanks = json.load(f)

with open('inputs_user.json') as f:
  data_inputs = json.load(f)

with open('simulation.json') as f:
  data_simulation = json.load(f)
  t_initial = data_simulation['log_initial']
  t_step = data_simulation['log_step']
  t_end = data_simulation['log_end']
  t_cycle = data_simulation['sim_step']


# MONTAMOS LA SIMULACION
plant_sim = plant(data_tanks, t_cycle)
plant_sim.simulation(time_end = t_end, user_inputs = data_inputs)

# ANALIZAMOS LOS DATOS
datos  = plant_sim.get_records()
df = plant_sim.get_results(t_end = t_end, t_step = t_step, t_initial = t_initial)

df.to_csv('datos_simulacion.csv')
subprocess.Popen(["open", 'datos_simulacion.csv'])

plant_sim.graph_volume_records()
print(df)



# TODO. Cambiar la obtención de resultados
# Incluir un paramtero flag en la controladora
# los tanques deberan comprobar un flag para su funcionamiento
# cuanbdo el flag este activo los pipes conectados al
# tanque de almacenamiento no pueden abrirse (tendrian que
# esperar a que cierre) 

# ventas y llenados son acumulados






