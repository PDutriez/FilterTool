# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import designer.output as ou
import sys



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = ou.QtWidgets.QApplication(sys.argv)
    MainWindow = ou.QtWidgets.QWidget()
    ui = ou.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
