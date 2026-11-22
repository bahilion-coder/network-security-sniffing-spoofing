#!/usr/bin/env python3
"""Server responder (the kernel ignores ICMP echo requests, this process decides).

ICMP echo request to the server (10.1.26.12):
  * from the attacker's real address, correctly built raw packet (Mission 8)  -> reply FLAG(M8)=...
  * from the attacker / client otherwise                                        -> normal echo reply
  * source address outside 10.1.26.0/24 (Mission 3, forged address)             -> reply FLAG(M3)=...

Mission 8 packet: src 10.1.26.10, ICMP echo request, IP identification 0x1337 (4919), payload
starting with "NETSEC", valid IP and ICMP checksums.
The reply goes to the packet's source address and the server mirrors its traffic to the attacker,
so the flag is visible only if the packet really was accepted.
"""
import ipaddress
import os
import socket
import subprocess
import sys

from scapy.all import ICMP, IP, Raw, conf, sniff  # noqa: E402

conf.verb = 0
SECRETS = os.environ.get("LAB_SECRETS", "/opt/lab/secrets")
ATTACKER, CLIENT, SERVER = "10.1.26.10", "10.1.26.11", "10.1.26.12"
LAN = ipaddress.ip_network("10.1.26.0/24")


def send(pkt):
    """Send through the kernel IP stack so that the mirroring rule of lab-net (iptables TEE)
    also copies the reply to the attacker (scapy's send() would bypass iptables)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    try:
        s.sendto(bytes(pkt), (pkt[IP].dst, 0))
    finally:
        s.close()


def secret(name):
    with open(os.path.join(SECRETS, name)) as fh:
        return fh.read().strip()


def lab_iface():
    out = subprocess.check_output(["ip", "-o", "-4", "addr", "show"], text=True)
    for line in out.splitlines():
        fields = line.split()
        if fields[3].startswith(SERVER + "/"):
            return fields[1]
    raise RuntimeError("lab interface not found")


def checksums_ok(ip):
    raw = bytes(ip)
    a = IP(raw)
    b = IP(raw)
    del b.chksum
    del b[ICMP].chksum
    b = IP(bytes(b))
    return a.chksum == b.chksum and a[ICMP].chksum == b[ICMP].chksum


def mission8_packet(ip, data):
    return (ip.src == ATTACKER and ip.id == 0x1337 and data.startswith(b"NETSEC")
            and checksums_ok(ip))


def handle(pkt):
    if IP not in pkt or ICMP not in pkt or pkt[IP].dst != SERVER or pkt[ICMP].type != 8:
        return
    ip, icmp = pkt[IP], pkt[ICMP]
    data = bytes(icmp.payload)
    src = ip.src
    if mission8_packet(ip, data):
        out = ("FLAG(M8)=%s" % secret("m8")).encode()
    elif src in (ATTACKER, CLIENT):
        out = data
    elif ipaddress.ip_address(src) not in LAN:
        out = ("FLAG(M3)=%s" % secret("m3")).encode()
    else:
        return
    send(IP(src=SERVER, dst=src) / ICMP(type=0, id=icmp.id, seq=icmp.seq) / Raw(out))


def main():
    iface = lab_iface()
    print("responder listening on", iface, flush=True)
    sniff(iface=iface, filter="icmp", prn=handle, store=False)


if __name__ == "__main__":
    sys.exit(main())
