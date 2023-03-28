"""

1. Meniu principal cu x module ("Departamente") : Done
2. Module functionale: Clients, Comenzi, Stocuri si Produse. eg. 3/4 Module functionale.
3. Creare Clase Comenzi, Stocuri si Produse. Done
4. De verificat relatiile dintre clase: Clienti, Vanzari, Stocuri/Produse, optional: comenzi # Done
5. De creat un meniu pentru rapoarte la vanzari. - IDK

De facut la final/completat: Adaugare Tree view in [Creat Client] Form si [Edit Client Form].
De facut: Functie click la formul vanzari penetru a deschide formul de vanzare. De afcut metode de calcul al pretului total.
De modificat form-ul vanzari si view vanzari adica adaugat o variabila pentru a vedea dac factura a fost achitata integral.
de exemplu in functie de produse 5 produse de exemplu se face o lista separata cu un atribut produse facturate si daca coencide cu cantitatea totala produsul este facturat n totalitate
si daca tote produsele is facturate in totalitate toata vanzarea este facturata.
in form-ul de creare a facturii se completeaza automat factura totala si se poate modifica cantitatea prdoselor nu poate sa fife mai mare
se poate alege o cantitate mai mica si se  actualizeaza pretul dupa se cheama o functie din form vanzare si se actualizeaza list aaia de produse speciale. si se actualizeaza formul respefctiv.

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from client_combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QStringListModel

    app = QApplication(sys.argv)

    string_list = ['Cojocariu Daniel', 'Danila Daniel', 'Amariei Razvan', 'good bye']

    combo = ExtendedComboBox()

    # either fill the standard model of the client_combobox
    combo.addItems(string_list)

    # or use another model
    #combo.setModel(QStringListModel(string_list))

    combo.resize(300, 40)
    combo.show()

    sys.exit(app.exec_())