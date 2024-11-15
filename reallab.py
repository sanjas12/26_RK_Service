import time
import sys
from typing import List, Dict, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, \
    QVBoxLayout, QGridLayout, QLabel, QFileDialog, QListWidget, QComboBox, QMainWindow, \
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDesktopWidget, QLineEdit
# from win32api import GetFiletitleInfo
import config.config as cnf
# from pyModbusTCP.client import ModbusClient
from collections import namedtuple
# from data_reallab import Module
from connect_module import ConnectModule 
# from orm import Module, DbSession

 
class MainWindow(QMainWindow):

    def __init__(self, title: str = '') -> None:
        super().__init__()
        self.df = None
        self.files, self.extension = None, None
        self.title = f'{cnf.MODULE_NAME}  {title}'
        self.width = 550
        self.height = 200
        self.dict_module = dict()
        # self.orm_base_modules = Module()
        self.is_connected = False
        # self.create_database()     # только для создания базы
        self.setup_ui(self.title)
    
    def setup_ui(self, title) -> None:
        # qtRectangle = self.frameGeometry()   # получение размеров окна 
        centerPoint = QDesktopWidget().availableGeometry().center()  # центр экрана
        self.setGeometry(centerPoint.x(), centerPoint.y(), self.width, self.height)
        self.setWindowTitle(title)

        # первый слой 
        self.btn_mac = QPushButton('Change MAC')
        self.btn_mac.clicked.connect(self.change_mac)
        self.btn_mac.setEnabled(False)
        
        self.btn_dhcp_off = QPushButton('DHCP off')
        self.btn_dhcp_off.clicked.connect(self.dhcp_off)
        self.btn_dhcp_off.setEnabled(False)

        self.btn_dhcp_on = QPushButton('DHCP on')
        self.btn_dhcp_on.clicked.connect(self.dhcp_on)
        self.btn_dhcp_on.setEnabled(False)
        dhcp_lay = QHBoxLayout()
        dhcp_lay.addWidget(self.btn_dhcp_off)
        dhcp_lay.addWidget(self.btn_dhcp_on)
        self.dhcp_GroupBox = QGroupBox("DHCP on\off")
        self.dhcp_GroupBox.setLayout(dhcp_lay)


        self.btn_info = QPushButton('Get info module')
        self.btn_info.clicked.connect(self.get_info_module)
        self.btn_info.setEnabled(False)

        self.btn_change_ip = QPushButton('Change IP')
        self.btn_change_ip.clicked.connect(self.change_ip)
        self.btn_change_ip.setEnabled(False)

        # list_module = ['NLS-16DI-Ethernet', 'NLS-16DO-Ethernet', 'NLS-8R-Ethernet']
        self.combobox_module = QComboBox()
        self.combobox_module.addItems(self.dict_module.keys())
        self.combobox_module.setCurrentIndex(1)

        self.combobox_number = QComboBox()
        self.combobox_number.addItems(self.dict_module.keys())
        self.combobox_number.setCurrentIndex(1)

        defautl_ip = cnf.SERVER_HOST
        # defautl_ip = cnf.LOCAL_IP
        self.ql_edit  = QLineEdit()
        self.ql_edit.setText(defautl_ip.split('.')[0])
        self.ql_edit_1  = QLineEdit()
        self.ql_edit_1.setText(defautl_ip.split('.')[1])
        self.ql_edit_2 = QLineEdit()
        self.ql_edit_2.setText(defautl_ip.split('.')[2])
        self.ql_edit_3 = QLineEdit()
        self.ql_edit_3.setText(defautl_ip.split('.')[3])
        
        ip_lay = QHBoxLayout()
        ip_lay.addWidget(self.ql_edit)
        ip_lay.addWidget(self.ql_edit_1)
        ip_lay.addWidget(self.ql_edit_2)
        ip_lay.addWidget(self.ql_edit_3)
        self.ip_GroupBox = QGroupBox("Set IP:")
        self.ip_GroupBox.setLayout(ip_lay)

        fisrt_lay = QVBoxLayout()
        fisrt_lay.addWidget(QLabel('Выбор названия модуля'))
        fisrt_lay.addWidget(self.combobox_module)
        fisrt_lay.addWidget(QLabel('Ввод заводского номера модуля'))
        fisrt_lay.addWidget(self.combobox_number)
        fisrt_lay.addWidget(self.btn_mac)
        fisrt_lay.addWidget(self.dhcp_GroupBox)
        fisrt_lay.addWidget(self.btn_info)
        fisrt_lay.addWidget(self.ip_GroupBox)
        fisrt_lay.addWidget(self.btn_change_ip)
        

        self.first_GroupBox = QGroupBox()
        self.first_GroupBox.setLayout(fisrt_lay)
        
        # второй слой 
        second_lay = QVBoxLayout()
        ip = QLineEdit()
        ip.setText(cnf.LOCAL_HOST)
        ip.setFixedWidth(100)
        second_lay.addWidget(ip)
        self.btn_connect = QPushButton('Connect to module')
        self.btn_connect.clicked.connect(lambda: self.connected_to_module(ip.text()))
        self.btn_connect.setEnabled(True)
        second_lay.addWidget(self.btn_connect)
        self.btn_disconnect = QPushButton('Disconnect from module')
        self.btn_disconnect.clicked.connect(self.disconnected_from_module)
        self.btn_disconnect.setEnabled(False)
        second_lay.addWidget(self.btn_disconnect)

        second_GroupBox = QGroupBox("Connect\Disconnect")
        second_GroupBox.setLayout(second_lay)
        
        self.ql_info = QLabel()
        second_lay.addWidget(self.ql_info)
        

        # main_layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(second_GroupBox)
        main_layout.addWidget(self.first_GroupBox)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)

    def connected_to_module(self, host=cnf.LOCAL_HOST):
        if not self.is_connected:
            self.cl = ConnectModule(host=host)
            if self.cl.cl.connected: 
                self.is_connected = True
                self.btn_disconnect.setEnabled(True)
                self.btn_connect.setEnabled(False)
                self.btn_change_ip.setEnabled(True)
                self.btn_dhcp_off.setEnabled(True)
                self.btn_dhcp_on.setEnabled(True)
                self.btn_info.setEnabled(True)
                self.btn_mac.setEnabled(True)
        else:
            print("Is connected")

    def disconnected_from_module(self):
        if self.is_connected:
            self.is_connected = False
            self.btn_connect.setEnabled(True)
            self.btn_disconnect.setEnabled(False)
            self.btn_change_ip.setEnabled(False)
            self.btn_dhcp_off.setEnabled(False)
            self.btn_dhcp_on.setEnabled(False)
            self.btn_info.setEnabled(False)
            self.btn_mac.setEnabled(False)
            self.cl.close()

    def create_database(self):
                with open(cnf.LIST_FILE, '+r', encoding=cnf.ENCODING) as f:
                    for i, line in enumerate(f.readlines()):
                        if line.startswith('#'):
                            continue
                        if len(line) > 1 :
                            mod, ser, mac = line.strip().replace('№', '').split('|')
                            if mod == None:
                                continue
                            else:
                                self.dict_module.setdefault(mod)
                                self.dict_module[mod] = {ser:mac}
                                # print(mod, ser, mac)
                                with DbSession() as db_session:
                                    new_entry = Module(type=mod, ser=ser, mac=mac)
                                    db_session.add(new_entry)
                    print(f'items in {cnf.LIST_FILE}-> {i}')

    def read_data_from_database(self):
        with DbSession() as db_session:
            db_session.query(Movie).all()

    def change_mac(self) -> None:
        self.cl.change_mac()

    def change_ip(self) -> None:
        ip_set = (
            int(self.ql_edit.text(), 16).to_bytes(2, "big"), 
            int(self.ql_edit_1.text(), 16).to_bytes(2, "big"),
            int(self.ql_edit_2.text(), 16).to_bytes(2, "big"),
            int(self.ql_edit_3.text(), 16).to_bytes(2, "big")
            )
        # ip_set = (self.ql_edit.text().to_byte(), self.ql_edit_1.text(), self.ql_edit_2.text(),  self.ql_edit_3.text())
        # ip_set = ("192", "168", "100", "101")    

        print(ip_set)

        # for octet in ip_set:
        #     print(type(octet))
        #     octet = hex(octet)
        #     octet = hex(octet)
        #     print(octet, len(octet))

        ip_byte = bytearray() 
        ip_byte = ip_set[0]+ip_set[1]+ip_set[2]+ip_set[3]

        print('byte ->', ip_byte)
        print('hex ->', ip_byte.hex())

        # ip_set = (self.ql_edit.text(), self.ql_edit_1.text(), self.ql_edit_2.text(), self.ql_edit_3.text())
        # print(ip_set)
        
        # new_ip = ' '.join(ip_set)
        # print(new_ip)
        
        self.cl.change_ip(ip_byte)
        time.sleep(1)
        self.get_info_module()

    def dhcp_off(self) -> None:
        if self.is_connected:
            self.cl.dhcp_off()
            time.sleep(1)
            # self.get_info_module()

    def dhcp_on(self) -> None:
        if self.is_connected:
            self.cl.dhcp_on()
            time.sleep(1)
            self.is_connected = False
            # self.get_info_module()

    def get_info_module(self):
        self.ql_info.setText(self.cl.get_info_module())

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
    except SystemExit:
        print("Пока")
        # if ex.is_connected: 
        #     print("закрыть соединение") # Проверка, если соединение установлено
        #     ex.diconnected_from_module()

if __name__ == '__main__':
    main()