import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from nmigen_boards.resources import *

__all__ = ["iCESugarNanoPlatform"]

class iCESugarNanoPlatform(LatticeICE40Platform):
    device      = "iCE40LP1K"
    package     = "CM36"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("D1", dir="i"),
                 Clock(12e6), Attrs(IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="B6", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        UARTResource(0, rx="A3", tx="B3",
            attrs=Attrs(IO_STANDARD="SB_LVTTL", PULLUP=1)),

        *SPIFlashResources(0,
            cs_n="D5", clk="E5", copi="E4", cipo="F5",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
    connectors  = [
        Connector("pmod", 1, "E2 D1 B1 A1 - -"), #PMOD1  
        Connector("pmod", 2, "B3 A3 B6 C5 - -"), #PMOD2
        Connector("pmod", 3, "B4 B5 E1 B1 - - C6 E3 C2 A1 - -"), #PMOD3
    ]

    gpio = [
        Resource("PMOD1", 0, Pins("1", dir="io", conn=("pmod", 1)),
                    Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD1", 1, Pins("2", dir="io", conn=("pmod", 1)),
                    Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD1", 2, Pins("3", dir="io", conn=("pmod", 1)),
                    Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD1", 3, Pins("4", dir="io", conn=("pmod", 1)),
                    Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 0, Pins("1", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 1, Pins("2", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 2, Pins("3", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 3, Pins("4", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 4, Pins("7", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 5, Pins("8", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 6, Pins("9", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("PMOD3", 7, Pins("10", dir="io", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
    ]

    pmod_led = [
       *LEDResources(pins={1: "1", 2:"2", 3:"3", 4:"4", 5:"7", 6:"8", 7:"9", 8:"10"}, conn=("pmod", 3),
                        attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 0, Pins("1", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 1, Pins("2", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 2, Pins("3", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 3, Pins("4", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 4, Pins("7", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 5, Pins("8", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 6, Pins("9", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pmod_led", 7, Pins("10", dir="o", conn=("pmod", 3)),
                        Attrs(IO_STANDARD="SB_LVCMOS")),
    ]

    def toolchain_program(self, products, name):
        icesprog = os.environ.get("ICESPROG", "icesprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([icesprog, "-w", bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import *
    iCESugarNanoPlatform().build(Blinky(), do_program=True)
