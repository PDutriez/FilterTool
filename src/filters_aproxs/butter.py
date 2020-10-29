"""
------------ APROXIMACIÓN DE BUTTERWORTH ------------
Te hace de todito (LP,HP,BP,BR) con las condiciones
de diseño clásicas (fp,fa,Ap,Aa) prorizando el orden
preestablecido.
Devuelve:
    -
    -
"""
#import scipy.signal as ss
from scipy.signal import buttord, butter
from src.lib.handy import save_filter, num2unit
class Butter(object):

    def __init__(self):
        super(Butter,self).__init__()
    #-------------------------------------------------
    def get_params(self, data):
        self.N   = data['N']
        self.fpp = data['fpp']
        self.fpm = data['fpm']
        self.fap = data['fap']
        self.fam = data['fam']
        self.Ap  = data['Ap']
        self.Aa = data['Aa']
        self.fc = self.calc_crit(data)
        self.format  = 'sos'
    # -------------------------------------------------
    def calc_crit(self,data):
        if data['E'] != 'auto':
            return 1/(data['E']**(self.N))
        else:
            return None
    #-------------------------------------------------
    def save(self, data, new):
        save_filter(data, new)

    # ------------------------------------------------
    def LP(self,data):
        self.get_params(data)
        if self.N == 0: #Nmin
            self.N, fc = buttord(self.fpp,self.fap,
                                      self.Ap,self.Aa)
            if self.fc is None: self.fc = fc

        self.save(data,butter(self.N,self.fc,btype='lowpass',
                                 output=self.format))
    # ------------------------------------------------
    def HP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord(self.fpp, self.fap,
                                      self.Ap, self.Aa)
            if self.fc is None: self.fc = fc
        self.save(data, butter(self.N, self.fc, btype='highpass',
                                  output=self.format))
    # ------------------------------------------------
    def BP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord([self.fpp,self.fpm],
                                      [self.fap,self.fam],
                                      self.Ap, self.Aa)
            if self.fc is None: self.fc = fc
        self.save(data, butter(self.N, self.fc, btype='bandpass',
                                  output=self.format))
    # ------------------------------------------------
    def BR(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord([self.fpp,self.fpm],
                                      [self.fap,self.fam],
                                      self.Ap, self.Aa)
            if self.fc is None: self.fc = fc
        self.save(data, butter(self.N, self.fc, btype='bandstop',
                                  output=self.format))
# ----------------------------------------------------
if __name__ == '__main__':
    pass
    #Calculo que debería hacer algo...