#!/usr/bin/env python3
import sys
from serial import Serial

def Usage():
    help_string = '''Usage: uterm -p PORT address [ data ]
        -p      : target serial port, "COMx", "/dev/ttySx" or "/dev/ttyACMx"
        address : target address, hex string, like "0x10000004"
        data    : optional, data for write to address, hex string
                  do read from address if w_data is not given.'''
    print(help_string)

def main():

    skip = 0
    port = ""
    address = ""
    data = ""
    i = 1
    for args in sys.argv[1:]:
        i += 1
        if skip == 1:
            skip = 0
            continue
        elif args == "-p":
            skip = 1
            port = sys.argv[i]
        elif address == "":
            address = args
        else:
            data = args

    if len(sys.argv) < 2 or port == "":
        Usage()
        sys.exit()

    try:
        p = Serial(port=port, baudrate=115200, timeout=0.1)
        p.flush()
    except:
        print("Serial open failed, check your settings!")
    
    try:
        if data != "":
            cmd_w = "0x0101{:08x}{:08x}".format(int(address, 16), int(data, 16))
            cmd_w = int(cmd_w, 16).to_bytes(10, 'big')
            p.write(cmd_w)
            p.flush()
        else:
            p.readall()
            cmd_r = "0x0201{:08x}".format(int(address, 16))
            cmd_r = int(cmd_r, 16).to_bytes(6, 'big')
            p.write(cmd_r)

            dd = b'' 
            ds = b'' 
            while ds == b'':
                ds = p.readall()

            dd += ds
            while ds != b'':
                ds = p.readall()
                dd += ds

            print(*["{:02x}".format(_) for _ in dd])
    except ValueError:
        print("Seems you given wrong address/data, check and try again!")

    if p is not None:
        p.close()

if __name__ == "__main__":
    main()
