import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3: Библиотека")
        self.resize(850, 600)

        self.db = None
        self.current_table = None

        self.init_ui()
        self.init_menu()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.b1_btn = QPushButton("bt1 'SELECT * FROM sqlite_master'")
        self.b1_btn.clicked.connect(self.execute_b1_query)
        top_layout.addWidget(self.b1_btn)

        self.columns_combo = QComboBox()
        self.columns_combo.addItem("Выберите колонку...")
        self.columns_combo.currentIndexChanged.connect(self.on_column_selected)
        top_layout.addWidget(self.columns_combo)
        main_layout.addLayout(top_layout)

        bottom_layout = QHBoxLayout()
        self.b2_btn = QPushButton("bt2 'Популярные книги (ТОП-5)'")
        self.b2_btn.clicked.connect(self.execute_b2_query)
        bottom_layout.addWidget(self.b2_btn)

        self.b3_btn = QPushButton("bt3 'Активные читатели (ТОП-5)'")
        self.b3_btn.clicked.connect(self.execute_b3_query)
        bottom_layout.addWidget(self.b3_btn)
        main_layout.addLayout(bottom_layout)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.tabs = []
        for i in range(1, 6):
            tab = QWidget()
            layout = QVBoxLayout(tab)
            table = QTableWidget()
            layout.addWidget(table)
            self.tabs.append(table)
            self.tab_widget.addTab(tab, f"Tab{i}")

    def init_menu(self):
        menu_bar = self.menuBar()
        menu = menu_bar.addMenu("Menu")

        action_set = QAction("Set connection", self)
        action_set.triggered.connect(self.set_connection)
        menu.addAction(action_set)

        action_close = QAction("Close connection", self)
        action_close.triggered.connect(self.close_connection)
        menu.addAction(action_close)


    def set_connection(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть БД", "", "SQLite Files (*.db *.sqlite);;All files (*)"
        )
        if not file_path:
            return

        if self.db:
            self.db.close()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(file_path)

        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к БД")
            self.db = None
            return

        QMessageBox.information(self, "Успех", "База подключена!")
        self.setup_tab1()
        self.load_columns_list()

    def close_connection(self):
        if self.db:
            self.db.close()
            self.db = None
        
        for tab in self.tabs:
            tab.setRowCount(0)
            tab.setColumnCount(0)
            
        self.columns_combo.clear()
        self.columns_combo.addItem("Выберите колонку...")
        QMessageBox.information(self, "Инфо", "Соединение закрыто.")


    def setup_tab1(self):
        query = QSqlQuery("SELECT * FROM sqlite_master", self.db)
        self.display_query_results(query, self.tabs[0])

    def load_columns_list(self):
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'", self.db)
        tables = []
        while query.next():
            tables.append(query.value(0))

        if tables:
            self.current_table = tables[0] 
            query = QSqlQuery(f"PRAGMA table_info({self.current_table})", self.db)
            columns = []
            while query.next():
                col_name = query.value(1) 
                if col_name:
                    columns.append(col_name)

            self.columns_combo.clear()
            self.columns_combo.addItem("Выберите колонку...")
            self.columns_combo.addItems(columns)

    def display_query_results(self, query, table_widget):
        if not query.exec_():
            QMessageBox.critical(self, "Ошибка", query.lastError().text())
            return

        record = query.record()
        col_count = record.count()

        if col_count == 0:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        headers = [record.fieldName(i) for i in range(col_count)]
        table_widget.setColumnCount(col_count)
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(0)

        row_index = 0
        while query.next():
            table_widget.insertRow(row_index)
            for col in range(col_count):
                val = query.value(col)
                item = QTableWidgetItem(str(val) if val is not None else "NULL")
                table_widget.setItem(row_index, col, item)
            row_index += 1
            
        table_widget.resizeColumnsToContents()


    def execute_b1_query(self):
        if not self.db: return
        query = QSqlQuery("SELECT name FROM sqlite_master", self.db)
        self.display_query_results(query, self.tabs[1])

    def on_column_selected(self):
        selected_col = self.columns_combo.currentText()
        if selected_col == "Выберите колонку..." or not self.db or not self.current_table:
            return

        query = QSqlQuery(f"SELECT {selected_col} FROM {self.current_table} LIMIT 10", self.db)
        self.display_query_results(query, self.tabs[2])

    def execute_b2_query(self):
        if not self.db: return
        query_str = """
            SELECT books.title, COUNT(loans.id) as times_issued
            FROM loans
            JOIN books ON loans.book_id = books.id
            GROUP BY books.id
            ORDER BY times_issued DESC
            LIMIT 5
        """
        query = QSqlQuery(query_str, self.db)
        self.display_query_results(query, self.tabs[3])

    def execute_b3_query(self):
        if not self.db: return
        query_str = """
            SELECT readers.name, COUNT(loans.id) as books_taken
            FROM loans
            JOIN readers ON loans.reader_id = readers.id
            GROUP BY readers.id
            ORDER BY books_taken DESC
            LIMIT 5
        """
        query = QSqlQuery(query_str, self.db)
        self.display_query_results(query, self.tabs[4])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())