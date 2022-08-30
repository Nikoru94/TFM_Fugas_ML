# -*- coding: utf-8 -*-
"""
@author: Yanes Pérez, Nicolás
@version: v0.0
---------------------------------------------------------------------------------------
CLASE CONTROLADOR
Clase donde se define el modo de control del tanque


---------------------------------------------------------------------------------------
"""

# TODO. Añadir ruido a las medidas de los tanques
# TODO (futuro). Si queremos asegurar que arrancamos con los litros definidos en el JSON en 
# los que no arrancan a cero. Habria que mejorar este método.

from tank import *

### CLASE CONTROLADOR

class controller(object):

    ## INICIALIZADOR
    def __init__(self, t_cycle):
        
        self._time_cycle = t_cycle
        self._active_tanks = []
        self._passive_tanks = []
        
        self._start_bt = False
        self._stop_bt = False
        self._emergency_bt = False
        self._auto_dial = False
        self._man_dial = True

        self._user_inputs = None
        
        self._mode = None
        
        self._a_overflow = False
        self._reset_signal = False
        
        self._status = 'INITIAL CONDITION'

    ## FUNCIÓN PRINT
    def __str__(self):
        msg = """\
            CONTROLLER 
                |time cycle (s): {}
                |active tanks ({}):\n""".format(
                    self.get_time_cycle(),
                    len(self.get_active_tanks()))

        for t in self.get_active_tanks():
            msg += """\
                    |{}\n""".format(t.get_name())

        msg +="""\
                |passive tanks ({}):\n""".format(len(self.get_passive_tanks()))

        for t in self.get_passive_tanks():
            msg += """\
                    |{}\n""".format(t.get_name())

        return textwrap.dedent(msg)
    
    ## FUNCIONES DE LOS TIEMPOS 

    def get_time_cycle(self):
        return self._time_cycle
    
    def set_time_cycle(self, t_cycle):
        self._time_cycle = t_cycle
        
    ## FUNCIONES GET / SET DEPÓSITOS
    def get_active_tanks(self):
        return self._active_tanks

    def add_active_tanks(self, new_tank):
        self._active_tanks.append(new_tank)
    
    def get_passive_tanks(self):
        return self._passive_tanks

    def add_passive_tanks(self, new_tank):
        self._passive_tanks.append(new_tank)


    ## FUNCION SET / GET DE LOS EVENTO DE USUARIO EN LA CONTROLADORA

    def get_user_inputs(self):
        return self._user_inputs

    def set_user_inputs(self, user_inputs):
        self._user_inputs = user_inputs
    
    
    ## FUNCIONES DE BOTONES

    def push_start_bt(self):
        self._start_bt = True

    def unpush_start_bt(self):
        self._start_bt = False

    def push_stop_bt(self):
        self._stop_bt = True

    def unpush_stop_bt(self):
        self._stop_bt = False

    def push_emergency_bt(self):
        self._emergency_bt = True
        
    def unpush_emergency_bt(self):
        self._emergency_bt = False

    def set_auto_dial(self):
        self._auto_dial = True
        self._man_dial = False
        self.set_auto_st()

    def set_man_dial(self):
        self._auto_dial = False
        self._man_dial = True
        self.set_man_st()

    def get_start_bt(self):
        return self._start_bt

    def get_stop_bt(self):
        return self._stop_bt

    def get_emergency_bt(self):
        return self._emergency_bt

    def get_dial(self):
        if self._man_dial:
            return 'MANUAL'
        else:
            return 'AUTOMATIC'

    ##  FUNC. SET DEL ESTADO DEL CONTROLADOR

    def set_emergency_st(self):
        self._status = 'EMERGENCY'

    def set_normal_operation_st(self):
        self._status = 'NORMAL OPERATION'

    def set_stop_st(self):
        self._status = 'STOP'
    
    def set_initial_cond_st(self):
        self._status = 'INITIAL CONDITION'
    
    def set_auto_st(self):
        self._mode = 'AUTOMATIC'
        
    def set_man_st(self):
        self._mode = 'MANUAL'

    def get_status(self):
        return self._status
        
        
    ## FUNC. COMPROBACIÓN DEL ESTADO DEL CONTROLADOR
    
    def is_emergency_st(self):
        return self.get_status() == 'EMERGENCY'

    def is_stop_st(self):
        return self.get_status() == 'STOP'
    
    def is_normal_op_st(self):
        return self.get_status() == 'NORMAL OPERATION'
    
    def is_initial_cond_st(self):
        return self.get_status() == 'INITIAL CONDITION'
    
    def is_auto_st(self):
        return self._mode == 'AUTOMATIC'
    
    def is_manual_st(self):
        return self._mode == 'MANUAL'
    
    
    #TODO. UN TANQUE SI ESTA LLENO QUE ES EL TANQUE QUE ALMACENA EL LÍQUIDO
    #TODO. Todos los que comienzan a cero abren su valvula de salida y los que no comienza a cero
    # cierran su valvula. Para detectar que hemos alcanzado las cond. ini. comprobar que todos los 
    # depositos que comienza a cero están en cero.

    ## FUNC. ACTUACIÓN DE LOS DEPÓSITOS
    
    # TODO. un tanque si podria tener liquido que seria el de retorno tener eso en cuenta
    def is_empty_all_tanks(self):    
        tank_list = self.get_active_tanks() + self.get_passive_tanks()
        empty = True        

        for tnk in tank_list:
            empty = empty and (tnk.is_empty())
        return empty

    def close_all_valves(self):
        for tk in self.get_active_tanks():
            tk.close_input_valves()
            tk.close_output_valves()
    
    def update_active_tanks(self, tsimulation, start_begin):
        emerg_st = False
        for tnk in self.get_active_tanks():
            emerg_st = emerg_st | (tnk.update_status(tsimulation, start_begin))
        return emerg_st




    ## FUNC. ACTUALIZACIÓN DEL CONTROLADOR
    
    def update_controller(self,tsimulation):
        
        # ESTABLECIMIENTO DEL ESTADO DE EMERGENCIA
        if self.get_emergency_bt():
            self.set_emergency_st()
    
        # ESTABLECIMIENTO DEL ESTADO DE OP. NORMAL
        elif (self.get_start_bt() and self.is_stop_st()):
            self.set_normal_operation_st()
            
        
        # ACCIÓN EN ESTADO DE PARADA
        if self.is_stop_st() :
            self.close_all_valves()
            

        # ACCIÓN EN ESTADO DE OPERACIÓN NORMAL  
        if self.is_normal_op_st():
            print("CONTROLADOR - OPERACIÓN NORMAL\n")

            if self.get_stop_bt():
                self.set_stop_st()
                self.close_all_valves()

            emerg_st = self.update_active_tanks(tsimulation, start_begin = False)
            if emerg_st:
                self.set_emergency_st()

        # ACCIÓN EN ESTADO DE EMERGENCIA
        elif self.is_emergency_st():
            print("CONTROLADOR - EMERGENCIA\n")
            self.update_active_tanks(start_begin = False)

            if (not (self.get_emergency_bt()) and (self.get_start_bt())):
                self.set_initial_cond_st()
            
        # ACCIÓN EN ESTADO DE CONDICIONES INICIALES
        elif self.is_initial_cond_st():
            print("CONTROLADOR - COND. INICIALES\n")
            
            
            if (self.is_empty_all_tanks() and self.is_manual_st()):
                self.update_active_tanks(tsimulation, start_begin = True)
                self.set_normal_operation_st()

            elif (self.is_auto_st() and self.get_start_bt()):
                self.update_active_tanks(tsimulation, start_begin = True)
                self.set_normal_operation_st()
            
            else:
                self.update_active_tanks(tsimulation, start_begin = False)
            

                

    # FUNC. ACTUALIZACIÓN DE ENTRADAS POR PARTE DEL USUARIO

    def apply_user_inputs(self, tsimulation):

        for input_element in self.get_user_inputs():
            
            input = input_element["Name"]
            
            list_times = [event['Time'] for event in input_element['Events']]
            list_values = [event['Value'] for event in input_element['Events']]
            time = [i for i in list_times if i <= tsimulation]
            
            # en caso que no haya eventos en el presente input dado el tiempo de simulación
            if time == []: 
                continue

            time = max(time)
            value = list_values[list_times.index(time)]


            if input == "start_bt": 
                if value == "ON":
                    self.push_start_bt()
                else:
                    self.unpush_start_bt()
            
            elif input == "stop_bt":
                if value == "ON":
                    self.push_stop_bt()
                else:
                    self.unpush_stop_bt()
            
            elif input == "emergency_bt":
                if value == "ON":
                    self.push_emergency_bt()
                else:
                    self.unpush_stop_bt()

            elif input == "dial":
                if value == "AUTO":
                    self.set_auto_dial()
                else:
                    self.set_man_dial()

            
            
            
        
            

            
                
                
        
                
            
                
                
    
        
          
        
        