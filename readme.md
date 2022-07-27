This python module allow writes and reads bits and registers 
to PLC Delta Electronics AS series via MODBUS TCP/IP using simple syntax.

For read bits, available:
    X0.0 - X63.15 input memory area
    Y0.0 - Y63.15 output memory area
    M0 - M8191 marker area

For write bits, available:
    Y0.0 - Y63.15 output memory area
    M0 - M8191 marker area

For reading registers, available:
    X0 - X63 input memory area
    Y0 - Y63 output memory area
    D0 - D29999 data area

For write registers, available:
    Y0 - Y63 output memory area
    D0 - D29999 data area

