# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import src.ui.filterwindow as ou
import AppClass as AC
import sys



if __name__ == '__main__':
    print(AC.QtWidgets.QStyleFactory.keys())
    MyFilterToolApp = AC.QtWidgets.QApplication(sys.argv)
    MyFilterToolApp.setStyle(AC.QtWidgets.QStyleFactory.create("MacOS"))
    MyFilterTool = AC.AppCLass()
    MyFilterTool.show()
    sys.exit(MyFilterToolApp.exec_())

