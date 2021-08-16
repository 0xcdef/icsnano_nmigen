import itertools
import math

from nmigen import *
from nmigen_boards.resources import *
from nmigen.build import *
from nmigen_soc import wishbone

from pym.icesugar_nano import *
from pym.uartbridge import *
from pym.gpio import *
from pym.spiflash import *

class WishboneToolDemo(Elaboratable):
    def __init__(self, uart_divisor, uart_pins, gpio_pins):

        self._wb_dec = wishbone.Decoder(addr_width=30, data_width=32, granularity=32)

        # wishbone master
        self._ub = UARTBridge(divisor=uart_divisor, pins=uart_pins)
        
        # wishbone devices
        self._gpio = GpioCtrl(pins=gpio_pins)
        self._wb_dec.add(self._gpio.bus, addr=0x10000000)

    def elaborate(self, p):
        m = Module()

        m.submodules.ub = self._ub
        m.submodules.wb_dec = self._wb_dec
        m.submodules.gpio = self._gpio

        m.d.comb += [
                self._ub.bus.connect(self._wb_dec.bus),
        ]

        return m

if __name__ == "__main__":

    pmod2_uart = [
        UARTResource(1, rx="C5", tx="B6",
            attrs=Attrs(IO_STANDARD="SB_LVTTL", PULLUP=1)),
    ]

    p = iCESugarNanoPlatform() 
    p.add_resources(p.gpio)
    p.add_resources(pmod2_uart)

    uart_pins = p.request("uart", 1)
    gpio_pins = []
    for idx in itertools.count():
        try:
            gpio_pins.append(p.request("PMOD3", idx))
        except ResourceError:
            break

    print("default_clk_frequency: {}".format(p.default_clk_frequency))
    uart_divisor = int(p.default_clk_frequency / 115200)
    demo = WishboneToolDemo(uart_divisor, uart_pins, gpio_pins)
    p.build(demo, build_dir="./build", do_program=True)
