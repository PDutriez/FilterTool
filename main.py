# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import src.ui.filterwindow as ou
import AppClass as AC
import sys



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyFilterToolApp = AC.QtWidgets.QApplication(sys.argv)
    MyFilterTool = AC.AppCLass()
    MyFilterTool.show()
    sys.exit(MyFilterToolApp.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
