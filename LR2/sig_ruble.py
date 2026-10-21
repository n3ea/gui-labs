from PyQt5.QtCore import QObject, pyqtSignal


class RubleChannel(QObject):
    value_entered = pyqtSignal(float)