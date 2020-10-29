# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import src.ui.filterwindow as ou
import sys



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = ou.QtWidgets.QApplication(sys.argv) #Instancia para iniciar una app
    FTMainWindow = ou.QtWidgets.QWidget()
    ui = ou.Ui_MainWindow()
    ui.setupUi(FTMainWindow)
    FTMainWindow.show()
    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
