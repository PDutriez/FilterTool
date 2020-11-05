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
from src.filters_aproxs.legendre import Legendre
from collections.abc import Iterable

from src.lib.handy import test_N, chkLP, chkHP, chkBP, chkBR, chkGD
import numpy as np
import scipy.signal as ss


class FilterMaker(object):

    def __init__(self):
        super(FilterMaker, self).__init__()
        self.Filtro = None
        self.err_msg = ""
        self.msg = ""
        self.chk = True
        self.name = None
        self.color = ''
        # self.color = None

    def make_filter(self, data, index):
        success = False
        filtros = {
            'Butterworth': Butter()
            , 'Chebyshev 1': Cheby1()
            , 'Chebyshev 2': Cheby2()
            , 'Bessel': Bessel()
            , 'Legendre': Legendre()
            # ,'Gauss':    #Not yet implemented
            , 'Cauer': Cauer()
        }
        self.aprox = data['aprox']
        if data['aprox'] not in filtros.keys():
            self.err_msg = 'ERROR: UniFilter - Aproximación errónea'
        elif data['ft'] == "Tipo de Filtro":
            self.err_msg = 'ERROR: UniFilter - No se selecciono un Tipo de Filtro' + data['ft']
        elif not test_N(data):
            self.err_msg = 'ERROR: UniFilter - Orden mal cargado'
        elif data['Aa'] < data['Ap']:
            self.err_msg = 'ERROR: Aa must be greater than Ap'
        else:  # Llegamos bien
            self.Filtro = filtros[data['aprox']]
            self.msg = data['aprox'] + ' ' + 'created' + ',' + ' ' + data['ft']
            self.ft = data['ft']
            if data['ft'] == 'LP':
                if chkLP(data)[0]:
                    self.Filtro.LP(data)
                    success = True
                else:
                    self.err_msg = chkLP(data)[1]
                    return success
            elif data['ft'] == 'HP':
                if chkHP(data)[0]:
                    self.Filtro.HP(data)
                    success = True
                else:
                    self.err_msg = chkHP(data)[1]
                    return success
            elif data['ft'] == 'BP':
                if chkBP(data)[0]:
                    self.Filtro.BP(data)
                    success = True
                else:
                    self.err_msg = chkBP(data)[1]
                    return success
            elif data['ft'] == 'BR':
                if chkBR(data)[0]:
                    self.Filtro.BR(data)
                    success = True
                else:
                    self.err_msg = chkBR(data)[1]
                    return success
            elif data['ft'] == 'Group Delay':
                if chkGD(data)[0]:
                    self.Filtro.GD(data)
                    success = True
                else:
                    self.err_msg = chkGD(data)[1]
                    return success
            self.name = data['ft'] + data['aprox'] +'(ID:' + str(index)+ ', N:' + str(self.Filtro.N) + ')'  # Le pusimos un nombre
        return success

    def setVisible(self, bool):
        self.chk = bool

    def __eq__(self, doppelganger):
        my = self.Filtro
        other = doppelganger.Filtro
        if my.N == other.N and my.fpp == other.fpp and my.fpm == other.fpm:
            if my.fap == other.fap and my.fam == other.fam and my.Ap == other.Ap:
                if my.Aa == other.Aa:
                    if my.Go == other.Go:
                        if self.compare(my.fc,other.fc):
                            if self.ft == doppelganger.ft:
                                if self.aprox == doppelganger.aprox:
                                    if self.ft == 'Group Delay':
                                        if my.tol == doppelganger.Filtro.tol:
                                            if my.retGroup == doppelganger.Filtro.retGroup:
                                                if my.fo == doppelganger.Filtro.fo:
                                                    return True
                                    else:
                                        return True
        return False

    def compare(self,a,b):
        return str(a) == str(b)


    def __str__(self):
        return self.name

"""    def handlePlot(self,axes,canvas, plot):
        if plot == 'mag':
            self.magPlot(axes, canvas)
        elif plot == 'ate':
            self.atePlot(axes, canvas)
        elif plot == 'paz':
            self.pazPlot(axes,canvas)
        elif plot == 'fas':
            self.fasPlot(axes, canvas)
        elif plot == 'rdg':
            self.rdgPlot(axes, canvas)
        elif plot == 'imp':
            self.impPlot(axes, canvas)
        elif plot == 'esc':
            self.escPlot(axes, canvas)

    def atePlot(self, axes, canvas):

    def pazPlot(self, axes, canvas):

    def fasPlot(self, axes, canvas):

    def rdgPlot(self, axes, canvas):

    def impPlot(self, axes, canvas):

    def escPlot(self, axes, canvas):

    def magPlot(self, axes, canvas):#Este seria el caso de LP
        if self.ft == 'LP':
            self.w = np.logspace(np.log10(self.Filtro.fpp / 10), np.log10(self.Filtro.fap * 10), num=10000) * 2 * np.pi
        elif self.ft == 'HP':
            self.w = np.logspace(np.log10(self.Filtro.fap / 10), np.log10(self.Filtro.fpp * 10), num=10000) * 2 * np.pi
        elif self.ft == 'BP':
            self.w = np.logspace(np.log10(self.Filtro.fam / 10), np.log10(self.Filtro.fap * 10), num=10000) * 2 * np.pi
        elif self.ft == 'BR':
            self.w = np.logspace(np.log10(self.Filtro.fam / 10), np.log10(self.Filtro.fap * 10), num=10000) * 2 * np.pi

        #self.w = np.logspace(0,6,1000)
        bode = ss.bode(ss.TransferFunction(self.Filtro.b, self.Filtro.a), w=self.w)
        axes.plot(bode[0] / (2 * np.pi), bode[1])
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()

        canvas.draw()"""
# -----------------------------------------------------
if __name__ == '__main__':
    pass
