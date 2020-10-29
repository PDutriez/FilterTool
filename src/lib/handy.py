import numpy as np
from numpy import pi, log10
import scipy.signal as ss

__all__ = ['qstr2str','change2unit','save_filter']

def qstr2str(text):
    """
    Convierte texto (QVariant, QString) u obj
    numerico en string
    :param text: QVariant, QString para convertir
    :return: string convertido
    """
    text_type = str(type(text)).lower()
    if "qstring" in text_type:
        string = text.toUtf8()
    elif "qvariant" in text_type:
        string = text.toString()
    elif "unicode" in text_type:
        return text
    else: string = str(text)

    return str(string)
# -----------------------------------------------------
def mixdicts(d_origin,d_source):

    if d_origin is None or d_origin == {}:
        d_origin = d_source
    else:
        for k,v in d_source.items():
            if not k in d_origin:
                d[k] = v

# -----------------------------------------------------
def dB(val, power = False):
    """
    Calcula dB de 'val'
    :param val: valor a calcular
    :param power: square or not
    :return: dB de 'val'
    """
    if power:
        return 10. * np.log10(val)
    else:
        return 20 * np.log10(val)
# -----------------------------------------------------
def num2unit(value, filt_type):
    """
    Convierte escalar a amplitud en dB
    """
    if filt_type == "BP":
        unit_value = -20 * log10(1. - value)
    elif filt_type == "BR":
        unit_value = -20 * log10(lin_value)
    return unit_value
#-----------------------------------------------------
def unit2num(value,filt_type):
    """
    Convierte amplitud en dB a escalar
    """
    if filt_type == "BP":
        lin_val = 1. - 10.**(-value / 20.)
    elif filt_type == "BR":
        lin_value = 10. ** (-value / 20)
    return value
#-----------------------------------------------------
def save_filter(data,new,new_format, convert=True):
    """
    Save Filter guarda mi filtro en el diccionario de
    filtros
    :param data: diccionario con filtros
    :return: Nada
    """
    if new_format == 'sos':
        data['sos'] = new
    elif new_format == 'zpk':
       data['zpk'] = [new[0],new[1],new[2]]
    elif new_format == 'ba':
        b = new[0]
        a = new[1]
        D = len(b)-len(a)
        if D > 0: # a > b llename de ceros a
            a = np.append(a, np.zeros(D))
        elif D < 0: # b > a llename de ceros b
            b = np.append(b, np.zeros(-D))

        #data['N'] = len(b) - 1 #Orden filtro
        data['ba'] = [np.array(b, dtype=np.complex),
                      np.array(a, dtype=np.complex)]
    if convert:
        convert_filter(data,new_format)
#-----------------------------------------------------
#def convert_filter(data,new_format):

#-----------------------------------------------------
def test_N(data):
    """
    Te avisa si el orden es demasiado alto para ser
    un filtro razonable
    """
    ok_N = False
    if data['N'] < 25:
        ok_N = True
    else:
        print("N muy alto")
    return ok_N
#-----------------------------------------------------
def resp(a=1,b=1,N=0,step = False):
    """
    Calcula la respuesta impulsiva y al escalon
    :param a: Numerador
    :param b: Denominador
    :param N: Numero de puntos a calcular    
    :return: 
    """
    if N==0: N=100
    H = ss.lti(a,b)
    if step == True:
        time, resp = H.step(N=N)
    else:
        time, resp = H.impulse(N=N)

    return time, resp
#-----------------------------------------------------
def gropu_delay(a=1,b=1,nfft=512,whole=False):
    w, gd = ss.group_delay((a, b), w=nfft, whole=whole)
    return w, gd
#-----------------------------------------------------

#-----------------------------------------------------
if __name__=='__main__':
    pass

#    pass