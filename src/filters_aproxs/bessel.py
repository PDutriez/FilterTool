"""
------------ APROXIMACIÓN DE BESSEL ------------
Te hace de todito  con las condiciones
de diseño clásicas prorizando el orden
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

        N, self.fc = self.bessord(self.fo*(2*pi),self.tol,self.retGroup, 24) #fije un N maximo para q no explote
        if self.N == 0:
            self.N = N
        elif self.N > 24:#de nuevo el n q invente
            self.N = 24

        self.b,self.a = signal.bessel(self.N, self.fc, 'low', True, 'ba', norm='delay')
        self.b = 10**(self.Go/20)*self.b

        print(self.b, self.a)



    def bessord(self, wo,tol,retGroup,N):
        #normalizamos
        woN = wo*retGroup*1e-6
        tolN = tol/100
        n=0
        for i in range(0,N):
            n+=1
            bn,an = signal.bessel(n,1,'low',analog=True,output='ba',norm='delay')
            w,h = signal.freqs(bn,an,worN=np.logspace(-1, np.log10(woN)+3, num=2000))
            retGroup_f = -np.diff(np.unwrap(np.angle(h)))/np.diff(w)   #el retardo de grupo es la derivada de la fase respecto de w
            minPos = self.minPos(w,woN)
            if retGroup_f[minPos] >= (1-tolN):
                break
        return n, 1/(retGroup*1e-6)

    def minPos(self,w,woN):
        new_w = []
        for it in w:
            new_w.append(abs(it-woN))#busco el valor q mas se parezca a woN
        return new_w.index(min(new_w))#devuelvo la posicion del elemento q cumpla esa condicion





#------------------------------------------------------
if __name__ == '__main__':
    pass
    #calculo que deberia hacer algo
