#!/usr/bin/env python3
"""Client traffic generator.

Run as root through the "labtrigger" SSH forced command (see lab-gen-wrapper): the student only
types   lab-trigger <id>   on the attacker. Secrets are read from /opt/lab/secrets (written by
Ansible from the APG variables of the sandbox).

    gen.py list | <id> | noise

Payloads look like  FLAG(<mission>)=<value>.  Decoy streams use the same look with a wrong value,
so only the right filter / the right reasoning finds the real flag.
"""
import hashlib
import os
import re
import socket
import subprocess
import sys
import time

from scapy.all import ICMP, IP, Raw, conf  # noqa: E402

conf.verb = 0
SECRETS = os.environ.get("LAB_SECRETS", "/opt/lab/secrets")
ATTACKER, CLIENT, SERVER = "10.1.26.10", "10.1.26.11", "10.1.26.12"


def send(pkt):
    """Send through the kernel IP stack (scapy's own send() uses an AF_PACKET socket, which
    bypasses iptables, so the traffic mirroring rule of lab-net would never see the packet)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    try:
        s.sendto(bytes(pkt), (pkt[IP].dst, 0))
    finally:
        s.close()


def secret(name):
    with open(os.path.join(SECRETS, name)) as fh:
        return fh.read().strip()


def decoy(tag):
    """Deterministic fake token with the same length as the real flags (never a real flag)."""
    size = len(secret("m1"))
    return (hashlib.sha256((secret("m1") + ":" + tag).encode()).hexdigest() * 4)[:size]


def tagged(mission, value):
    return ("FLAG(%s)=%s" % (mission, value)).encode()


def tcp_send(dst, port, data, wait=0.4):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((dst, port))
        s.sendall(data)
        time.sleep(wait)
        try:
            s.recv(256)
        except OSError:
            pass
    except OSError as exc:
        print("  (tcp to %s:%d failed: %s)" % (dst, port, exc))
    finally:
        s.close()


def udp_send(dst, port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto(data, (dst, port))
    finally:
        s.close()


def icmp_send(dst, data, count=3):
    for _ in range(count):
        send(IP(dst=dst) / ICMP() / Raw(data))
        time.sleep(0.5)


def telnet_login(user, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    try:
        s.connect((ATTACKER, 23))
        s.recv(256)
        s.sendall(user.encode() + b"\r\n")
        s.recv(256)
        time.sleep(0.3)
        s.sendall(password.encode() + b"\r\n")
        s.recv(256)
    except OSError as exc:
        print("  (telnet failed: %s)" % exc)
    finally:
        s.close()


def s_m1():
    icmp_send(ATTACKER, tagged("M1", secret("m1")))               # real: addressed to the attacker
    icmp_send(SERVER, tagged("M1", decoy("icmp-server")), 2)      # decoy: another destination
    print("Mission 1 traffic sent (ICMP echo requests).")


def s_m2():
    tcp_send(ATTACKER, 40444, tagged("M2", secret("m2")))         # real: TCP, destination port 40444
    tcp_send(ATTACKER, 40443, tagged("M2", decoy("tcp-other-port")))
    udp_send(ATTACKER, 40444, tagged("M2", decoy("udp-same-port")))
    print("Mission 2 traffic sent (TCP/UDP towards the attacker).")


def s_m6():
    udp_send(ATTACKER, 40445, tagged("M6", secret("m6")))         # real: UDP destination port 40445
    udp_send(ATTACKER, 40446, tagged("M6", decoy("udp-other-port")))
    udp_send(SERVER, 40445, tagged("M6", decoy("udp-other-dst")))
    print("Mission 6 traffic sent (UDP datagrams).")


def s_m7():
    telnet_login("guest", decoy("telnet-guest"))                  # decoy: other account
    time.sleep(0.5)
    telnet_login("labuser", secret("m7"))                         # real: password of "labuser"
    print("Mission 7 traffic sent (two Telnet logins towards the attacker).")


def ping_target(ip, count=3):
    out = subprocess.run(["ping", "-n", "-c", str(count), "-i", "0.5", "-W", "2", ip],
                         capture_output=True, text=True).stdout
    m = re.search(r"(\d+) received", out)
    return int(m.group(1)) if m else 0


def s_m5():
    print("The client is pinging three targets; your sniff-then-spoof program must answer them.")
    dead_inet, dead_lan, alive = "192.0.2.99", "10.1.26.99", "8.8.8.8"
    r1, r2, r3 = ping_target(dead_inet), ping_target(dead_lan), ping_target(alive)
    print("  ping %-12s non-existing host on the Internet : %d/3 replies" % (dead_inet, r1))
    print("  ping %-12s non-existing host on the LAN      : %d/3 replies" % (dead_lan, r2))
    print("  ping %-12s host on the Internet              : %d/3 replies" % (alive, r3))
    if r1 >= 1 and r3 >= 1:
        print("Your program answers pings for hosts that do not exist: well done.")
        print("FLAG(M5)=%s" % secret("m5"))
    else:
        print("Not yet: the non-existing Internet host and the Internet host must both answer.")


SCENARIOS = {
    "m1": (s_m1, "Mission 1  ICMP echo requests"),
    "m2": (s_m2, "Mission 2  TCP + UDP streams (find the TCP one to port 40444)"),
    "m5": (s_m5, "Mission 5  client pings 3 targets (needs your sniff-then-spoof program)"),
    "m6": (s_m6, "Mission 6  UDP datagrams (for your C sniffer)"),
    "m7": (s_m7, "Mission 7  Telnet logins"),
}


def noise():
    while True:
        try:
            send(IP(src=CLIENT, dst=SERVER) / ICMP() / Raw(b"lab-noise"))
        except Exception as exc:  # keep the service alive during network start-up
            print("noise: %s" % exc, file=sys.stderr)
        time.sleep(5)


def main():
    arg = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
    if arg == "noise":
        noise()
    elif arg in SCENARIOS:
        SCENARIOS[arg][0]()
    else:
        if arg and arg != "list":
            print("Unknown scenario: %r" % arg[:40])
        print("Usage: lab-trigger <id>\nAvailable scenarios:")
        for key, (_, desc) in SCENARIOS.items():
            print("  %-4s %s" % (key, desc))
        sys.exit(0 if arg in ("", "list") else 2)


if __name__ == "__main__":
    main()
