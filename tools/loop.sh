#!/bin/bash

[[ -z "$1" ]] && port="/dev/ttyACM0" || port="$1"

[[ ! -e $port ]] && echo ">> Target port not exists!" && exit 0

i=1
for ((;;)) do
	let v=255-i
	vv=$(printf '0x%02x' $v)
	./uterm.py -p $port 0x10000000 $vv 2>/dev/null
	[[ "$?" != "0" ]] && break
       	sleep 0.1
	let i=i*2
	[[ $i -eq 128 ]] && let i=1
done
