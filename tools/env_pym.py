#!/usr/bin/env python3

import os
import sys

# step 1: python version
vs = sys.version.split()[0]
vv = vs.split('.')

vi = int(vv[0])*10 + int(vv[1])

if vi < 36:
    print(">> Your python version : {}".format(vs))
    print(">> But version 3.6 is minimal for nMigen!")
    exit(0)

print(">> Python check pass!")

# step 2: nMigen module
import subprocess
import pkg_resources

required = {'nmigen', 'nmigen-soc', 'nmigen-stdio', 'nmigen-boards', 'pyserial'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if len(missing) > 0:
    print(">> Install missing modules:")
    python = sys.executable
    for mm in missing:
        print(">> ...Install ", mm)
        subprocess.check_call([python, '-m', 'pip', 'install', mm], stdout=subprocess.DEVNULL)

print(">> Python modules ready!")

# fpga toolchain
fpga_tools = {'yosys', 'icepack', 'nxtpnr-ice40'}

r = 0
for t in fpga_tools:
    r += os.system("which {}".format(t))

    if r != 0:
        print(">> {} is not found, check that!".format(t))

if r != 0:
    print(">> fpga toolchain seems not proper installed!")
    print(">> ==========================================================")
    print(">> for linux/mac, follow prebuild image is recommended")
    print(">>   https://github.com/YosysHQ/fpga-toolchain/releases")
    print(">> for windows user, msys2 + eda package is recommended")
    print(">>   [msys2] $ pacman -S mingw-w64-x86_64-eda")
    print(">>   make sure 'yosys', 'icestorm', 'nxtpnr', 'icesprog' selected")
    print(">> ==========================================================")
    exit(0)
else:
    print(">> fpga toolchain ready!")
