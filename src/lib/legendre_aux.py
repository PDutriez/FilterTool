"""
-------- ECUACIONES AUXILIARES PARA LEGENDRE --------
Tiene dos funciones:
 - 	legord(wp, wa, Ap, Aa) con la misma funcionalidad
    que 'Buttord'.
 -	legendre(N, fc, btype, output) con la misma fun-
    cionalidad que 'butter'.
"""
from numpy import *
from scipy import special, signal


def ln(N):
    if N == 0:
        return [0]
    if N % 2:  # N impar
        k = (N - 1) // 2
        a0 = 1 / (sqrt(2) * (k + 1))

        poly = poly1d([a0])
        for i in range(1, k + 1):
            ai = a0 * (2 * i + 1)
            new_poly = ai * special.legendre(i)
            poly = polyadd(poly, new_poly)
        poly = polymul(poly, poly)  # Potencia
        poly = polyint(poly)  # Integro
        b = poly1d([2, 0, -1])  # Borde superior
        a = poly1d([-1])  # Borde inferior

    else:  # N par
        k = (N - 2) // 2
        if k % 2:  # k impar
            b0 = 1 / sqrt((k + 1) * (k + 2))
            poly = poly1d(0)

            for i in range(1, k + 1):
                if i % 2:  # i impar
                    bi = b0 * (2 * i + 1)
                    new_poly = bi * special.legendre(i)
                    poly = polyadd(poly, new_poly)
        else:  # k par
            b0 = 1 / sqrt((k + 1) * (k + 2))
            poly = poly1d(b0)

            for i in range(1, k + 1):
                if not i % 2:  # i par
                    bi = b0 * (2 * i + 1)
                    new_poly = bi * special.legendre(i)
                    poly = polyadd(poly, new_poly)

        poly = polymul(poly, poly)  # Potencia
        poly = polymul(poly, poly1d([1, 1]))  # Multiplico por lo de afuera
        poly = polyint(poly)  # Integro
        b = poly1d([2, 0, -1])  # Borde superior
        a = poly1d([-1])  # Borde inferior

    return polysub(polyval(poly, b), polyval(poly, a))


def legendre(N, E, btype, output):
    myln = (E**2)*ln(N)
    gain = 1
    den = polyadd(poly1d([1]), myln)
    print(den, den.roots)
    poles = []
    for pole in 1j * den.roots:
        if pole.real < 0:
            new_pole = complex(pole.real if abs(pole.real) > 1e-10 else 0,
                                pole.imag if abs(pole.imag) > 1e-10 else 0)
            gain *= abs(new_pole)
            poles.append(new_pole)

    if btype == 'low' or btype == 'lowpass':
        z, p, k = signal.lp2lp_zpk([], poles, gain)
    elif btype == 'highpass':
        z, p, k = signal.lp2hp_zpk([], poles, gain)
    elif btype == 'bandpass':
        z, p, k = signal.lp2bp_zpk([], poles, gain)
    elif btype == 'bandstop':
        z, p, k = signal.lp2bs_zpk([], poles, gain)

    print("input",[], poles, gain)
    print(btype,z, p ,k)

    formats = {'zpk':(z, p, k),
               'ba':signal.zpk2tf(z, p, k),
               'sos':signal.zpk2sos(z, p, k)}
    if output in formats.keys():
        return formats[output]
    else:
        return 0

def legord(wp, ws, gpass, gstop, analog=False):
    """
    El Orden minimo se cumple cuando:
    Ln(wa^2)>=log((10**(gstop/10) - 1)/E**2)
    :param wp: 
    :param ws: 
    :param gpass: 
    :param gstop: 
    :param analog: 
    :return: 
    """
    E = sqrt(10**(gpass/10)-1) #E max

    wp = atleast_1d(wp)
    ws = atleast_1d(ws)

    filter_type = 2 * (len(wp) - 1)
    filter_type += 1
    if wp[0] >= ws[0]:
        filter_type += 1

    # Pre-warp frequencies for digital filter design
    if not analog:
        passb = tan(pi * wp / 2.0)
        stopb = tan(pi * ws / 2.0)
    else:
        passb = wp * 1.0
        stopb = ws * 1.0

    if filter_type == 1:            # low
        nat = stopb / passb
    elif filter_type == 2:          # high
        nat = passb / stopb
    elif filter_type == 3:          # stop
        nat = ((stopb * (passb[0] - passb[1])) /
               (stopb ** 2 - passb[0] * passb[1]))
    elif filter_type == 4:          # pass
        nat = ((stopb ** 2 - passb[0] * passb[1]) /
               (stopb * (passb[0] - passb[1])))

    nat = min(abs(nat))
    #print(f'Wan={nat}, E={E}, max={log10((10 ** (gstop / 10) - 1) / E ** 2)}')
    for i in range(1,21): # más de 20 sino se rompe
        Ln = ln(i)
        #print(f'l_{i}({nat**2})={polyval(Ln, nat**2)}\n')
        if polyval(Ln, nat**2) >= log10((10**(gstop/10) - 1)/E**2):
            order = i
            W0 = (10 ** (0.1 * abs(gpass)) - 1.0) ** (-1.0 / (2.0 * order))
            break
    if filter_type == 1:  # low
        WN = W0 * passb
    elif filter_type == 2:  # high
        WN = passb / W0
    elif filter_type == 3:  # stop
        WN = zeros(2, float)
        discr = sqrt((passb[1] - passb[0]) ** 2 +
                     4 * W0 ** 2 * passb[0] * passb[1])
        WN[0] = ((passb[1] - passb[0]) + discr) / (2 * W0)
        WN[1] = ((passb[1] - passb[0]) - discr) / (2 * W0)
        WN = sort(abs(WN))
    elif filter_type == 4:  # pass
        W0 = array([-W0, W0], float)
        WN = (-W0 * (passb[1] - passb[0]) / 2.0 +
              sqrt(W0 ** 2 / 4.0 * (passb[1] - passb[0]) ** 2 +
                   passb[0] * passb[1]))
        WN = sort(abs(WN))

    if not analog:
        wn = (2.0 / pi) * arctan(WN)
    else:
        wn = WN

    if len(wn) == 1:
        wn = wn[0]

    return order, wn, E

def validate_gpass_gstop(gpass, gstop):

    if gpass <= 0.0:
        raise ValueError("gpass should be larger than 0.0")
    elif gstop <= 0.0:
        raise ValueError("gstop should be larger than 0.0")
    elif gpass > gstop:
        raise ValueError("gpass should be smaller than gstop")

