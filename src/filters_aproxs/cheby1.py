"""
------------ APROXIMACIÓN DE CHEBYSHEV 1 ------------
Te hace de todito (LP,HP,BP,BR) con las condiciones
de diseño clásicas (fp,fa,Ap,Aa) prorizando el orden
preestablecido.
Devuelve:
    -
    -
"""
#import scipy.signal as ss
from scipy.signal import cheb1ord, cheby1
from src.lib.handy import save_filter, num2unit
class Cheby1(object):

    def __init__(self:
        super(Cheby1, self).__init__()

    #-------------------------------------------------
    def get_params(self,data):

        self.N   = data['N']
        self.fpp = data['fpp']
        self.fpm = data['fpm']
        self.fap = data['fap']
        self.fam = data['fam']
        self.Ap  = data['Ap']
        self.Aa = data['Aa']
        self.fc = None
        self.format  = 'sos'
    #-------------------------------------------------
    def test_N(self):
    """
    Te avisa si el orden es demasiado alto para ser
    un filtro razonable
    """
    #-------------------------------------------------
    def save(self, data, new):
    save_filter(data, new)

    #-------------------------------------------------
    def LP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, self.fc = cheb1ord(self.fpp,self.fap,
                                          self.Ap,self.Aa)
        self.save(data,cheby1(self.N,self.Ap,self.fc,
                                 btype='lowpass',output=self.format))
    #-------------------------------------------------
    def HP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, self.fc = cheb1ord(self.fpp, self.fap,
                                        self.Ap, self.Aa)
        self.save(data,cheby1(self.N, self.Ap, self.fc,
                              btype='highpass', output=self.format))
    #-------------------------------------------------
    def BP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, self.fc = cheb1ord([self.fpp,self.fpm],
                                       [self.fap,self.fam],
                                          self.Ap, self.Aa)
        self.save(data,cheby1(self.N,self.Ap,self.fc,btype='bandpass',
                              output=self.format))
    #-------------------------------------------------
    def BR(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, self.fc = cheb1ord([self.fpp, self.fpm],
                                       [self.fap, self.fam],
                                       self.Ap, self.Aa)
        self.save(data, cheby1(self.N, self.Ap, self.fc, btype='bandstop',
                                output=self.format))
#------------------------------------------------------
if __name__ == '__main__':
    pass
    #calculo que deberia hacer algo
