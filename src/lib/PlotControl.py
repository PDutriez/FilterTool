from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame, QMessageBox, QColorDialog
from src.ui.plotcontrol import Ui_plotControlWrapper

class plotControl(QWidget, Ui_plotControlWrapper):

    def __init__(self, mainWindow, plotModelInfo):
        super(plotControl, self).__init__()
        self.setupUi(self)

        self.mainWindow = mainWindow
        self.model = plotModelInfo
        self.label_plot.setText(self.model.name)
        self.checkBox_plot.stateChanged.connect(self.toggleVisible)
        #self.toolButton_plotCol.pressed.connect(self.selectColor)
        self.toolButton_plotDel.pressed.connect(self.destroyPlot)

        # self.checkBox_plot.setChecked(True)

    def toggleVisible(self):

        if self.checkBox_plot.isChecked():
            self.model.setVisible(True)
        else:
            self.model.setVisible(False)

#    def selectColor(self):

#        colorDialog = QColorDialog()
#        color = colorDialog.getColor()
#        if color.isValid():
#            self.model.setPlotColor(color)

    def destroyPlot(self):
        doomedName = self.model.name
        return doomedName
        #self.mainWindow.deletePlotControlItem(name=doomedName)