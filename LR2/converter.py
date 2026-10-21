from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
)
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json


class ConverterWidget(QWidget):
    def __init__(self, dollar_sig, euro_sig, ruble_sig, control_sig):
        super().__init__()

        self.dollar_sig = dollar_sig
        self.euro_sig = euro_sig
        self.ruble_sig = ruble_sig
        self.control_sig = control_sig

        self.updating = False

        # Базовые курсы на случай, если API не ответит
        self.rates = {
            'usd_to_rub': 82.14,
            'eur_to_rub': 92.17,
            'usd_to_eur': 82.14 / 92.17,
            'eur_to_usd': 92.17 / 82.14,
            'rub_to_usd': 1 / 82.14,
            'rub_to_eur': 1 / 92.17,
        }

        self.network_manager = QNetworkAccessManager()

        self.build_ui()
        self.connect_all()
        
        self.update_rates_from_api()

    def build_ui(self):
        self.setWindowTitle('Конвертер валют (ЛР2)')
        self.resize(400, 250)

        root = QVBoxLayout()
        self.setLayout(root)

        self.rub_edit = self._add_field(root, 'Рубли (RUB):')
        self.usd_edit = self._add_field(root, 'Доллары (USD):')
        self.eur_edit = self._add_field(root, 'Евро (EUR):')

        self.clear_btn = QPushButton('Очистить все поля')
        root.addWidget(self.clear_btn)

    def _add_field(self, layout, title):
        row = QHBoxLayout()
        row.addWidget(QLabel(title))
        edit = QLineEdit()
        row.addWidget(edit)
        layout.addLayout(row)
        return edit

    def connect_all(self):
        self.usd_edit.textChanged.connect(self._usd_typed)
        self.eur_edit.textChanged.connect(self._eur_typed)
        self.rub_edit.textChanged.connect(self._rub_typed)

        self.dollar_sig.value_entered.connect(self._recalc_from_usd)
        self.euro_sig.value_entered.connect(self._recalc_from_eur)
        self.ruble_sig.value_entered.connect(self._recalc_from_rub)

        self.clear_btn.clicked.connect(self.control_sig.clear_requested.emit)
        self.control_sig.clear_requested.connect(self._clear_all)

    def update_rates_from_api(self):
        url = "https://open.er-api.com/v6/latest/USD"
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)
        self.network_manager.finished.connect(self.on_api_response)

    def on_api_response(self, reply):
        error = reply.error()
        if error == reply.NoError:
            raw = reply.readAll().data()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                print("Ошибка парсинга JSON")
                return

            if data.get("result") == "success":
                rates = data.get("rates", {})
                usd_to_rub = rates.get('RUB', 0)
                usd_to_eur = rates.get('EUR', 0)

                if usd_to_eur and usd_to_rub:
                    self.rates['usd_to_rub'] = usd_to_rub
                    self.rates['eur_to_rub'] = usd_to_rub / usd_to_eur
                    self.rates['usd_to_eur'] = usd_to_eur
                    self.rates['eur_to_usd'] = 1 / usd_to_eur
                    self.rates['rub_to_usd'] = 1 / usd_to_rub
                    self.rates['rub_to_eur'] = 1 / self.rates['eur_to_rub']
                    
                    print(f"Курсы загружены: 1 USD = {usd_to_rub} RUB, 1 EUR = {self.rates['eur_to_rub']:.2f} RUB")
                else:
                    print("В ответе API нет курсов EUR или RUB")
            else:
                print("API вернул ошибку:", data.get("error-type", "неизвестно"))
        else:
            print("Ошибка сети:", reply.errorString())

    def _usd_typed(self, text):
        if self.updating: return
        v = self._to_float(text)
        if v is not None:
            self.dollar_sig.value_entered.emit(v)

    def _eur_typed(self, text):
        if self.updating: return
        v = self._to_float(text)
        if v is not None:
            self.euro_sig.value_entered.emit(v)

    def _rub_typed(self, text):
        if self.updating: return
        v = self._to_float(text)
        if v is not None:
            self.ruble_sig.value_entered.emit(v)

    @pyqtSlot(float)
    def _recalc_from_usd(self, usd):
        self.updating = True
        self.rub_edit.setText(f"{usd * self.rates['usd_to_rub']:.2f}")
        self.eur_edit.setText(f"{usd * self.rates['usd_to_eur']:.2f}")
        self.updating = False

    @pyqtSlot(float)
    def _recalc_from_eur(self, eur):
        self.updating = True
        self.rub_edit.setText(f"{eur * self.rates['eur_to_rub']:.2f}")
        self.usd_edit.setText(f"{eur * self.rates['eur_to_usd']:.2f}")
        self.updating = False

    @pyqtSlot(float)
    def _recalc_from_rub(self, rub):
        self.updating = True
        self.usd_edit.setText(f"{rub * self.rates['rub_to_usd']:.2f}")
        self.eur_edit.setText(f"{rub * self.rates['rub_to_eur']:.2f}")
        self.updating = False

    @pyqtSlot()
    def _clear_all(self):
        self.updating = True
        self.rub_edit.clear()
        self.usd_edit.clear()
        self.eur_edit.clear()
        self.updating = False

    @staticmethod
    def _to_float(text):
        try:
            return float(text.replace(',', '.'))
        except ValueError:
            return None