import config.config as cnf
from pymodbus.client import ModbusTcpClient
import config.config as cnf
import time
from binascii import unhexlify


class ConnectModule:
    name_addr = 200
    ver_addr = 212
    ip_addr = 256 
    mac_addr = 262
    dhcp_addr = 266

    def __init__(self, host=cnf.SERVER_HOST, port=cnf.SERVER_PORT, timeout=cnf.TIME_TO_CONNECT):
        self.msg = ''
        self.host = host
        self.port = port
        self.timeout = timeout
        self.cl = ModbusTcpClient(host=self.host, port=self.port, timeout=self.timeout)
        self.cl.connect() 
        if self.cl.connected:
            print(f'Connected  to {self.host}:{cnf.SERVER_PORT}:{cnf.MODULE_NAME}')
        # self.is_connected()

    # def is_connected(self):
    #     if self.cl.connected:
    #         print(f'Connected  to {self.host}:{cnf.SERVER_PORT}:{cnf.MODULE_NAME}')
    #         return True
    #     else:
    #         print(f'do not connect {self.host}:{cnf.SERVER_PORT}:{cnf.MODULE_NAME}')
    #         return False
    

    def get_info_module(self):
        if self.cl.connected:
            name_info = self.cl.read_holding_registers(__class__.name_addr, count=4)
            ver_info = self.cl.read_holding_registers(__class__.ver_addr, count=4)     
            ip_info = self.cl.read_holding_registers(__class__.ip_addr, count=2)
            ip_adrr = []
            if ip_info:
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
                print('нет данныx о DHCP')

            name_info = ''.join([''.join(map(chr, self.bytess(char))) for char in name_info])
            ver_info = ''.join([''.join(map(chr, self.bytess(char))) for char in ver_info])
            ip_info = '.'.join(ip_adrr)
            mac_info = ''.join(['.'.join(map(hex, self.bytess(char))) for char in mac_info])
            mac_info = mac_info.replace("0x", "").upper()

            self.msg = f'name->{name_info}, version->{ver_info}, mac->{mac_info}, dhcp-> {dhcp_info}, ip-> {ip_info}'

            print(self.msg)
            return self.msg
        else:
            self.print_con_is_not_ok()

    def bytess(self, integer):
        return divmod((integer), 0x100)

    def change_mac(self) -> None:
        if self.cl.connected:
            # tran = 0x0001
            # pro_id =0x0000
            # length = 0x0017     # 23 байта
            # addr = 0x01
            # code = 0x10         # 16 function code 
            # start_addr = 0x0320    # 0x0320     - dec->800
            # num_registr = 0x0008    # количество регистров
            # num_byte = 0x10    # 10- кол-во байт 
            # reallab = 0x4d4143   # - код конторы
            # end = 0x2E

            # от Вани если MAC -> AA.BB.CC.DD.EE.FF
            example = '00.01.00.00.00.17.01.10.03.20.00.08.10.4D.41.43.3A.AA.2E.BB.2E.CC.2E.DD.2E.EE.2E.FF.2E.'
            mac = '70-B3-D5-22-31-E3'
            mac = 'AA-BB-CC-DD-EE-FF'
            
            example = ''.join(example.split('.'))

            mac = mac.split('-')
            prefix = ['3A', '2E', '2E', '2E', '2E', '2E']
            new_mac = []
            
            for ma, da in zip(prefix, mac):
                new_mac.append(ma+da)
            
            new_mac = ' '.join(new_mac)
            start = '0001 0000 0017 0110 0320 0008 104D 4143 '
            end = ' 2E'

            mac = start + new_mac + end
            # mac = mac.replace(' ', '')
            print(mac)
            
            mac_bytes = bytes.fromhex(mac)
            print(mac_bytes)
            # print(len(mac_bytes))
           
            # print(example)
            # example_bytes = bytes.fromhex(example)
            # print(example_bytes)  
            # print(len(example_bytes))

            write_ok = self.cl.write_registers(__class__.mac_addr, mac_bytes)
            # write_ok = self.cl.write_single_register(__class__.mac_addr, mac_bytes)
            print(write_ok)
            if write_ok:
                print('MAC -> changed')
        else:
            self.print_con_is_not_ok()

    def dhcp_off(self):
        if self.cl.connected:
            write_response = self.cl.write_register(__class__.dhcp_addr, 0)
            if not write_response.isError():
                print(f'DHCP -> OFF')
            else:
                print("не хаписано")
        else:
            self.print_con_is_not_ok()

    def dhcp_on(self):
        if self.cl.connected:
            write_ok = self.cl.write_register(__class__.dhcp_addr, 1)
            if write_ok:
                print(f'DHCP -> ON')
        else:
            self.print_con_is_not_ok()

    def change_ip(self, ip:bytearray ):
        # read_ip = '0001 0000 0006 0103 0100 0002'
        # print('ip str->', read_ip)
        # read_ip = bytes.fromhex(read_ip)
        # print('ip byte->', read_ip)

        # mac_info = self.cl.read_holding_registers(__class__.mac_addr, 3)     # - dhcp_off только в Init
        # print(ip)

        if self.cl.connected:
            # ip_bytes = bytes.fromhex(' '.join(map(str, ip)))
            # print(ip_bytes)
            # print(len(mac_bytes))

            ip_change = self.cl.write_registers(__class__.ip_addr, ip)
            print(ip_change)
            if ip_change:
                print(f'IP -> Changed')
        else:
            self.print_con_is_not_ok()

    def print_con_is_not_ok(self):
        print('Connect failed')

    def close(self):
        if self.cl.connected:
            print(f'Disconnected  from {self.host}:{cnf.SERVER_PORT}:{cnf.MODULE_NAME}')
            self.cl.close()

def main():
    c = ConnectModule(cnf.LOCAL_HOST)
    try:
        while True:
            c.dhcp_off() 
            # c.get_info_module()
            time.sleep(2)
    except KeyboardInterrupt:
        print("Остановка программы пользователем.")
        c.close()
    except Exception as e:
        print((f"Произошла ошибка: {e}"))


if __name__ == '__main__':
    main()