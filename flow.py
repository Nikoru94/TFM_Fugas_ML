# -*- coding: utf-8 -*-
"""
@author: Yanes Pérez, Nicolás
@version: v0.0
---------------------------------------------------------------------------------------
CLASE CAUDAL
Clase que define los atributos del caudal

---------------------------------------------------------------------------------------
"""

import numpy as np

class flow(object):

    # INICIALIZADOR
    def __init__(self, attr, tank_obj, time_cycle):
        self._flow_type = attr['Flow type']
        self._flow_value = attr['Flow value']
        self._tank = tank_obj
        self._time_cycle = time_cycle
        
    
    # TIPOS DE CAUDAL
    def get_flow_type(self):
        return self._flow_type
    
    def set_flow_type(self, flow_type):
        self._flow_type = flow_type
        
    
    # VALOR DE CAUDAL 
    def get_flow_value(self):
        return self._flow_value
    
    def set_flow_value(self, flow_value):
        self._flow_value = flow_value

    def get_time_cycle(self):
        return self._time_cycle

    # DEVUELVE EL TANQUE ASOCIADO AL QUE LE EXTRAE EL VOLUMEN
    def get_tank(self):
        return self._tank

    def get_time_cycle(self):
        return self._time_cycle

        
    # DEVOLUCIÓN DEL VOLUMEN
    def get_vol(self):
        t_cycle = self.get_time_cycle()
        type = self.get_flow_type()
        value = self.get_flow_value()
        
        if type == "Const":
            return t_cycle*value

        elif type == "Var":
            vol = self.get_tank().get_vol()
            max_vol = self.get_tank().get_capacity()
            flow_calc = value*np.sqrt(vol/max_vol)
            return self.t_cycle*flow_calc 
            
        else:
            return 0
        


            