#!/usr/bin/env bash
CURDIR=`pwd`
/sbin/ifconfig -a > "$CURDIR/ip.txt"
scp $CURDIR/ip.txt card-test:~/weiwei/ip/ip.txt
/home/ubuntu/.virtualenvs/py3/bin/python dns.py
