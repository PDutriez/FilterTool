import matplotlib.pyplot as plt
from skimage import io
import numpy as np
from src.filters_aproxs import butter_aprox as bt
import scipy.signal as signal


class newFilter:
    def __init__(self,new_filter_data, parent=None):
        self.data = new_filter_data
        if self.data['ft'] == 'Butterworth': #ojo q aprox tiene cargado el tipo de filtro y ft la aproximacion a usar
            print("nace un butterworth!")
            self.filter_object = bt.Butter(self.data)
            print(self.filter_object)



    def handlePlot(self,obj):
        print(self.data)

        self.w, self.h = signal.freqs(self.filter_object.b, self.filter_object.a, np.logspace(1, 8, 500))
        obj.axes_mag.semilogx(self.w, 20 * np.log10(abs(self.h)))
        obj.axes_mag.margins(0, 0.1)
        obj.axes_mag.grid(which='both', axis='both')
        obj.axes_mag.axvline(100, color='green')  # cutoff frequency
        obj.canvas_mag.draw()