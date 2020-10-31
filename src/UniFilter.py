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
from src.lib.handy import test_N, chkLP, chkHP, chkBP, chkBR
import numpy as np
import scipy.signal as ss

class FilterMaker(object):

    def __init__(self):
        super(FilterMaker,self).__init__()
        self.Filtro = None
        self.err_msg = ""
    def make_filter(self,data):
        success = False
        filtros = {
            'Butterworth': Butter()
            , 'Chebyshev 1': Cheby1()
            , 'Chebyshev 2': Cheby2()
            , 'Bessel': Bessel()
            # ,'Legendre': #Not yet implemented
            # ,'Gauss':    #Not yet implemented
            , 'Cauer': Cauer()
        }
        if data['aprox'] not in filtros.keys():
           self.err_msg = 'ERROR: UniFilter - Aproximación errónea'
        elif data['ft'] == "Tipo de Filtro":
            self.err_msg = 'ERROR: UniFilter - No se selecciono un Tipo de Filtro' + data['ft']
        elif not test_N(data):
            self.err_msg = 'ERROR: UniFilter - Orden mal cargado'
        else:
            success = True
            self.Filtro = filtros[data['aprox']]
            if data['ft'] == 'LP':
                if chkLP(data):
                    self.Filtro.LP(data)
            elif data['ft'] == 'HP':
                if chkHP(data):
                    self.Filtro.HP(data)
            elif data['ft'] == 'BP':
                if chkBP(data):
                    self.Filtro.BP(data)
            elif data['ft'] == 'BR':
                if chkBR(data):
                    self.Filtro.BR(data)

        return success

    def handlePlot(self,axes,canvas): #Este seria el caso de LP
        self.w = np.logspace(np.log10(self.Filtro.fpp / 10), np.log10(self.Filtro.fap * 10), num=10000) * 2 * np.pi
        bode = ss.bode(ss.TransferFunction(self.Filtro.b, self.Filtro.a), w=self.w)
        axes.plot(bode[0] / (2 * np.pi), bode[1])
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()
        axes.grid(which='both')
        canvas.draw()
        """self.w, self.h = ss.freqs(self.Filtro.b, self.Filtro.a)
        obj.axes_mag.semilogx(self.w, 20 * np.log10(abs(self.h)))
        obj.axes_mag.margins(0, 0.1)
        obj.axes_mag.set_xlabel('Frequency [radians / second]')
        obj.axes_mag.set_ylabel('Amplitude [dB]')
        obj.axes_mag.grid(which='both', axis='both')
        #obj.axes_mag.legend()
        obj.canvas_mag.draw()"""
#-----------------------------------------------------
if __name__ == '__main__':
    pass

