from PyQt5.QtWidgets import QWidget
from src.ui.plotcontrol import Ui_plotControlWrapper


class stageControl(QWidget, Ui_plotControlWrapper):

    def __init__(self, mainWindow, stageInfo, name):
        super(stageControl, self).__init__()
        self.setupUi(self)

        self.mainWindow = mainWindow
        self.lista = stageInfo
        self.label_plot.setText("Stage "+str(name))
        self.index = name
        self.checkBox_plot.setChecked(False)
        self.checkBox_plot.stateChanged.connect(self.toggleVisible)
        self.toolButton_plotDel.setVisible(False)
        self.toolButton_plotCol.setVisible(False)
        self.button_SOS.setVisible(False)
        # self.toolButton_plotCol.pressed.connect(self.selectColor)
        #self.toolButton_plotDel.pressed.connect(self.destroyPlot)


    def toggleVisible(self):

        if self.checkBox_plot.isChecked():
            self.lista[self.index] = True
        else:
            self.lista[self.index] = False
        self.mainWindow.manage_plot()
