"""
------------ APROXIMACIÓN DE GAUSS ------------
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
from numpy import *
from math import factorial
class Gauss(object):

    def __init__(self):
        super(Gauss, self).__init__()
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

        N, self.fc = self._bessord(self.fo*(2*pi),self.tol,self.retGroup, 20) #fije un n_max
        print(N)
        if self.N == 0:
            self.N = N
        elif self.N > 20:#de nuevo el n_max q invente
            self.N = 20
        print(N)

        self.b,self.a = signal.bessel(N, self.fc, 'low', True, 'ba', norm='delay')
        self.b = 10**(self.Go/20)*self.b

        print(self.b, self.a)
    #-----------------------------------------------------------------------------
    def _gaussord(self, wrg, tol, tau_0, max_order):
        wrgn = wrg*tau_0*1e-6
        n = 0
        while True:  # do{}while() statement python style
            n = n+1
            z_n, p_n, k_n = signal.bessel(n, 1, 'low', analog=True, output='zpk', norm='delay')
            w, h = signal.freqs_zpk(z_n, p_n, k_n, worN=np.logspace(-1, np.log10(wrgn)+1, num=2000))
            g_delay = -np.diff(np.unwrap(np.angle(h)))/np.diff(w)
            w_prima = [abs(j-wrgn) for j in w]
            i = w_prima.index(min(w_prima))  # Busco el wrgn (en su defecto el mas cercano)
            if i<len(g_delay):
                if g_delay[i] >= (1-tol/100) or n is max_order:
                    break
            else:
                break
        return n, 1/(tau_0*1e-6)
    #-----------------------------------------------------------------------------
    def gauss_tf(self,N,Wn, btype='low',output='ba'):
        Wn = asarray(Wn)
        #MODULO CUADRADO DE LA FUNCION TRANSFERENCIA
        gain = 1
        poly = poly1d(1)
        for n in arange(1, N + 1):
            base = zeros(n + 1)
            base[0] = 1 / factorial(n)
            new_poly = poly1d(base)
            poly = polyadd(poly, new_poly)

        den = polyval(poly, poly1d([1, 0, 0]))

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
            if size(Wn) != 1:
                raise ValueError('Must specify a single critical frequency Wn for lowpass or highpass filter')

            if btype == 'lowpass':
                z, p, k = signal.lp2lp_zpk(z, p, k, wo=warped)
            elif btype == 'highpass':
                z, p, k = signal.lp2hp_zpk(z, p, k, wo=warped)
        elif btype in ('bandpass', 'bandstop'):
            try:
                bw = warped[1] - warped[0]
                wo = sqrt(warped[0] * warped[1])
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



