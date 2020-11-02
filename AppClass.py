import sys
from src.ui.filterwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from src import UniFilter as UF
from src.lib import handy as hand
from src.lib.PlotControl import plotControl
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
                print(bob.err_msg)
            else:
                self.filter_list.append(bob) #Lo sumamos a nuestra lista
                self.filter_list[-1].handlePlot(self.axes_mag,self.canvas_mag) #dibujame papu
                tempObject = plotControl(self, bob.name)
                tempItem = QtWidgets.QListWidgetItem()
                tempItem.setSizeHint(tempObject.sizeHint())
                self.ui.FilterList.addItem(tempItem)
                self.ui.FilterList.setItemWidget(tempItem, tempObject)



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
    def identicalTwins(self,data):
        for i in self.filter_list:
            if i.name == str(data):
                return True #Sin GEMELOS
        return False #Felicidades es un BARON/VARON

    def recover(self,data):
        self.ui.NumOrden.setValue(int(data['N'][0]))
        if data['Q'][0] != 'auto':
            self.ui.SpinBoxQ.setValue(float(data['Q'][0]))
        if data['E'][0] != 'auto':
            self.ui.SpinBoxDesnorm.setValue(int(data['E'][0]))
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
        print("me clickearon!")

# ------------------------------------------------------------
if __name__ == '__main__':
    MyFilterToolApp = QtWidgets.QApplication(sys.argv)
    MyFilterTool = AppCLass()
    MyFilterTool.show()
    sys.exit(MyFilterToolApp.exec_())
