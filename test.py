import logging
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton

app = QApplication(sys.argv)
window = QFrame()

layout = QVBoxLayout()

labels1 = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5", "Label 6", "Label 7"]
labels2 = ["Label 8", "Label 9"]
current_labels = labels1
page_size = 3
current_page = 0
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())
def show_page():
    global current_page, layout, current_labels
    try:
        clearLayout(layout)
    except BaseException as e:
        logging.exception(e)
    for i in range(current_page * page_size, (current_page + 1) * page_size):
        if i >= len(current_labels):
            break
        row_layout = QHBoxLayout()
        for j in range(3):
            if i + j < len(current_labels):
                label = QLabel(current_labels[i + j])
            else:
                label = QLabel("nothing")
            row_layout.addWidget(label)
        layout.addLayout(row_layout)
    if current_page * page_size + page_size < len(current_labels):
        layout.addWidget(next_button)

def handle_next():
    global current_page, current_labels
    current_page += 1
    if current_page * page_size >= len(current_labels):
        current_page = 0
        if current_labels == labels1:
            current_labels = labels2
        else:
            current_labels = labels1
    show_page()

next_button = QPushButton("Next")
next_button.clicked.connect(handle_next)

show_page()
window.setLayout(layout)
window.show()
sys.exit(app.exec_())
