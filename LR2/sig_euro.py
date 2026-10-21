from PyQt5.QtCore import QObject, pyqtSignal


class EuroChannel(QObject):
    value_entered = pyqtSignal(float)