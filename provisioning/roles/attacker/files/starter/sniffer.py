#!/usr/bin/env python3
# Starter code for Mission 1 (adapted from the SEED "Packet Sniffing and Spoofing" lab).
# The interface name is looked up for you with `lab-iface`.  Run with:  sudo python3 sniffer.py
import subprocess

from scapy.all import *

IFACE = subprocess.check_output(["lab-iface"], text=True).strip()


def print_pkt(pkt):
    pkt.show()


pkt = sniff(iface=IFACE, filter='icmp', prn=print_pkt)
