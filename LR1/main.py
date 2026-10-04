import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Лабораторная работа №1")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        self.label = QLabel("При нажатии кнопки надпись меняется на изображение)))")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")

        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setMinimumSize(1, 1)

        layout.addWidget(self.label)

        self.button = QPushButton("Показать изображение")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

        self.original_pixmap = None


    def on_button_clicked(self):
        """Открывает диалог выбора изображения и показывает его в QLabel."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{file_path}", )
            return

        self.original_pixmap = pixmap
        self._update_pixmap()


    def _update_pixmap(self):
        """Масштабирует оригинал под текущий размер QLabel."""
        if self.original_pixmap is None:
            return

        if self.label.width() <= 0 or self.label.height() <= 0:
            return

        scaled = self.original_pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation,  )
        self.label.setText("")
        self.label.setPixmap(scaled)


    def resizeEvent(self, event):
        """При изменении размера окна пересчитываем масштаб картинки."""
        super().resizeEvent(event)
        if self.original_pixmap is not None:
            self._update_pixmap()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()