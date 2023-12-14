import time
import sys
from typing import List, Dict, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, \
    QVBoxLayout, QGridLayout, QLabel, QFileDialog, QListWidget, QComboBox, QMainWindow, \
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDesktopWidget
# from win32api import GetFiletitleInfo
from config.config import NAME_REALLAB, LIST_FILE, SERVER_HOST
from pyModbusTCP.client import ModbusClient

cl = ModbusClient(host=SERVER_HOST)

class MainWindow(QMainWindow):
    # cycle_plc = 0.01

    def __init__(self, title: str = '') -> None:
        super().__init__()
        self.df = None
        self.ready_plot = False
        self.files, self.extension = None, None
        self.base_signals, self.secondary_signals = [], []
        self.dict_x_axe, self.dict_base_axe, self.dict_secondary_axe = {}, {}, {}
        self.field_name = ("Основная Ось", "Вспомогательная Ось", "Ось X (Времени)")
        self.title = f'{NAME_REALLAB}  {title}'
        self.width = 450
        self.height = 200
        self.dict_module = dict()
        with open(LIST_FILE, '+r', encoding='UTF-8') as f:
            for line in f.readlines():
                print(line)
                num, mac = line.split(':')
                if num not in self.dict_module:
                    self.dict_module[num] = mac

        self.setup_ui(self.title)

    def setup_ui(self, title) -> None:
        # qtRectangle = self.frameGeometry()   # получение размеров окна 
        centerPoint = QDesktopWidget().availableGeometry().center()  # центр экрана
        self.setGeometry(centerPoint.x(), centerPoint.y(), self.width, self.height)
        self.setWindowTitle(title)

        btn_mac = QPushButton('Change MAC')
        btn_mac.clicked.connect(self.change_mac)

        btn_read_mac = QPushButton('Read MAC')
        btn_read_mac.clicked.connect(self.read_mac)
        
        list_module = ['NLS-16DI-Ethernet', 'NLS-16DO-Ethernet', 'NLS-8R-Ethernet']
        self.combobox_module = QComboBox()
        self.combobox_module.addItems(list_module)
        self.combobox_module.setCurrentIndex(1)

        self.combobox_number = QComboBox()
        self.combobox_number.addItems(self.dict_module.keys())
        self.combobox_number.setCurrentIndex(1)

        # main_layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Выбор названия модуля'))
        main_layout.addWidget(self.combobox_module)
        main_layout.addWidget(QLabel('Ввод заводского номера модуля'))
        main_layout.addWidget(self.combobox_number)
        main_layout.addWidget(btn_mac)
        main_layout.addWidget(btn_read_mac)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)
        
    def change_mac(self) -> None:
        self.log_message()
        self.dialog_box()
        
    def read_mac(self) -> None:
        mac = cl.read_holding_registers(1, 8)
        print(mac)
    
        # self.log_message()
        # self.dialog_box()

    def log_message(self) -> None:
        """
        Clear all old signals and insert new signals to QTable(Список сигналов)
        """
        module = self.combobox_module.currentText().split()
        num = self.combobox_number.currentText()
        print(f'{module} Ser.:{num} -> set MAC {self.dict_module[num]}'.split())

    def dialog_box(self) -> None:
        QMessageBox.information(self, QMessageBox.StandardButton.Ok)
    

def main():
    global app
    sys_argv = sys.argv
    # if '.exe' in sys.argv[0]:                                # если EXE in Win
    #     title = GetFiletitleInfo(sys.argv[0], '\\')
    #     title = (title['FiletitleMS'] // 65536, title['FiletitleMS'] % 65536, title['FiletitleLS'] // 65536, title['FiletitleLS'] % 65536)
    #     title = '#' + '.'.join(map(str, title))
    # else:
    #     with open('setup.py', 'r+', encoding='utf-8') as f:
    #         title = f.readline()
    #     print(title)

    app = QApplication(sys_argv)
    ex = MainWindow("#0.0.0.0")
    ex.show()
    try:
        sys.exit(app.exec())
    except:
        print("Пока")

if __name__ == '__main__':
    main()