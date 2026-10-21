import sys
from PyQt5.QtWidgets import QApplication

from sig_dollar import DollarChannel
from sig_euro import EuroChannel
from sig_ruble import RubleChannel
from sig_control import ControlChannel
from converter import ConverterWidget


def main():
    app = QApplication(sys.argv)

    ruble_sig = RubleChannel()
    dollar_sig = DollarChannel()
    euro_sig = EuroChannel()
    control_sig = ControlChannel()

    window = ConverterWidget(dollar_sig, euro_sig, ruble_sig, control_sig)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()