"""
------------ APROXIMACIÓN DE BESSEL ------------
Te hace de todito (LP,HP,BP,BR) con las condiciones
de diseño clásicas (fp,fa,Ap,Aa) prorizando el orden
preestablecido.
Devuelve:
    -
    -
"""
#import scipy.signal as ss
from scipy.signal import buttord, bessel
from scipy import signal
from src.lib.handy import save_filter, num2unit
from numpy import pi
import numpy as np

class Bessel(object):

    def __init__(self):
        super(Bessel, self).__init__()
        self.b, self.a = None, None

    #-------------------------------------------------
    def get_params(self, data):
        print(data)
        self.N = data['N']
        self.fpp = data['fpp']
        self.fpm = data['fpm']
        self.fap = data['fap']
        self.fam = data['fam']
        self.Ap = data['Ap']
        self.Aa = data['Aa']
        self.Go = data['Go']
        self.E = data['E']
        self.Q = data['Q']
        self.tol = data['tol']
        self.retGroup = data['retGroup']
        self.fo = data['fo']

    def GD(self, data):
        self.get_params(data)

        N, fc = self.bessord(self.fo*(2*pi),self.tol,self.retGroup, 24) #fije un N maximo para q no explote
        if self.N == 0:
            self.N = N
        elif self.N > 24:#de nuevo el n q invente
            self.N = 20

        self.b,self.a = signal.bessel(self.N, fc, 'low', True, 'ba', norm='delay')
        self.b = 10**(self.Go/20)*self.b

        print(self.b, self.a)



    def bessord(self, fo,tol,retGroup,N):
        #normalizamos
        woN = fo*retGroup*1e-6

        n=0
        for i in range(0,N):
            n+=1
            bn,an = signal.bessel(n,1,'low',analog=True,output='ba',norm='delay')
            w,h = signal.freqs(bn,an,worN=np.logspace(-1, np.log10(woN)+1, num=1000))
            g_delay = -np.diff(np.unwrap(np.angle(h)))/np.diff(w)
            minPos = self.minPos(w,woN)
            if g_delay[minPos] >= (1-tol/100):
                break
        return n, 1/(retGroup*1e-6)

    def minPos(self,w,woN):
        new_w = []
        for it in w:
            new_w.append(abs(it-woN))
        return new_w.index(min(new_w))







    # # -------------------------------------------------
    # def calc_NQE(self, N, fc, ft):
    #     if self.N == 0:
    #         self.N = N
    #     if self.E == 'auto':
    #         if self.Q == 'auto':
    #             self.fc = fc
    #         else:
    #             self.E = (max(1 / (2 * self.Q), self.calc_Emin(ft)) + self.calc_Emax()) / 2
    #             self.fc = self.fpp / (self.E ** (self.N))
    #     else:
    #         if self.Q == 'auto':
    #             Emin = self.calc_Emin(ft)
    #         else:
    #             Emin = max(1 / (2 * self.Q), self.calc_Emin(ft))
    #         self.E = self.calc_Emax() - self.E * (self.calc_Emax() - Emin) / 100
    #         self.fc = self.fpp / (self.E ** (self.N))
    #
    # def calc_Emin(self, ft):
    #     frec_norm = {
    #         'LP': self.fap / self.fpp,
    #         'HP': self.fpp / self.fap,
    #         'BP': (self.fap - self.fam) / (self.fpp - self.fpm),
    #         'BR': (self.fpp - self.fpm) / (self.fap - self.fam)
    #     }
    #     return np.sqrt(10 ** (self.Aa / 10) - 1) / (frec_norm[ft] ** self.N)
    #
    # def calc_Emax(self):
    #     return np.sqrt(10 ** (self.Ap / 10) - 1)
    #
    # # ------------------------------------------------
    # def LP(self, data):
    #     self.get_params(data)
    #
    #     N, fc = buttord(self.fpp * (2 * pi), self.fap * (2 * pi),
    #                     self.Ap, self.Aa, analog=True)
    #     self.calc_NQE(N, fc, 'LP')
    #
    #     print("fc:" + str(self.fc) + ",N:" + str(self.N))
    #     self.b, self.a = bessel(self.N, self.fc * (2 * pi), btype='low', analog=True, output='ba')
    #     self.b = 10 ** (self.Go / 20) * self.b
    #     # self.z, self.p, self.k = sos2zpk(self.sos)
    #     print(self.b, self.a)
    #
    # # ------------------------------------------------
    # def HP(self, data):
    #     self.get_params(data)
    #     N, fc = buttord(self.fpp * (2 * pi), self.fap * (2 * pi),
    #                     self.Ap, self.Aa, analog=True)
    #     self.calc_NQE(N, fc, 'HP')
    #
    #     print("fc:" + str(self.fc) + ",N:" + str(self.N))
    #     self.b, self.a = bessel(self.N, self.fc * (2 * pi), btype='highpass', analog=True, output='ba')
    #     self.b = 10 ** (self.Go / 20) * self.b
    #     # self.z, self.p, self.k = sos2zpk(self.sos)
    #     print(self.b, self.a)
    #
    # # ------------------------------------------------
    # def BP(self, data):
    #     self.get_params(data)
    #     N, fc = buttord([self.fpm * (2 * pi), self.fpp * (2 * pi)],
    #                     [self.fam * (2 * pi), self.fap * (2 * pi)],
    #                     self.Ap, self.Aa, analog=True)
    #     self.calc_NQE(N, fc, 'BP')
    #
    #     self.b, self.a = bessel(self.N, [self.fam * (2 * pi), self.fpp * (2 * pi)], btype='bandpass', analog=True)
    #     self.b = 10 ** (self.Go / 20) * self.b
    #     # self.z, self.p, self.k = sos2zpk(self.sos)
    #     print(self.b, self.a)
    #
    # # ------------------------------------------------
    # def BR(self, data):
    #     self.get_params(data)
    #     N, fc = buttord([self.fpm * (2 * pi), self.fpp * (2 * pi)],
    #                     [self.fam * (2 * pi), self.fap * (2 * pi)],
    #                     self.Ap, self.Aa, analog=True)
    #     self.calc_NQE(N, fc, 'BR')
    #
    #     self.b, self.a = bessel(self.N, [self.fam * (2 * pi), self.fpp * (2 * pi)], btype='bandstop', analog=True)
    #     self.b = 10 ** (self.Go / 20) * self.b
    #     # self.z, self.p, self.k = sos2zpk(self.sos)
    #     print(self.b, self.a)
#------------------------------------------------------
if __name__ == '__main__':
    pass
    #calculo que deberia hacer algo
