import sys
from src.ui.stages import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from src import UniFilter as UF
from src.lib import handy as hand
from src.lib.stagescontrol import stageControl
import numpy as np
import scipy.signal as ss

class AppStages(QtWidgets.QWidget):

    def __init__(self, parent=None):  # instanciamos la clase
        super(AppStages, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.GraphsWidget.setCurrentIndex(0)
        self.sos = []

        #MY STUFF
        self.createBodePlotsCanvas()
        self.stages_list = []

        #EVENT HANDLER
        self.ui.chk_all_selected.toggled.connect(self.draw_cascade)
        self.ui.GraphsWidget.currentChanged.connect(self.manage_plot)

    def receive_stages(self,b,a):
        self.sos = np.array(ss.tf2sos(b,a,pairing='keep_odd'))
        for it in range(0,len(self.sos)):
            self.stages_list.append(False)
            tempObject = stageControl(self, self.stages_list,it)
            tempItem = QtWidgets.QListWidgetItem()
            tempItem.setSizeHint(tempObject.sizeHint())
            self.ui.FilterList.addItem(tempItem)
            self.ui.FilterList.setItemWidget(tempItem, tempObject)

        self.manage_plot() #Ploteamos las etapas
        #self.sos.append([])  #Agregamos una extra para la acumulada, esta horrible, perdon
        #self.stages_list.append(False)

    def draw_cascade(self):
        if self.ui.chk_all_selected.isChecked(): #Graficame PLS
            if any(self.stages_list) == True:
                A = np.poly1d(1)
                B = np.poly1d(1)
                for i in range(0,len(self.stages_list)):
                    if self.stages_list[i]:
                        temp_list = []
                        temp_list.append(self.fix(self.sos[i]))
                        b, a = ss.sos2tf(temp_list)
                        b = np.poly1d(b)
                        a = np.poly1d(a)
                        B = np.polymul(B,b)
                        A = np.polymul(A,a)
                # self.sos=np.insert(self.sos[0],0,ss.tf2sos(B.c, A.c))
                # for t in range(0,len(self.stages_list)):
                #     self.stages_list[t] = False
                # self.stages_list[len(self.stages_list)-1] = True
                w = np.logspace(np.log10(1), np.log10(self.furthestPZ() * 100 / (2 * np.pi)), num=10000) * 2 * np.pi
                bode = ss.bode(ss.TransferFunction(B.c, A.c), w=w)
                self.axes_mag.plot(bode[0] / (2 * np.pi), bode[1], label='acumulada')
                self.axes_mag.set_xscale('log')
                self.axes_mag.set_xlabel('Frequency [Hz]');
                self.axes_mag.set_ylabel('Magnitude [dB]')
                self.axes_mag.minorticks_on()
                self.axes_mag.legend(loc='best')
                self.canvas_mag.draw()
        else:
                self.manage_plot()

    def manage_plot(self):
        w = self.ui.GraphsWidget.currentWidget() #Wipe it
        tabs = {self.ui.MagTab: (self.axes_mag, self.canvas_mag, self.magplot),
                self.ui.PazTab: (self.axes_paz, self.canvas_paz, self.pazPlot),
                self.ui.AtenTab: (self.axes_ate, self.canvas_ate, self.atePlot),
                self.ui.FaseTab: (self.axes_fas, self.canvas_fas, self.fasPlot),
                self.ui.RetGrupTab: (self.axes_rdg, self.canvas_rdg, self.rdgPlot),
                self.ui.RespImpTab: (self.axes_imp, self.canvas_imp, self.impPlot),
                self.ui.RespEscTab: (self.axes_esc, self.canvas_esc, self.escPlot)}
        if w in tabs.keys():
            axes, canvas, plotter = tabs[w]
            axes.clear()
        if len(self.sos):
            axes.grid(which='both')
            plotter(axes, canvas)
        else:    canvas.draw()

    def fix(self,sos):
        if sos[2]==0 and sos[1]==0:
            sos = np.delete(sos,2)
            sos = np.insert(sos,0,0)
            sos = np.delete(sos, 2)
            sos = np.insert(sos, 0, 0)
        elif sos[2]==0:
            sos = np.delete(sos, 2)
            sos = np.insert(sos, 0, 0)
        return sos

    def magplot(self, axes, canvas):
        w = np.logspace(np.log10(1), np.log10(self.furthestPZ() * 100/(2*np.pi)), num=10000) * 2 * np.pi
        for i in range(0,len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.fix(self.sos[i]))
                b, a = ss.sos2tf(temp_list)
                bode = ss.bode(ss.TransferFunction(b, a), w=w)
                axes.plot(bode[0] / (2 * np.pi), bode[1], label=str(i))
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()
        axes.legend(loc='best')
        canvas.draw()

    def atePlot(self, axes, canvas):
        w = np.logspace(np.log10(1), np.log10(self.furthestPZ() * 1000/(2*np.pi)), num=10000) * 2 * np.pi
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                bode = ss.bode(ss.TransferFunction(a, b), w=w)
                axes.plot(bode[0] / (2 * np.pi), bode[1],label=str(i))
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()
        axes.legend(loc='best')
        canvas.draw()

    def pazPlot(self, axes, canvas):
        #theta = np.linspace(-np.pi, np.pi, 201)
        #axes.plot(np.sin(theta), np.cos(theta), color='gray', linewidth=0.2)
        #plt.annotate("ωo", pol2cart(1, np.pi / 4))
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                poles = np.roots(a)
                zeros = np.roots(b)
                axes.plot(np.real(poles), np.imag(poles), 'Xb', label='Poles' + str(i))
                axes.plot(np.real(zeros), np.imag(zeros), 'or', label='Zeros' + str(i))
        axes.axhline(y=0, color='gray', linewidth=1)
        axes.axvline(x=0, color='gray', linewidth=1)
        d = self.furthestPZ()
        axes.set_xlim(-d*1.1,d*1.1)
        axes.set_ylim(-d*1.1,d*1.1)
        axes.set_xlabel("Real")
        axes.set_ylabel("Imaginary")
        axes.legend(loc='best')
        canvas.draw()

    def fasPlot(self, axes, canvas):
        w = np.logspace(np.log10(1), np.log10(self.furthestPZ() * 10 /(2*np.pi)), num=10000) * 2 * np.pi
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                bode = ss.bode(ss.TransferFunction(b, a), w=w)
                axes.plot(bode[0] / (2 * np.pi), bode[2], label=str(i))
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Phase [º]')
        axes.minorticks_on()
        axes.legend(loc='best')
        canvas.draw()

    def rdgPlot(self, axes, canvas):
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                w, gd = ss.group_delay((b, a))
                axes.plot(w/(2 * np.pi), gd, label=str(i))
        axes.set_xscale('log')
        axes.set_ylabel('Group delay [samples]')
        axes.set_xlabel('Frequency [Hz]')
        axes.minorticks_on()
        axes.legend(loc='best')
        canvas.draw()

    def impPlot(self, axes, canvas):
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                H = ss.lti(b, a)
                time, resp = H.impulse()
                axes.plot(time, resp, label=str(i))
        axes.set_xlabel('time')
        axes.set_ylabel('Amplitude')
        axes.legend(loc='best')
        canvas.draw()
    def escPlot(self, axes, canvas):
        for i in range(0, len(self.stages_list)):
            if self.stages_list[i]:
                temp_list = []
                temp_list.append(self.sos[i])
                b, a = ss.sos2tf(temp_list)
                H = ss.lti(b, a)
                time, resp = H.step()
                axes.plot(time, resp, label=str(i))
        axes.set_xlabel('time')
        axes.set_ylabel('Amplitude')
        axes.legend(loc='best')
        canvas.draw()

    def furthestPZ(self):
        dist = []
        for i in range(0, len(self.stages_list)):

            temp_list = []
            temp_list.append(self.sos[i])
            b, a = ss.sos2tf(temp_list)

            poles = np.roots(a)
            zeros = np.roots(b)

            if len(poles):
                if len(zeros):
                    dist.append(max(max(abs(poles)), max(abs(zeros))))
                else:
                    dist.append(max(abs(poles)))
            elif len(zeros):
                dist.append(max(abs(zeros)))
        return max(dist)


    def createBodePlotsCanvas(self):
        # creo una figura por pestaña
        self.figure_mag = Figure()
        self.figure_ate = Figure()
        self.figure_paz = Figure()
        self.figure_fas = Figure()
        self.figure_rdg = Figure()
        self.figure_imp = Figure()
        self.figure_esc = Figure()
        # le creo un canvas a la figura
        self.canvas_mag = FigureCanvas(self.figure_mag)
        self.canvas_ate = FigureCanvas(self.figure_ate)
        self.canvas_paz = FigureCanvas(self.figure_paz)
        self.canvas_fas = FigureCanvas(self.figure_fas)
        self.canvas_rdg = FigureCanvas(self.figure_rdg)
        self.canvas_imp = FigureCanvas(self.figure_imp)
        self.canvas_esc = FigureCanvas(self.figure_esc)
        # necesito algo donde poner el canvas
        plot_layout_mag = QtWidgets.QVBoxLayout()
        plot_layout_ate = QtWidgets.QVBoxLayout()
        plot_layout_paz = QtWidgets.QVBoxLayout()
        plot_layout_fas = QtWidgets.QVBoxLayout()
        plot_layout_rdg = QtWidgets.QVBoxLayout()
        plot_layout_imp = QtWidgets.QVBoxLayout()
        plot_layout_esc = QtWidgets.QVBoxLayout()
        # toolbar es la barra sobre el canvas, un verdadero amigo
        plot_layout_mag.addWidget(NavigationToolbar(self.canvas_mag, self))
        plot_layout_mag.addWidget(self.canvas_mag)
        plot_layout_ate.addWidget(NavigationToolbar(self.canvas_ate, self))
        plot_layout_ate.addWidget(self.canvas_ate)
        plot_layout_paz.addWidget(NavigationToolbar(self.canvas_paz, self))
        plot_layout_paz.addWidget(self.canvas_paz)
        plot_layout_fas.addWidget(NavigationToolbar(self.canvas_fas, self))
        plot_layout_fas.addWidget(self.canvas_fas)
        plot_layout_rdg.addWidget(NavigationToolbar(self.canvas_rdg, self))
        plot_layout_rdg.addWidget(self.canvas_rdg)
        plot_layout_imp.addWidget(NavigationToolbar(self.canvas_imp, self))
        plot_layout_imp.addWidget(self.canvas_imp)
        plot_layout_esc.addWidget(NavigationToolbar(self.canvas_esc, self))
        plot_layout_esc.addWidget(self.canvas_esc)
        # tengo todos unidos, ahora lo agrego a cada pesaña
        self.ui.MagTab.setLayout(plot_layout_mag)
        self.ui.PazTab.setLayout(plot_layout_paz)
        self.ui.AtenTab.setLayout(plot_layout_ate)
        self.ui.FaseTab.setLayout(plot_layout_fas)
        self.ui.RetGrupTab.setLayout(plot_layout_rdg)
        self.ui.RespImpTab.setLayout(plot_layout_imp)
        self.ui.RespEscTab.setLayout(plot_layout_esc)
        # agregame el plot que sino nada tine sentido
        self.axes_mag = self.figure_mag.add_subplot()
        self.axes_paz = self.figure_paz.add_subplot()
        self.axes_ate = self.figure_ate.add_subplot()
        self.axes_imp = self.figure_imp.add_subplot()
        self.axes_esc = self.figure_esc.add_subplot()
        self.axes_rdg = self.figure_rdg.add_subplot()
        self.axes_fas = self.figure_fas.add_subplot()