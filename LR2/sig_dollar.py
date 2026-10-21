from PyQt5.QtCore import QObject, pyqtSignal


class DollarChannel(QObject):
    value_entered = pyqtSignal(float)