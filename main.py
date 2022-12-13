from PyQt5 import QtWidgets

from model.main_window_model import LoginWindow
from qt_material import apply_stylesheet
import qtmodern.styles
import qtmodern.windows
if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    qtmodern.styles.light(app)

    widget = LoginWindow()
    widget.show()

    app.exec_()


