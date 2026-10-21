from PyQt5.QtCore import QObject, pyqtSignal


class ControlChannel(QObject):
    clear_requested = pyqtSignal()