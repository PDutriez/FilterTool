from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame, QMessageBox, QColorDialog
from src.ui.plotcontrol import Ui_plotControlWrapper
import AppStages as AS
import sys

class plotControl(QWidget, Ui_plotControlWrapper):

    def __init__(self, mainWindow, plotModelInfo):
        super(plotControl, self).__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.model = plotModelInfo
        self.label_plot.setText(self.model.name)
        self.checkBox_plot.setChecked(True)
        self.checkBox_plot.stateChanged.connect(self.toggleVisible)
        self.toolButton_plotCol.pressed.connect(self.selectColor)
        self.toolButton_plotDel.pressed.connect(self.destroyPlot)
        self.button_SOS.pressed.connect(self.openSOS_Window)
        # self.checkBox_plot.setChecked(True)

    def toggleVisible(self):

        if self.checkBox_plot.isChecked():
            self.model.setVisible(True)
        else:
            self.model.setVisible(False)
        self.mainWindow.manage_plot()

    def selectColor(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()
        if color.isValid():
            self.model.setPlotColor(color)
            self.mainWindow.manage_plot()

    def destroyPlot(self):
        self.mainWindow.delete_PlotControlItem(self)

    def openSOS_Window(self):
        #MyStagesToolApp = AS.QtWidgets.QApplication(sys.argv)
        self.MyStagesTool = AS.AppStages()
        self.MyStagesTool.receive_stages(self.model.Filtro.b,self.model.Filtro.a)
        self.MyStagesTool.show()
        #sys.exit(MyStagesToolApp.exec_())