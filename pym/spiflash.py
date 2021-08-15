from nmigen import *
from nmigen.lib.io import *
from nmigen_soc import wishbone
from nmigen_soc.memory import MemoryMap

__all__ = ["SpiFlashCtrl"]

class DummyIO():
    def __init__(self, width, name='io'):
        self.o = Signal(width, name='%s_o'%name)
        self.i = Signal(width, name='%s_i'%name)
        self.oe = Signal(width, name='%s_z'%name)
        self.width = width

    def __len__(self):
        return self.width

class SpiFlashCtrl(Elaboratable):
    def __init__(self, pins):
        self.bus = wishbone.Interface(addr_width=8,
                                      data_width=32, granularity=32)

        # memory_map to make decoder happy
        _mmap = MemoryMap(addr_width=8, data_width=32, alignment=0)
        self.bus.memory_map = _mmap

        self.pins = pins

        self.port_reg = Signal(32)
        self.ddr_reg = Signal(32)

    def elaborate(self, platform):
        m = Module()

        if platform is None:
            ports_o = self.pins.o
            ports_oe = self.pins.oe
            ports_i = self.pins.i
        else:
            ports_o = [ pin.o for pin in self.pins ]
            ports_oe = [ pin.oe for pin in self.pins ]
            ports_i = [ pin.i for pin in self.pins ]

        if len(self.pins) > 32:
            raise ValueError("length of self.pins may not be greater than 32!")

        pins_buf = Signal(32)
        m.d.comb += pins_buf.eq(Cat(ports_i, C(0, 32-len(self.pins))))

        i_wen = Signal()
        m.d.comb += [
                i_wen.eq(self.bus.cyc & self.bus.stb & self.bus.we),
                Cat(ports_o).eq(self.port_reg),
                Cat(ports_oe).eq(self.ddr_reg),
        ]

        with m.Switch(self.bus.adr[2:5]):
            with m.Case(0): 
                m.d.comb += self.bus.dat_r.eq(self.port_reg)
                with m.If(i_wen):
                    m.d.sync += self.port_reg.eq(self.bus.dat_w)
            with m.Case(1):
                m.d.comb += self.bus.dat_r.eq(self.ddr_reg)
                with m.If(i_wen):
                    m.d.sync += self.ddr_reg.eq(self.bus.dat_w)
            with m.Default():
                    m.d.comb += self.bus.dat_r.eq(pins_buf)

        with m.If(self.bus.cyc & self.bus.stb):
            m.d.sync += self.bus.ack.eq(1)
        with m.Else():
            m.d.sync += self.bus.ack.eq(0)

        return m

    def ports(self):
        return [_ for _ in self.bus.fields.values()] + [ self.pins.i, self.pins.o, self.pins.oe ]

if __name__ == "__main__":
    p = GpioCtrl(DummyIO(16, 'gpio'))
    from nmigen.back import verilog
    print(verilog.convert(p, ports=p.ports()))
