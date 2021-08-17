from nmigen import *
from nmigen_stdio.serial import AsyncSerial, AsyncSerialTX
from pym.icesugar_nano import *

class UARTEcho(Elaboratable):
    def __init__(self, divisor, pins):
        self._pins = pins
        self._divisor = divisor

    def elaborate(self, platform):
        m = Module()

        m.submodules.serial = serial = AsyncSerial(divisor=self._divisor, pins=self._pins)

        data = Signal(8)

        with m.FSM():
            with m.State("Receive"):
                m.d.comb += serial.rx.ack.eq(1)

                with m.If(serial.rx.rdy):
                    m.d.sync += data.eq(serial.rx.data)
                    m.next = "Send-Data"
            with m.State("Send-Data"):
                m.d.comb += serial.tx.ack.eq(1)
                m.d.comb += serial.tx.data.eq(data)

                with m.If(serial.tx.rdy):
                    m.next = "Receive"

        return m

if __name__ == "__main__":
    p = iCESugarNanoPlatform()

    uart_pins = p.request("uart", 0)
    uart_divisor = int(p.default_clk_frequency // 115200)

    demo = UARTEcho(uart_divisor, uart_pins)
    p.build(demo, do_program=True)
