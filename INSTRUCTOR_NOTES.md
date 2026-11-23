# Instructor notes

Topology, accounts, image names and playbook layout follow the `seed-bof-lab` sandbox that is known to deploy without errors (image `seed`, mgmt_user `ubuntu`, SEED login `seed` / `dees`, network `lab-switch` 10.1.26.0/24, `groups: []`).

## How the per-student uniqueness works

`variables.yml` declares 8 APG variables of type `text` (one per mission flag). The platform generates new values for every sandbox; they are injected into Ansible under the same name and written into root-only files (`/opt/lab/secrets/*`) on the machine that emits the flag. `training.json` levels use `variant_answers: true` and `answer_variable_name`. The student submits only the value found after `FLAG(Mx)=`.

## 1. Topology (lab-switch 10.1.26.0/24, attacker, client and server m1.medium, router standard.small (as in seed-bof-lab))

| Node | Address | Image | Student access |
|---|---|---|---|
| attacker | 10.1.26.10 | SEED Ubuntu 20.04 | yes (account `seed` / `dees`, sudo) |
| client | 10.1.26.11 | SEED Ubuntu (image `seed`) | only `lab-trigger <id>` (SSH forced command) |
| server | 10.1.26.12 | SEED Ubuntu (image `seed`) | none (packets only) |
| router | 10.1.26.1 | Debian 12 | none; gateway + simulated path 172.31.0.0/16 |

The router also hosts three network namespaces (hop2 172.31.1.2, hop3 172.31.2.2, far 172.31.3.2) that make a 4-hop path for the traceroute mission.

## 2. Missions (all auto-graded, one APG flag each)

| # | Mission | Points | Hints (penalty) | How the flag is released |
|---|---|---:|---|---|
| 1 | Sniff ICMP (Scapy) | 20 | 5, 10 | payload of echo requests addressed to the attacker; decoy goes to the server |
| 2 | BPF filter, TCP port 40444 | 25 | 5, 10, 10 | TCP stream; decoys: TCP 40443, UDP 40444 |
| 3 | Spoof an ICMP echo request | 25 | 5, 10, 10 | server replies with the flag only to a forged source outside 10.1.26.0/24; reply is mirrored to the attacker |
| 4 | Traceroute | 20 | 5, 10 | echo reply of 172.31.3.2 (hop 4) |
| 5 | Sniff then spoof | 25 | 5, 10, 10 | `lab-trigger m5` prints the flag when forged replies answer the pings of a non-existing Internet host and 8.8.8.8 |
| 6 | C sniffer with libpcap | 30 | 5, 10, 15 | UDP payload to port 40445; decoys: port 40446, other destination |
| 7 | Telnet eavesdropping | 25 | 5, 10, 10 | password of `labuser` in a plain-text login (a `guest` login is a decoy) |
| 8 | C raw sockets | 30 | 5, 10, 15 | server replies only to a correct packet (src 10.1.26.10, ICMP echo, IP id 0x1337, payload `NETSEC…`, valid IP+ICMP checksums) |
| | **Total** | **200** | | |

## 3. Scoring

The platform stores integers: 200 points = 20/20, grade = points / 10. Hint penalties are 5 and 10 points (0.5 and 1.0), and a third hint costs 20 points capped at *mission points − 15* (so the three hints of a mission never cost more than the mission: 10 or 15 for 25- and 30-point missions). Missions worth 20 points have two hints. The solution costs the whole mission. The score cannot go below zero by construction.
The concept questions of the SEED handout (report) are supplementary and not part of the 20 points.

## 4. Flags and anti-cheating

* `variables.yml` declares 8 password variables; the platform generates new values for every sandbox (`variant_sandboxes: true`, `variant_answers: true`).
* Ansible writes each value into a root-only file (`/opt/lab/secrets`) on the machine that emits it, and never into source code or a shell command line.
* Students cannot log in to client/server/router. The only door is the forced command `lab-trigger <id>` (whitelist inside `gen.py`); the key on the attacker is useless for anything else, so the student having root on the attacker exposes no secret.
* Spoofing and raw-socket missions are checked by the lab itself (the flag is only released if the forged packet was accepted), so a screenshot or a copied flag proves nothing.
* Decoy streams carry look-alike values that are wrong.

## 5. Mirroring

A virtual switch does not show a machine the unicast traffic of other machines. `client` and `server` therefore copy every packet they send on the lab LAN to the attacker (`iptables -t mangle … -j TEE --gateway 10.1.26.10`), as a SPAN port would. Scripts send through the kernel stack (scapy's own `send()` bypasses iptables).

## 6. Report questions (not graded in the 20 points)

1. Where does a sniffer's BPF filter run, and why is it set before the callback?
2. Why does sniffing in promiscuous mode need root?
3. Why can a forged source address be used in an ICMP echo request, and what stops the reply from reaching the attacker in the normal case?
4. How many hops did your traceroute find, and why does TTL=1 give a reply from the router?
5. What is the difference between sniffing and spoofing, and why are the two combined in Mission 5?
6. Explain byte order and the Internet checksum (Mission 8).

## 7. Reference solutions (short)

1. `sudo python3 -c "from scapy.all import *; sniff(iface='<iface>', filter='icmp and dst host 10.1.26.10', prn=lambda p: p.show())"` then `lab-trigger m1`.
2. Filter `tcp dst port 40444`, then `lab-trigger m2`.
3. `send(IP(src='203.0.113.50', dst='10.1.26.12')/ICMP())` while sniffing `icmp and src host 10.1.26.12`.
4. Loop TTL 1..9 with `sr1(IP(dst='172.31.3.2', ttl=t)/ICMP())`; hop 4 answers with the flag.
5. Sniff echo requests from 10.1.26.11 and send forged replies (swap addresses, type 0, copy id/seq/payload); then `lab-trigger m5`.
6. libpcap program with filter `udp dst port 40445`; then `lab-trigger m6`.
7. Capture TCP port 23; password following the user name `labuser`; `lab-trigger m7`.
8. C raw socket: IP id 0x1337, ICMP echo request, payload `NETSEC...`, valid checksums, src 10.1.26.10, dst 10.1.26.12.

## 8. To confirm on the first real deployment

- The cloud must allow the attacker to send other source addresses (Missions 3 and 5).
- The SEED Ubuntu kernel on client and server must support `iptables -j TEE` (traffic mirroring).
- The platform should stop a score at zero (penalties are already capped by mission points).
- The access level text uses `seed` / `dees` as in the playbook.

Tested locally with network namespaces (virtual copy of the lab, the real provisioning scripts, Python and C reference solutions): all missions released the sandbox's own flag; malformed Mission 8 packets and Mission 5 without the spoofing program released nothing.
