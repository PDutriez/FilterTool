"""
------------ APROXIMACIÓN DE BUTTERWORTH ------------
Te hace de todito (LP,HP,BP,BR) con las condiciones
de diseño clásicas (fp,fa,Ap,Aa) prorizando el orden
preestablecido.
Devuelve:
    -
    -
"""
import scipy.signal as ss
from scipy.signal import buttord

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

    #-------------------------------------------------
    def test_n(self):
    """
    Te avisa si el orden es demasiado alto para ser
    un filtro razonable
    """
    #-------------------------------------------------
    def save(selfself, data):

# ----------------------------------------------------
if __name__ == '__main__':
    #Calculo que debería hacer algo...