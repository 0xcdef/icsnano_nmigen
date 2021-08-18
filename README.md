nMigen demos for iCESugar-Nano board
-------------------------------------
# Usage
Project test under Ubuntu/Windows WSL/CentOS/msys2

### Pull the project to your local
    $git clone https://gitee.com/x55aa/icsnano_nmigen

### Check tool chains:
    $cd icsnano_nmigen
    $./tools/check_tools.py --nmigen-gitee

if get error like `**check_tools.py**  is not executable`, try `$chmod +x ./tools/check_tools.py`<br>
for other errors, the message will guide you to resolve the problem.

### Connect your iCESugar-nano

for Windows user, open hardware manager to confirm serial port : like **COM4** <br>
for Linux user, serial device ' **/dev/ttyACM0** ' is created. you can run `dmesg | grep usb` for more details<br>
for WSL, the windows serial **COMx**  mapped to **/dev/ttySx**<br>
for msys2, following the case of Windows. target ports should be given like **COMx**

#### important notes:
    confirm that you have access rights (w/r) for serial port and usbhid devices created by icelink.
    if not, you can just change their access control by `$sudo chmod 666 /dev/xxx`.
    but for general usage, it's recommended to setup your udev configure file to control the devices.
    for details, please refer to:

    https://github.com/trabucayre/openFPGALoader/blob/master/INSTALL.md#udev-rules

### Build and program
    $python3 wb_bridge.py

### Test
    $./tools/pmod_led.sh /dev/ttyS4
    - change '/dev/ttyS4' to your device node.
this demo run with 'pmod_led' board, if you do not have one, you can try:`$python3 blink.py`

## Project summary

   **blink.py** : a simple blink demo
  
   **uart_echo.py** : echo anything received from serial port. you can run 'screen /dev/ttySx' to test
  
   **wb_bridge.py** : a wishbone bridge based serial control terminal
	    gpio module mapped to 0x10000000, with PORT/DDR/PIN registers implemented
	    you can read/write those register by `tools/uterm.py` utility
  
   **tools/check_tools.py** : utility to check python and fpga toolchains. 
	    `$./tools/check_tools.py --nmigen-gitee` is recommanded (to install nmigen stuffs)
  
   **tools/pmod3_led.sh** : bash script for pmod_led test
  
   **tools/uterm.py** : communicate with wishbone bridge to control gpio module of wb_bridge project
