# Packet Sniffing and Spoofing Lab (CyberRangeCZ Platform)

A four-machine sandbox for [CyberRangeCZ Platform](https://docs.platform.cyberrange.cz/), adapting SEED Labs' *Packet Sniffing and Spoofing Lab* (W. Du, Syracuse University) into a graded, per-student exercise. Same structure as the `library-junior-hacker` example and the `seed-bof-lab` sandbox (`topology.yml` + `training.json` + `variables.yml` + Ansible `provisioning/`).

## Game levels summary

1. Sniff ICMP packets with Scapy
2. Filter TCP traffic with BPF (port 40444)
3. Spoof an ICMP echo request (forged source address)
4. Write a traceroute (simulated 4-hop path)
5. Sniff and then spoof (fake replies for non-existing hosts)
6. Write a C sniffer with libpcap
7. Eavesdrop on a Telnet login
8. Build an ICMP packet with C raw sockets

All eight levels are auto-graded: 200 platform points = 20/20 (grade = points / 10).

## Topology summary

| Host | Image | mgmt_user | Flavor | Address |
|---|---|---|---|---|
| attacker | seed | ubuntu | m1.medium | 10.1.26.10 |
| client | seed | ubuntu | m1.medium | 10.1.26.11 |
| server | seed | ubuntu | m1.medium | 10.1.26.12 |
| router | debian-12-x86_64 | debian | standard.small | 10.1.26.1 |

Network `lab-switch` 10.1.26.0/24. The student works only on `attacker` (login `seed` / `dees`); `lab-trigger <id>` asks the client to generate traffic.

## Why every sandbox is different

APG (see `variables.yml`): 8 `text` variables, one flag per mission, generated per sandbox and checked with `variant_answers`.

See `INSTRUCTOR_NOTES.md` for scoring, hints, anti-cheating design and items to confirm on first deployment.
