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
from scipy.signal import buttord, butter, sos2zpk
from numpy import pi
#from src.lib.handy import save_filter, num2unit
class Butter(object):

    def __init__(self):
        super(Butter,self).__init__()
        self.b, self.a = None, None
        self.sos = None
        self.zpk = None
        print("Butter Created")
    #-------------------------------------------------
    def get_params(self, data):
        print(data)
        self.N   = data['N']
        self.fpp = data['fpp']
        self.fpm = data['fpm']
        self.fap = data['fap']
        self.fam = data['fam']
        self.Ap  = data['Ap']
        self.Aa = data['Aa']
        self.Go = data['Go']
        self.fc = self.calc_crit(data)
    # -------------------------------------------------
    def calc_crit(self,data):
        if data['E'] == 0:
            data['E'] = 0.01 #Reemplazar por el val MIN
        if data['E'] != 'auto': #buttord debe calcular fc
            return 1/(data['E']**(self.N))
        elif data['N'] != 0: #setearon el orden con E auto
            return (10**(self.Ap/10)-1)**0.5 #implementar desnorm
        else:
            return None
    #-------------------------------------------------
    def save(self, new):
        print(new)
        self.sos = new
        self.z, self.p, self.k = sos2zpk(new)
    # ------------------------------------------------
    def LP(self,data):
        self.get_params(data)
        if self.N == 0: #Nmin
            self.N, fc = buttord(self.fpp*(2*pi),self.fap*(2*pi),
                                 self.Ap,self.Aa, analog = True)
            if self.fc is None: self.fc = fc/(2*pi)
        print("fc:"+str(self.fc)+",N:"+str(self.N))
        self.b, self.a = butter(self.N, self.fc*(2*pi), btype='low', analog = True,output='ba')
        self.b = 10 ** (self.Go / 20) * self.b
        #self.z, self.p, self.k = sos2zpk(self.sos)
        print(self.b, self.a)
    # ------------------------------------------------
    def HP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord(self.fpp*(2*pi), self.fap*(2*pi),
                                 self.Ap, self.Aa,analog = True)
            if self.fc is None: self.fc = fc/(2*pi)
        print("fc:"+str(self.fc)+",N:"+str(self.N))
        self.b, self.a = butter(self.N, self.fc*(2*pi), btype='highpass', analog=True, output='ba')
        self.b = 10**(self.Go/20)*self.b
        # self.z, self.p, self.k = sos2zpk(self.sos)
        print(self.b, self.a)
    # ------------------------------------------------
    def BP(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord([self.fpm*(2*pi),self.fpp*(2*pi)],
                                      [self.fam*(2*pi),self.fap*(2*pi)],
                                      self.Ap, self.Aa)
            if self.fc is None: self.fc = fc/(2*pi)

        #self.b, self.a = butter(self.N, self.fc*(2*pi), btype='bandpass', analog=True)
        self.b, self.a = butter(self.N, [self.fam*(2*pi),self.fpp*(2*pi)], btype='bandpass', analog=True)
        self.b = 10 ** (self.Go / 20) * self.b
        # self.z, self.p, self.k = sos2zpk(self.sos)
        print(self.b, self.a)
    # ------------------------------------------------
    def BR(self,data):
        self.get_params(data)
        if self.N == 0:
            self.N, fc = buttord([self.fpm*(2*pi),self.fpp*(2*pi)],
                                      [self.fam*(2*pi),self.fap*(2*pi)],
                                      self.Ap, self.Aa)
            if self.fc is None: self.fc = fc/(2*pi)
        self.b, self.a = butter(self.N, [self.fam*(2*pi),self.fpp*(2*pi)], btype='bandstop', analog=True)
        self.b = 10 ** (self.Go / 20) * self.b
        # self.z, self.p, self.k = sos2zpk(self.sos)
        print(self.b, self.a)
# ----------------------------------------------------
if __name__ == '__main__':
    prueba = Butter()
    data = {'N':2,'fpp':20,'fpm':0,'fam':0,'fap':50,'Ap':0.175,'Aa':60,'E':'auto'}
    prueba.HP(data)
    print(prueba.sos)
    print(prueba.z,prueba.p,prueba.k)
    pass
    #Calculo que debería hacer algo...