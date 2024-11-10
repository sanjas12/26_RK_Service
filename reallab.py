import time
import sys
from typing import List, Dict, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, \
    QVBoxLayout, QGridLayout, QLabel, QFileDialog, QListWidget, QComboBox, QMainWindow, \
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDesktopWidget, QLineEdit
# from win32api import GetFiletitleInfo
import config.config as cnf
from pyModbusTCP.client import ModbusClient
from collections import namedtuple
# from data_reallab import Module
from connect_module import ConnectModule 
from orm import Module, DbSession

 
class MainWindow(QMainWindow):

    def __init__(self, title: str = '') -> None:
        super().__init__()
        self.df = None
        self.files, self.extension = None, None
        self.title = f'{cnf.MODULE_NAME}  {title}'
        self.width = 550
        self.height = 200
        self.dict_module = dict()
        self.orm_base_modules = Module()
        # self.create_database()     # только для создания базы
        self.setup_ui(self.title)
        self.cl = ConnectModule(host=cnf.LOCAL_HOST)
        print(1)
    
    def setup_ui(self, title) -> None:
        # qtRectangle = self.frameGeometry()   # получение размеров окна 
        centerPoint = QDesktopWidget().availableGeometry().center()  # центр экрана
        self.setGeometry(centerPoint.x(), centerPoint.y(), self.width, self.height)
        self.setWindowTitle(title)

        # первый слой 
        btn_mac = QPushButton('Change MAC')
        btn_mac.clicked.connect(self.change_mac)
        
        btn_dhcp_off = QPushButton('DHCP off')
        btn_dhcp_off.clicked.connect(self.dhcp_off)

        btn_dhcp_on = QPushButton('DHCP on')
        btn_dhcp_on.clicked.connect(self.dhcp_on)
        dhcp_lay = QHBoxLayout()
        dhcp_lay.addWidget(btn_dhcp_off)
        dhcp_lay.addWidget(btn_dhcp_on)
        self.dhcp_GroupBox = QGroupBox("DHCP on\off")
        self.dhcp_GroupBox.setLayout(dhcp_lay)


        btn_info = QPushButton('Get info module')
        btn_info.clicked.connect(self.get_info_module)
        
        btn_change_ip = QPushButton('Change IP')
        btn_change_ip.clicked.connect(self.change_ip)

        # list_module = ['NLS-16DI-Ethernet', 'NLS-16DO-Ethernet', 'NLS-8R-Ethernet']
        self.combobox_module = QComboBox()
        self.combobox_module.addItems(self.dict_module.keys())
        self.combobox_module.setCurrentIndex(1)

        self.combobox_number = QComboBox()
        self.combobox_number.addItems(self.dict_module.keys())
        self.combobox_number.setCurrentIndex(1)

        defautl_ip = cnf.DEFAULT_IP
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
        fisrt_lay.addWidget(btn_mac)
        fisrt_lay.addWidget(self.dhcp_GroupBox)
        fisrt_lay.addWidget(btn_info)
        fisrt_lay.addWidget(self.ip_GroupBox)
        fisrt_lay.addWidget(btn_change_ip)
        

        self.first_GroupBox = QGroupBox()
        self.first_GroupBox.setLayout(fisrt_lay)
        
        # второй слой 
        self.ql_info = QLabel()
        self.second_lay = QHBoxLayout()
        self.second_lay.addWidget(self.ql_info)
        self.second_GroupBox = QGroupBox()
        self.second_GroupBox.setLayout(self.second_lay)

        # main_layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.first_GroupBox)
        main_layout.addWidget(self.second_GroupBox)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)

    def is_con_ok(self):
        # print('is_con_ok')
        # while True:
        self.cl.connect_to_module()
            # time.sleep(cnf.TIME_TO_CONNECT)

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

    def read_data(self):
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
        self.cl.dhcp_off()
        time.sleep(1)
        self.get_info_module()

    def dhcp_on(self) -> None:
        self.cl.dhcp_on()
        time.sleep(1)
        self.get_info_module()

    def get_info_module(self):
        if self.cl.con_is_ok:
            self.ql_info.setText(self.cl.get_info_module())
        else:
            print("Don't connect to module")

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
    ex.get_info_module()

    #TODO
    # while перевести на asich
    while True:
        ex.is_con_ok()
        # print('main while')
        try:
            sys.exit(app.exec())
            time.sleep(cnf.TIME_TO_CONNECT)
        except:
            print("Пока")

if __name__ == '__main__':
    main()