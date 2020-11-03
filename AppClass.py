import sys
from src.ui.filterwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from src import UniFilter as UF
from src.lib import handy as hand
from src.lib.PlotControl import plotControl
import numpy as np
import scipy.signal as ss
import graficador as filterFactory


class AppCLass(QtWidgets.QWidget):

    def __init__(self, parent=None):  # instanciamos la clase
        super(AppCLass, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.GraphsWidget.setCurrentIndex(0)
        # MY STUFF: cosas que necesito instanciar externas a Qt
        self.createBodePlotsCanvas()
        self.plotDict = {}
        self.filter_list = []
        if hand.read_data():
            self.recover(hand.read_data())

        # EVENT HANDLER: acciones a partir de la UI
        self.ui.CBFilters.currentIndexChanged.connect(self.change_ParamInputs)
        self.ui.ButtonCreateFilter.clicked.connect(self.CreateNew)
        self.ui.FilterList.itemClicked.connect(self.selected_filter)
        self.ui.GraphsWidget.currentChanged.connect(self.manage_plot)

    def change_ParamInputs(self):
        # la idea es que no muestre todas las fpp... y App... dependiendo del filtro
        filtro = self.ui.CBFilters.currentText()
        if filtro == 'LP':
            self.ui.Filter_Image.setPixmap(QtGui.QPixmap("src/Images/LP.png"))
            self.ui.Filter_Image.setScaledContents(True)
        elif filtro == 'HP':
            self.ui.Filter_Image.setPixmap(QtGui.QPixmap("src/Images/HP.png"))
            self.ui.Filter_Image.setScaledContents(True)
        elif filtro == 'BP':
            self.ui.Filter_Image.setPixmap(QtGui.QPixmap("src/Images/BP.png"))
            self.ui.Filter_Image.setScaledContents(True)
        elif filtro == 'BR':
            self.ui.Filter_Image.setPixmap(QtGui.QPixmap("src/Images/BR.png"))
            self.ui.Filter_Image.setScaledContents(True)
        else:
            print('Filtro Incorrecto')

    def CreateNew(self):
        # botón de crear un filtro nuevo
        bob = UF.FilterMaker()
        new_filter = self.parse_specs()  # creamos un nuevo filtro
        if not self.identicalTwins(new_filter):
            if not bob.make_filter(new_filter):
                self.printMsg(bob.err_msg)
            else:
                self.printMsg(bob.msg)
                self.filter_list.append(bob)  # Lo sumamos a nuestra lista
                self.manage_plot()
                # self.filter_list[-1].handlePlot(self.axes_mag,self.canvas_mag) #dibujame papu
                tempObject = plotControl(self, bob.name)
                tempItem = QtWidgets.QListWidgetItem()
                tempItem.setSizeHint(tempObject.sizeHint())
                self.ui.FilterList.addItem(tempItem)
                self.ui.FilterList.setItemWidget(tempItem, tempObject)
                self.manage_plot()
        else:
            msg ="No se admiten gemelos, aborten..."
            self.printMsg(msg)

    def parse_specs(self):
        """
        Parsea los datos cargados, en caso de estar correctamente cargados,
        crea un diccionario con el siguiente esqueleto:
        filtro = {'N':X, 'Q':X.xx, 'E':X%, 'aprox':..., 'ft':..., 'Go':X.xx,
                 'fpp':X.xx, 'fpm':X.xx, 'fap':X.xx, 'fam':X.xx, 'Ap':X.xx, 'Aa':X.xx }
        """
        # cargamos todos los datos del filtro, supongo que fueron corroborados antes

        filter = {}

        if self.ui.CheckMinOrden.isChecked():
            filter['N'] = 0
        else:
            filter['N'] = self.ui.NumOrden.value()

        if self.ui.CheckQmax.isChecked():
            filter['Q'] = 'auto'
        else:
            filter['Q'] = self.ui.SpinBoxQ.value()

        if self.ui.CheckDesnorm.isChecked():
            filter['E'] = 'auto'
        else:
            filter['E'] = self.ui.SpinBoxDesnorm.value()

        filter['aprox'] = self.ui.CBAprox.currentText()
        filter['ft'] = self.ui.CBFilters.currentText()
        filter['Go'] = self.ui.SpinBoxGain.value()
        filter['fpp'] = self.ui.SpinBoxFpplus.value()
        filter['fpm'] = self.ui.SpinBoxFpminus.value()
        filter['fap'] = self.ui.SpinBoxFaplus.value()
        filter['fam'] = self.ui.SpinBoxFaminus.value()
        filter['Ap'] = self.ui.SpinBoxAp.value()
        filter['Aa'] = self.ui.SpinBoxAa.value()

        hand.save_data(filter)
        return filter

    def identicalTwins(self, data):
        for i in self.filter_list:
            if i.name == str(data):
                return True  # Sin GEMELOS
        return False  # Felicidades es un BARON/VARON

    def recover(self, data):
        self.ui.NumOrden.setValue(int(data['N'][0]))
        if data['Q'][0] != 'auto':
            self.ui.SpinBoxQ.setValue(float(data['Q'][0]))
        else:
            self.ui.CheckQmax.setChecked(True)
        if data['E'][0] != 'auto':
            self.ui.SpinBoxDesnorm.setValue(int(data['E'][0]))
        else:
            self.ui.CheckDesnorm.setChecked(True)
        self.ui.CBAprox.setCurrentText((data['aprox'][0]))
        self.ui.CBFilters.setCurrentText(data['ft'][0])
        self.ui.SpinBoxGain.setValue(float(data['Go'][0]))
        self.ui.SpinBoxFpplus.setValue(float(data['fpp'][0]))
        self.ui.SpinBoxFpminus.setValue(float(data['fpm'][0]))
        self.ui.SpinBoxFaplus.setValue(float(data['fap'][0]))
        self.ui.SpinBoxFaminus.setValue(float(data['fam'][0]))
        self.ui.SpinBoxAp.setValue(float(data['Ap'][0]))
        self.ui.SpinBoxAa.setValue(float(data['Aa'][0]))

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

    def selected_filter(self):
        self.ui.textBrowser.append(("me clickearon"))
        # print("me clickearon!")


    def printMsg(self,msg):
        self.ui.textBrowser.append(msg)

    #
    # def sheet(self):
    #     self.currentsheet=

    def manage_plot(self):
        w = self.ui.GraphsWidget.currentWidget()
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
            axes.grid(which='both')
            plotter(axes, canvas)

    def magplot(self, axes, canvas):
        w = np.logspace(np.log10(self.lowestFreq() / 10), np.log10(self.lowestFreq() * 10), num=10000) * 2 * np.pi
        for f in self.filter_list:
            if f.chk:
                bode = ss.bode(ss.TransferFunction(f.Filtro.b,f.Filtro.a),w=w)
                axes.plot(bode[0] / (2 * np.pi), bode[1])
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()
        canvas.draw()

    def atePlot(self, axes, canvas):
        w = np.logspace(np.log10(self.lowestFreq() / 10), np.log10(self.lowestFreq() * 10), num=10000) * 2 * np.pi
        for f in self.filter_list:
            if f.chk:
                bode = ss.bode(ss.TransferFunction(f.Filtro.b, f.Filtro.a), w=w)
                axes.plot(bode[0] / (2 * np.pi), 1/bode[1])
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Magnitude [dB]')
        axes.minorticks_on()
        canvas.draw()

    def pazPlot(self, axes, canvas):
        #theta = np.linspace(-np.pi, np.pi, 201)
        #axes.plot(np.sin(theta), np.cos(theta), color='gray', linewidth=0.2)
        #plt.annotate("ωo", pol2cart(1, np.pi / 4))
        for f in self.filter_list:
            if f.chk:
                poles = np.roots(f.Filtro.a)
                zeros = np.roots(f.Filtro.b)
                axes.plot(np.real(poles), np.imag(poles), 'Xb', label='Poles' + f.name)
                axes.plot(np.real(zeros), np.imag(zeros), 'or', label='Zeros' + f.name)
        axes.axhline(y=0, color='gray', linewidth=1)
        axes.axvline(x=0, color='gray', linewidth=1)
        axes.set_xlabel("Real")
        axes.set_ylabel("Imaginary")
        axes.legend(loc='best')
        canvas.draw()

    def fasPlot(self, axes, canvas):
        w = np.logspace(np.log10(self.lowestFreq() / 10), np.log10(self.lowestFreq() * 10), num=10000) * 2 * np.pi
        for f in self.filter_list:
            if f.chk:
                bode = ss.bode(ss.TransferFunction(f.Filtro.b, f.Filtro.a), w=w)
                axes.plot(bode[0] / (2 * np.pi), bode[2])
        axes.set_xscale('log')
        axes.set_xlabel('Frequency [Hz]');
        axes.set_ylabel('Phase [º]')
        axes.minorticks_on()
        canvas.draw()

    def rdgPlot(self, axes, canvas):
        for f in self.filter_list:
            if f.chk:
                w, gd = ss.group_delay((f.Filtro.a, f.Filtro.b))
                axes.plot(w/(2 * np.pi), gd)
        axes.set_xscale('log')
        axes.set_ylabel('Group delay [samples]')
        axes.set_xlabel('Frequency [Hz]')
        axes.minorticks_on()
        canvas.draw()

    def impPlot(self, axes, canvas):
        for f in self.filter_list:
            if f.chk:
                H = ss.lti(f.Filtro.b,f.Filtro.a)
                time, resp = H.impulse()
                axes.plot(time, resp)
        axes.set_xlabel('time')
        axes.set_ylabel('Amplitude')
        canvas.draw()
    def escPlot(self, axes, canvas):
        for f in self.filter_list:
            if f.chk:
                H = ss.lti(f.Filtro.b,f.Filtro.a)
                time, resp = H.step()
                axes.plot(time, resp)
        axes.set_xlabel('time')
        axes.set_ylabel('Amplitude')
        canvas.draw()

    def lowestFreq(self):
        lf = []
        filtro = self.ui.CBFilters.currentText()
        for f in self.filter_list:
            if filtro == 'LP' or filtro == 'HP':
                lf.append(f.Filtro.fap)
            elif filtro == 'BP' or filtro == 'BR':
                lf.append(f.Filtro.fam)
            else:
                print('Filtro Incorrecto')
        return min(lf)
    def highestFreq(self):
        hf = []
        filtro = self.ui.CBFilters.currentText()
        for f in self.filter_list:
            if filtro == 'LP' or filtro == 'HP':
                hf.append(f.Filtro.fpp)
            elif filtro == 'BP' or filtro == 'BP':
                hf.append(f.Filtro.fap)
            else:
                print('Filtro Incorrecto')
        return max(hf)
# ------------------------------------------------------------
if __name__ == '__main__':
    MyFilterToolApp = QtWidgets.QApplication(sys.argv)
    MyFilterTool = AppCLass()
    MyFilterTool.show()
    sys.exit(MyFilterToolApp.exec_())
