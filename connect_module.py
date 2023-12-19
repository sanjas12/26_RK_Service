import config.config as cnf
from pyModbusTCP.client import ModbusClient
import config.config as cnf
import time
from binascii import unhexlify


class ConnectModule:
    name_addr = 200
    ver_addr = 212
    ip_addr = 256 
    mac_addr = 262
    dhcp_addr = 266


    def __init__(self):
        self.msg = ''
        try:
            self.cl = ModbusClient(cnf.SERVER_HOST, cnf.SERVER_PORT, timeout=cnf.TIME_TO_CONNECT)
            print(f'Connection {cnf.SERVER_HOST} {cnf.SERVER_PORT} -> created sucsecc')
        except ValueError:
            print("Error with host or port parametrs")
        self.connect_to_module()

    def connect_to_module(self) -> None:
        if not self.cl.is_open():
            if not self.cl.open():
                print(f'do not connect {cnf.SERVER_HOST} + {cnf.SERVER_PORT} + {cnf.MODULE_NAME}')
        else:
            print('Connect is OK')
    
    def get_info_module(self):
        name_info = self.cl.read_holding_registers(__class__.name_addr, 4)
        ver_info = self.cl.read_holding_registers(__class__.ver_addr, 4)     
        ip_info = self.cl.read_holding_registers(__class__.ip_addr, 2)
        ip_adrr = []
        for char in ip_info:
            h, l = self.bytess(char)
            ip_adrr.append(str(h))     
            ip_adrr.append(str(l))     
        mac_info = self.cl.read_holding_registers(__class__.mac_addr, 3)     
        if self.cl.read_holding_registers(__class__.dhcp_addr, 1):      
            if self.cl.read_holding_registers(__class__.dhcp_addr, 1)[0] == 0:     # - dhcp_off только в Init
                dhcp_info = 'выкл'
            else:
                dhcp_info = 'вкл'
        else:
            print('нет данныз о DHCP')

        name_info = ''.join([''.join(map(chr, self.bytess(char))) for char in name_info])
        ver_info = ''.join([''.join(map(chr, self.bytess(char))) for char in ver_info])
        ip_info = '.'.join(ip_adrr)
        mac_info = ''.join(['.'.join(map(hex, self.bytess(char))) for char in mac_info])
        mac_info = mac_info.replace("0x", "").upper()

        self.msg = f'name->{name_info}, version->{ver_info}, mac->{mac_info}, dhcp-> {dhcp_info}, ip-> {ip_info}'

        print(self.msg)
        return self.msg

    def bytess(self, integer):
        return divmod((integer), 0x100)

    def change_mac(self) -> None:
        tran = 0x0001
        pro_id =0x0000
        length = 0x0017     # 23 байта
        addr = 0x01
        code = 0x10         # 16 function code 
        ch_mac_addr = 0x0320    # 0x0320     - dec->800
        xa = 0x0008    # количество регистров
        xz = 0x10    # 10- кол-во байт 
        reallab = 0x4d4143   # - код конторы
        end = 0x2E

        mac = '70-B3-D5-22-31-E3'
        mac = mac.split('-')
        prefix = ['3A', '2E', '2E', '2E', '2E', '2E']
        new_mac = []
        for ma, da in zip(prefix, mac):
            new_mac.append(ma+da)
        new_mac = ' '.join(new_mac)
        start = '0001 0000 0017 0110 0320 0008 104D 4143 '
        end = ' 2E'

        mac = start + new_mac + end
        print(mac)
        
        mac = bytes.fromhex(mac)
        print(mac)

        w = self.cl.write_multiple_registers(ch_mac_addr, mac)
        print(w)
        if w:
            print('mac -> changed')

        # mac_info = self.cl.read_holding_registers(__class__.mac_addr, 3)     # - dhcp_off только в Init
        # mac_info = ''.join(['.'.join(map(hex, self.bytess(char))) for char in mac_info])
        # mac_info = mac_info.replace("0x", "").upper()

        # self.msg = f'name->{name_info}, version->{ver_info}, mac->{mac_info}, dhcp-> {dhcp_info}'

        # print(mac_info)

    def dhcp_off(self):
        dhcp_off = '0001 0000 0006 0106 010A 0000'
        print(dhcp_off)
        dhcp_off = bytes.fromhex(dhcp_off)
        print(dhcp_off)

        write_ok = self.cl.write_multiple_registers(__class__.dhcp_addr, dhcp_off)

        if write_ok:
            print(f'DHCP -> OFF')

    def read_ip(self):
        # read_ip = '0001 0000 0006 0103 0100 0002'
        # print('ip str->', read_ip)
        # read_ip = bytes.fromhex(read_ip)
        # print('ip byte->', read_ip)

        # mac_info = self.cl.read_holding_registers(__class__.mac_addr, 3)     # - dhcp_off только в Init

        read_ip_ok = self.cl.read_holding_registers(__class__.ip_addr, read_ip)



def main():
    c = ConnectModule()
    while True:
        # c.get_info_module()
        c.change_mac()
        time.sleep(5)


if __name__ == '__main__':
    main()