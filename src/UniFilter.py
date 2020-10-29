"""
----------------------- UNIVERSAL FILTER -----------------------
Es una clase pensada para poder manejar todos los filtros diseñados
y que de manera abstracta maneje cada filtro como cualquier otro.
"""
from src.filters_aproxs.butter import Butter
from src.filters_aproxs.cheby1 import Cheby1
from src.filters_aproxs.cheby2 import Cheby2
from src.filters_aproxs.bessel import Bessel
from src.filters_aproxs.cauer import Cauer
#from src.filters_aproxs.gauss import Butter
#from src.filters_aproxs.legendre import Butter

class UniFilter(object):

    def __init__(self):
        super(UniFilter,self).__init__()
        self.Filtro = None

    def make_filter(self,data):
        filtros = {
            'Butterworth': Butter
            , 'Chebyshev 1': Cheby1
            , 'Chebyshev 2': Cheby2
            , 'Bessel': Bessel
            # ,'Legendre': #Not yet implemented
            # ,'Gauss':    #Not yet implemented
            , 'Cauer': Cauer
        }
        if data['aprox'] not in filtros.keys():
            print('ERROR: UniFilter - Aproximación errónea')
        elif data['ft'] != "Tipo de Filtro":
            print('ERROR: UniFilter - No se selecciono un Tipo de Filtro')
        elif not filtros[data['aprox']].test_N(data):
            print('ERROR: UniFilter - Orden mal cargado')
        else:
            self.Filtro = filtros[data['aprox']]
            if data['ft'] == 'LP':
                self.Filtro.LP(data)
            elif data['ft'] == 'HP':
                self.Filtro.HP(data)
            elif data['ft'] == 'BP':
                self.Filtro.BP(data)
            elif data['ft'] == 'BR':
                self.Filtro.BR(data)

# ------------------------------------------------------------
if __name__ == '__main__':
    pass

