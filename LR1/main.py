import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QFileDialog, QMessageBox,)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt


class CanvasWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None

    def set_background(self, pixmap: QPixmap):
        self.background_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.background_pixmap is None:
            painter.fillRect(self.rect(), QColor(240, 240, 240))
            return

        scaled = self.background_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        painter.setOpacity(0.75)
        painter.drawPixmap(0, 0, scaled)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лабораторная работа №1")
        self.resize(600, 400)

        self.canvas = CanvasWidget()
        self.setCentralWidget(self.canvas)

        main_layout = QVBoxLayout()
        self.canvas.setLayout(main_layout)

        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white;"
            "background: transparent;"
        )
        main_layout.addStretch(1)
        main_layout.addWidget(self.label)
        main_layout.addStretch(1)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.button1 = QPushButton("Кнопка1")
        self.button2 = QPushButton("Кнопка2")
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button2)

        self.button1.clicked.connect(self.switch_text)
        self.button2.clicked.connect(self.upload_png)

    def switch_text(self):
        if self.label.text() == "Надпись":
            self.label.setText("Текст изменён!")
        else:
            self.label.setText("Надпись")

    def upload_png(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите PNG-изображение",
            "",
            "PNG Files (*.png);;All Files (*)",
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить изображение:\n{file_path}",
            )
            return

        self.canvas.set_background(pixmap)
        self._fit_window_to_pixmap(pixmap)

    def _fit_window_to_pixmap(self, pixmap: QPixmap):
        img_w = pixmap.width()
        img_h = pixmap.height()

        screen = QApplication.primaryScreen().availableGeometry()

        if img_w > screen.width() or img_h > screen.height():
            self.showMaximized()
        else:
            self.showNormal()
            self.resize(img_w, img_h)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()