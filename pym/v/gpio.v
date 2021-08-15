/* Generated by Yosys 0.9+4081 (git sha1 e2c95800, gcc 7.5.0-3ubuntu1~18.04 -fPIC -Os) */

(* \nmigen.hierarchy  = "top" *)
(* top =  1  *)
(* generator = "nMigen" *)
module top(bus__dat_w, bus__dat_r, bus__sel, bus__cyc, bus__stb, bus__we, bus__ack, gpio_i, gpio_o, gpio_z, clk, rst, bus__adr);
  reg \initial  = 0;
  (* src = "gpio.py:50" *)
  wire \$1 ;
  (* src = "gpio.py:50" *)
  wire \$3 ;
  (* src = "gpio.py:67" *)
  wire \$5 ;
  (* src = "gpio.py:20" *)
  output bus__ack;
  reg bus__ack = 1'h0;
  (* src = "gpio.py:20" *)
  reg \bus__ack$next ;
  (* src = "gpio.py:20" *)
  input [7:0] bus__adr;
  (* src = "gpio.py:20" *)
  input bus__cyc;
  (* src = "gpio.py:20" *)
  output [31:0] bus__dat_r;
  reg [31:0] bus__dat_r;
  (* src = "gpio.py:20" *)
  input [31:0] bus__dat_w;
  (* src = "gpio.py:20" *)
  input bus__sel;
  (* src = "gpio.py:20" *)
  input bus__stb;
  (* src = "gpio.py:20" *)
  input bus__we;
  (* src = "/home/franz/.local/lib/python3.8/site-packages/nmigen-0.3.dev256+gabb2642-py3.8.egg/nmigen/hdl/ir.py:524" *)
  input clk;
  (* src = "gpio.py:28" *)
  reg [31:0] ddr_reg = 32'd0;
  (* src = "gpio.py:28" *)
  reg [31:0] \ddr_reg$next ;
  (* src = "gpio.py:11" *)
  input [15:0] gpio_i;
  (* src = "gpio.py:10" *)
  output [15:0] gpio_o;
  (* src = "gpio.py:12" *)
  output [15:0] gpio_z;
  (* src = "gpio.py:48" *)
  wire i_wen;
  (* src = "gpio.py:45" *)
  wire [31:0] pins_buf;
  (* src = "gpio.py:27" *)
  reg [31:0] port_reg = 32'd0;
  (* src = "gpio.py:27" *)
  reg [31:0] \port_reg$next ;
  (* src = "/home/franz/.local/lib/python3.8/site-packages/nmigen-0.3.dev256+gabb2642-py3.8.egg/nmigen/hdl/ir.py:524" *)
  input rst;
  assign \$1  = bus__cyc & (* src = "gpio.py:50" *) bus__stb;
  assign \$3  = \$1  & (* src = "gpio.py:50" *) bus__we;
  assign \$5  = bus__cyc & (* src = "gpio.py:67" *) bus__stb;
  always @(posedge clk)
    bus__ack <= \bus__ack$next ;
  always @(posedge clk)
    ddr_reg <= \ddr_reg$next ;
  always @(posedge clk)
    port_reg <= \port_reg$next ;
  always @* begin
    if (\initial ) begin end
    (* full_case = 32'd1 *)
    (* src = "gpio.py:55" *)
    casez (bus__adr[4:2])
      /* src = "gpio.py:56" */
      3'h0:
          bus__dat_r = port_reg;
      /* src = "gpio.py:60" */
      3'h1:
          bus__dat_r = ddr_reg;
      /* src = "gpio.py:64" */
      default:
          bus__dat_r = pins_buf;
    endcase
  end
  always @* begin
    if (\initial ) begin end
    \port_reg$next  = port_reg;
    (* src = "gpio.py:55" *)
    casez (bus__adr[4:2])
      /* src = "gpio.py:56" */
      3'h0:
          (* src = "gpio.py:58" *)
          casez (i_wen)
            /* src = "gpio.py:58" */
            1'h1:
                \port_reg$next  = bus__dat_w;
          endcase
    endcase
    (* src = "/home/franz/.local/lib/python3.8/site-packages/nmigen-0.3.dev256+gabb2642-py3.8.egg/nmigen/hdl/xfrm.py:519" *)
    casez (rst)
      1'h1:
          \port_reg$next  = 32'd0;
    endcase
  end
  always @* begin
    if (\initial ) begin end
    \ddr_reg$next  = ddr_reg;
    (* src = "gpio.py:55" *)
    casez (bus__adr[4:2])
      /* src = "gpio.py:56" */
      3'h0:
          /* empty */;
      /* src = "gpio.py:60" */
      3'h1:
          (* src = "gpio.py:62" *)
          casez (i_wen)
            /* src = "gpio.py:62" */
            1'h1:
                \ddr_reg$next  = bus__dat_w;
          endcase
    endcase
    (* src = "/home/franz/.local/lib/python3.8/site-packages/nmigen-0.3.dev256+gabb2642-py3.8.egg/nmigen/hdl/xfrm.py:519" *)
    casez (rst)
      1'h1:
          \ddr_reg$next  = 32'd0;
    endcase
  end
  always @* begin
    if (\initial ) begin end
    (* full_case = 32'd1 *)
    (* src = "gpio.py:67" *)
    casez (\$5 )
      /* src = "gpio.py:67" */
      1'h1:
          \bus__ack$next  = 1'h1;
      /* src = "gpio.py:69" */
      default:
          \bus__ack$next  = 1'h0;
    endcase
    (* src = "/home/franz/.local/lib/python3.8/site-packages/nmigen-0.3.dev256+gabb2642-py3.8.egg/nmigen/hdl/xfrm.py:519" *)
    casez (rst)
      1'h1:
          \bus__ack$next  = 1'h0;
    endcase
  end
  assign gpio_z = ddr_reg[15:0];
  assign gpio_o = port_reg[15:0];
  assign i_wen = \$3 ;
  assign pins_buf = { 16'h0000, gpio_i };
endmodule

