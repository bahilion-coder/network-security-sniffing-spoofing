#!/usr/bin/env python3
"""Destination host of the simulated traceroute path (runs inside the "far" namespace).

Answers ICMP echo requests sent to 172.31.3.2 with a reply whose payload carries the Mission 4 flag:
FLAG(M4)=<value>. The probe only reaches this host when its TTL is large enough (>= 4), so the
student gets the flag by finishing the traceroute.
"""
import os
import sys

from scapy.all import ICMP, IP, Raw, conf, send, sniff  # noqa: E402

conf.verb = 0
SECRETS = os.environ.get("LAB_SECRETS", "/opt/lab/secrets")
FAR = "172.31.3.2"


def secret(name):
    with open(os.path.join(SECRETS, name)) as fh:
        return fh.read().strip()


def handle(pkt):
    if IP in pkt and ICMP in pkt and pkt[IP].dst == FAR and pkt[ICMP].type == 8:
        icmp = pkt[ICMP]
        body = ("FLAG(M4)=%s" % secret("m4")).encode()
        send(IP(src=FAR, dst=pkt[IP].src) / ICMP(type=0, id=icmp.id, seq=icmp.seq) / Raw(body))


def main():
    print("far responder ready", flush=True)
    sniff(iface="lab-f3", filter="icmp", prn=handle, store=False)


if __name__ == "__main__":
    sys.exit(main())
