"""
------------ APROXIMACIÓN DE GAUSS ------------
Te hace de todito con las condiciones
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
import math
import time

class Gauss(object):

    def __init__(self):
        super(Gauss, self).__init__()
        self.b, self.a = None, None
        self.fc =None

    # -------------------------------------------------
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

        N,fc = self.Gaussord(self.fo*(2*pi),self.tol,self.retGroup, 24) #fije un N maximo para q no explote

        if self.N == 0:
            self.N = N
        elif self.N > 24:  # de nuevo el n q invente
            self.N = 24

        self.b, self.a = self.Gauss(self.N,fc)
        self.b = 10 ** (self.Go / 20) * self.b

        print(self.b, self.a)

    def Gaussord(self,wo,tol,retGroup,N):
        woN = wo * retGroup * 1e-6
        tolN = tol / 100
        den = np.poly1d(1)
        n=0
        for it in range(0,N):
            n+=1
            an = den + self.nextTerm(1,it)
            w, h = signal.freqs([1], an.c, worN=np.logspace(-1, np.log10(woN) + 1, num=100000))
            retGroup_f = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)  # el retardo de grupo es la derivada de la fase respecto de w
            minPos = self.minPos(w, woN)
            if retGroup_f[minPos] >= (1-tolN):
                break
        return n,1/(retGroup*1e-6)


    def nextTerm(self,tol,k):
        #newTerm= [(self.tol**(k+1)/math.factorial(k+1))]
        newTerm= [(tol**(k+1)/math.factorial(k+1))]  #Normalizado

        for it in range(0,2*(1+k)):
            newTerm.append(0)
        return np.poly1d(newTerm)

    def minPos(self,w,woN):
        new_w = []
        for it in w:
            new_w.append(abs(it-woN))#busco el valor q mas se parezca a woN
        return new_w.index(min(new_w))#devuelvo la posicion del elemento q cumpla esa condicion

    def Gauss(self,N,tol):
        bn = np.poly1d(1)
        for it in range(0,N):
            bn += self.nextTerm(tol,it)
        # w, h = signal.freqs(bn.c, 1, worN=np.logspace(-1, np.log10(wo) + 1, num=100000))
        # retGroup_f = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
        return bn,1