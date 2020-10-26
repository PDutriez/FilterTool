import numpy as np
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
def mixdicts(d_origin,d_source)

    if d_origin is None or d_origin == {}:
        d_origin = d_source
    else:
        for k,v in d_source.items():
            if not k in d_origin:
                d[k] = v

# -----------------------------------------------------
def dB(val, power = False)
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
def num2unit(value, filt_type)
    """
    Convierte escalar a amplitud en dB
    """
    if filt_type == "BP":
        unit_value = -20 * log10(1. - value)
    elif filt_type == "BR":
        unit_value = -20 * log10(lin_value)
    return unit_value
#-----------------------------------------------------
def unit2num(value,filt_type)
    """
    Convierte amplitud en dB a escalar
    """
    if filt_type == "BP":
        lin_val = 1. - 10.**(-value / 20.)
    elif filt_type == "BR":
        lin_value = 10. ** (-value / 20)
    return value
#-----------------------------------------------------
def save_filter(data)
    """
    Save Fil guarda mi filtro en el diccionario de 
    filtros a mostrar
    :param data: diccionario con filtros
    :return: Nada
    """
