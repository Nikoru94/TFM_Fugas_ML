# -*- coding: utf-8 -*-
"""
@author: Yanes Pérez, Nicolás
@version: v0.0
---------------------------------------------------------------------------------------
Class Events
---------------------------------------------------------------------------------------
"""

from inspect import Attribute
import numpy as np


class event(object):
    
    # INICIALIZADOR
    def __init__(self, attr):
        self._params = attr

    def get_prob_dist_type(self):
        return self._params['Prob Distr']

    def get_prob_dist_params(self):
        return self._params

    def get_prob_dist(self):
        params = self.get_prob_dist_params()
        pd_type = self.get_prob_dist_type()
        
        if pd_type == 'Uniform':
            l = np.arange(
                params['Min'],
                params['Max'] + params['Step'], 
                params['Step'])
            return np.random.choice(l, size=1)[0]
        
        elif pd_type == 'Binomial':
            return np.random.binomial(params['n'],params['q'])

        elif pd_type == 'exp':
            return np.random.exponential(params['h'])

        else:
            pass
            

class time_event(event):
    # INICIALIZADOR
    def __init__(self, attr):
        super().__init__(attr) 


class vol_event(event):
    # INICIALIZADOR
    def __init__(self, attr):
        super().__init__(attr)         




