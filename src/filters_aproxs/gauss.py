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

        N,self.fc = self.Gaussord(self.fo*(2*pi),self.tol,self.retGroup, 24) #fije un N maximo para q no explote

        if self.N == 0:
            self.N = N
        elif self.N > 24:  # de nuevo el n q invente
            self.N = 24

        self.b, self.a = self.gauss_tf(self.N,self.fc)
        self.b = 10 ** (self.Go / 20) * self.b

        print(self.b, self.a)

    def Gaussord(self,wo,tol,retGroup,N):
        woN = wo * retGroup * 1e-6
        tolN = tol / 100
        it=0
        for it in range(1,N+1):
            bn,an = self.gauss_tf(it,woN)
            w, h = signal.freqs(bn, an, worN=np.logspace(-1, np.log10(woN) + 1, num=2000))
            retGroup_f = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)  # el retardo de grupo es la derivada de la fase respecto de w
            minPos = self.minPos(w, woN)
            if retGroup_f[minPos] >= (1 - tolN):
                  break
        return it, 1 / (retGroup * 1e-6)


    def nextTerm(self,tol,k):
        #newTerm= [(self.tol**(k+1)/math.factorial(k+1))]
        newTerm = np.zeros(2*(k+1))
        newTerm= [(tol**(k+1)/math.factorial(k+1))]  #Normalizado

        for it in range(0,2*(1+k)):
            newTerm.append(0)
        return np.poly1d(newTerm)

    def minPos(self,w,woN):
        new_w = []
        for it in w:
            new_w.append(abs(it-woN))#busco el valor q mas se parezca a woN
        return new_w.index(min(new_w))#devuelvo la posicion del elemento q cumpla esa condicion



    # -----------------------------------------------------------------------------
    def gauss_tf(self, N, Wn, btype='low', output='ba'):
        Wn = np.asarray(Wn)
        # MODULO CUADRADO DE LA FUNCION TRANSFERENCIA
        gain = 1
        poly = np.poly1d(1)
        for n in np.arange(1, N + 1):
            base = np.zeros(n + 1)
            base[0] = 1 / np.factorial(n)
            new_poly = np.poly1d(base)
            poly = np.polyadd(poly, new_poly)

        den = np.polyval(poly, np.poly1d([1, 0, 0]))

        poles = []
        for pole in 1j * den.roots:
            if pole.real < 0:
                new_pole = complex(pole.real if abs(pole.real) > 1e-10 else 0,
                                   pole.imag if abs(pole.imag) > 1e-10 else 0)
                gain *= abs(new_pole)
                poles.append(new_pole)
        warped = Wn
        z, p, k = ([], poles, gain)
        # Transformo mi LP filter al resto
        if btype in ('lowpass', 'highpass'):
            if np.size(Wn) != 1:
                raise ValueError('Must specify a single critical frequency Wn for lowpass or highpass filter')

            if btype == 'lowpass':
                z, p, k = signal.lp2lp_zpk(z, p, k, wo=warped)
            elif btype == 'highpass':
                z, p, k = signal.lp2hp_zpk(z, p, k, wo=warped)
        elif btype in ('bandpass', 'bandstop'):
            try:
                bw = warped[1] - warped[0]
                wo = np.sqrt(warped[0] * warped[1])
            except IndexError:
                raise ValueError('Wn must specify start and stop frequencies for bandpass or bandstop filter')

            if btype == 'bandpass':
                z, p, k = signal.lp2bp_zpk(z, p, k, wo=wo, bw=bw)
            elif btype == 'bandstop':
                z, p, k = signal.lp2bs_zpk(z, p, k, wo=wo, bw=bw)
        else:
            raise NotImplementedError("'%s' not implemented in iirfilter." % btype)

        # print("input",[], poles, gain)
        # print(btype,z, p ,k)

        if output == 'zpk':
            return z, p, k
        elif output == 'ba':
            return signal.zpk2tf(z, p, k)
        elif output == 'sos':
            return signal.zpk2sos(z, p, k)