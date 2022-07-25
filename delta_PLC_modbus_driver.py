from time import sleep

from pyModbusTCP.client import ModbusClient


class PLCDelta(ModbusClient):

    def __init__(self, ip_addr='127.0.0.1', port=10002):
        try:
            ModbusClient.__init__(self, host=ip_addr, port=port, auto_open=True, auto_close=False)
        except ValueError:
            print("Error with host or port params")

    @classmethod
    def convert_addr(cls, addr: str) -> int:

        # convert addr X0.0 - X63.15
        if addr[0].upper() == 'X' and '.' in addr:
            addr_elements = addr[1:].split('.')
            modul = int(addr_elements[0])
            m_input = int(addr_elements[1])
            if 0 <= modul <= 63 and 0 <= m_input <= 15:
                return 24576+(modul*16)+m_input
            else:
                print('Wrong input number')

        # convert addr X0-X63
        elif addr[0].upper() == 'X' and '.' not in addr:
            x = int(addr[1:])
            if 0 <= x <= 63:
                return 32768 + x
            else:
                print('Wrong input register number')

        # convert addr Y0.0 - Y 63.15
        elif addr[0].upper() == 'Y' and '.' in addr:
            addr_elements = addr[1:].split('.')
            modul = int(addr_elements[0])
            m_output = int(addr_elements[1])
            if 0 <= modul <= 63 and 0 <= m_output <= 15:
                return 40960 + (modul*16) + m_output
            else:
                print('Wrong coil register number')

        # convert addr Y0 - Y63
        elif addr[0].upper() == 'Y' and '.' not in addr:
            y = int(addr[1:])
            if 0 <= y <= 63:
                return 40960 + y
            else:
                print('Wrong coil register number')

        # convert addr M0 - M8191 markers
        elif addr[0].upper() == 'M':
            m = int(addr[1:])
            if 0 <= m <= 8191:
                return m
            else:
                print('Wrong marker number')

        # convert addr D0 - D29999
        elif addr[0].upper() == 'D' and '.' not in addr:
            d = int(addr[1:])
            if 0 <= d <= 29999:
                return d
            else:
                print('Wrong data register number')

    def write_plc_bit(self, bit_addr: str, bit_value: bool):
        if bit_addr[0].upper() in 'MY':
            self.write_single_coil(bit_addr=self.convert_addr(bit_addr), bit_value=bit_value)

    def read_plc_bit(self, bit_addr: str):
        if bit_addr[1].upper() == 'X':
            return self.read_discrete_inputs(bit_addr=self.convert_addr(bit_addr))[0]
        else:
            return self.read_coils(bit_addr=self.convert_addr(bit_addr))[0]

    def read_plc_register(self, reg_addr: str):
        if reg_addr[0].upper() == 'X':
            return self.read_input_registers(reg_addr=self.convert_addr(reg_addr))[0]
        elif reg_addr[0].upper() in 'YD':
            return self.read_holding_registers(reg_addr=self.convert_addr(reg_addr))[0]

    def write_plc_register(self, reg_addr: str, reg_value: int):
        if reg_addr[0].upper() in 'YD':
            self.write_single_register(reg_addr=self.convert_addr(reg_addr), reg_value=reg_value)

    def write_plc_registers(self, list_of_values: list, first_reg_addr: str, n: int = 1):
        # check max range of address
        if first_reg_addr[0].upper() == 'Y' and int(first_reg_addr[1:]) + n > 63:
            n = n-(int(first_reg_addr[1:]) + n - 63)
        if first_reg_addr[0].upper() == 'D' and int(first_reg_addr[1:]) + n > 29999:
            n = n - (int(first_reg_addr[1:]) + n - 29999)
        # check length of values list
        if len(list_of_values) < n:
            n = len(list_of_values)
        # write registers
        for value in list_of_values[:n]:
            self.write_plc_register(reg_addr=first_reg_addr, reg_value=value)
            first_reg_addr = first_reg_addr[0] + str(int(first_reg_addr[1:]) + 1)


def main():
    plc = PLCDelta(ip_addr='localhost')
    while True:
        byte_list = list(range(5, 20, 10))
        print(len(byte_list))
        plc.write_plc_registers(byte_list, 'd0')
        sleep(1)


if __name__ == '__main__':
    main()
