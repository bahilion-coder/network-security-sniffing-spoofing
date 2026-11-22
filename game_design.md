# Game Design — Network Security: Packet Sniffing and Spoofing (v4)

## 1. Scenario overview

Students act as junior network security analysts investigating controlled traffic in an isolated lab. They use a SEED Ubuntu workstation to capture and filter packets, construct ICMP packets, investigate ARP and local-path behavior, demonstrate sniff-and-spoof, write a C/libpcap sniffer, inspect Telnet plaintext, and construct an IPv4 packet using C raw sockets.

Adapted from the SEED Labs *Packet Sniffing and Spoofing Lab* and structured using the CyberRangeCZ Library Junior scenario template.

## 2. Learning objectives

Students should be able to:
1. Identify interfaces, IPv4 addresses, routes and hosts.
2. Capture packets using Scapy and BPF filters.
3. Explain root privileges and packet-capture permissions.
4. Construct and inspect ICMP packets in the isolated network.
5. Understand ARP and why same-subnet traffic bypasses the router.
6. Demonstrate sniff-and-spoof in a controlled lab.
7. Implement a packet sniffer using C/libpcap.
8. Explain why Telnet exposes credentials in plaintext.
9. Construct IPv4 packets with C raw sockets and understand byte order/checksums.

## 3. Topology

| Node | Role | Address | Image | Flavor |
|---|---|---|---|---|
| attacker | Student workstation | 10.9.0.5 | SEED Ubuntu 20.04 (custom image) | m1.medium |
| client | Fixed-action traffic generator | 10.9.0.6 | Debian 12 | m1.medium |
| server | Target host | 10.9.0.7 | Debian 12 | m1.medium |
| router | Gateway/egress | 10.9.0.1 | Debian 12 | m1.medium |

All hosts are on `10.9.0.0/24`. The attacker, client, and server are on the same subnet; the router is not an intermediate hop for attacker-to-server or client-to-attacker traffic. Therefore, Mission 4 investigates ARP/local path rather than relying on traceroute to a same-subnet destination.

**Cloud prerequisites:** verify the SEED image identifier `seed-ubuntu-20.04`, management user `seed`, Debian 12 image and management user, and availability of `m1.medium`. All four nodes use `m1.medium` as requested. For 30 students, the topology may require up to 120 VMs; confirm capacity.

## 4. Client traffic generation and privilege model

The client has no student SSH account and no SSH credential is stored on attacker. A root-owned HTTP service listens only on `10.9.0.6:8080` and accepts five fixed POST actions: `/icmp`, `/tcp`, `/udp`, `/telnet`, `/spoof-test`. It accepts no shell command, arbitrary input, or payload argument. Attacker-side wrappers call these endpoints.

Students have root privileges on the isolated attacker VM only, because packet capture, Scapy and raw sockets require elevated privileges. This grants control of their own attacker workstation, but the client/server credentials and answer files are not stored there. The trigger endpoint must remain isolated from any external network.

## 5. Mission flow

| Mission | Activity | Assessment | Points |
|---|---|---|---:|
| 1 | Scapy ICMP capture | APG marker | 2/20 |
| 2 | TCP/BPF filtering | APG marker | 2.5/20 |
| 3 | Construct an ICMP packet | Manual source + PCAP | 2.5/20 |
| 4 | ARP and same-subnet path investigation | Manual capture + explanation | 2/20 |
| 5 | Sniff and spoof ICMP reply | Manual source + PCAP | 2.5/20 |
| 6 | C/libpcap sniffer | APG marker | 3/20 |
| 7 | Telnet plaintext investigation | APG marker | 2.5/20 |
| 8 | C raw-socket packet | Manual source + PCAP | 3/20 |
| **Total** | | | **20/20** |

Automatic missions (M1, M2, M6, M7) total 100 platform points = 10 academic points. Manual missions (M3, M4, M5, M8) total 100 rubric points = 10 academic points. Final grade is `(platform points + manual rubric points) / 10`. Manual evidence points are not automatically awarded by the platform; verify the instructor workflow before release.

Automatic hints have penalties 2, 4, and 6 platform points (0.2, 0.4, and 0.6 academic points). Confirm cumulative behavior and score floor in the platform.

## 6. APG variables

Four APG variables are used for the automatic missions: `flag_m1_icmp`, `flag_m2_tcp`, `flag_m6_pcap`, and `flag_m7_telnet`. They are injected into fixed traffic payloads or the Telnet test password. Templates use base64 encoding before insertion into Python strings. No answer files are created on the client.

## 7. Instructor validation

- Confirm images, management usernames, and flavor availability.
- Deploy one sandbox and verify all provisioning.
- Verify the client trigger service is bound to the lab IP and each fixed action works.
- Verify markers are visible in captures and APG answers validate.
- Verify Telnet daemon and plaintext test session.
- Verify Scapy, tcpdump, tshark/Wireshark, GCC, and libpcap.
- Verify all manual missions can be performed and graded.
- Deploy two sandboxes and confirm automatic answers differ and validate independently.
- Confirm hint and manual-score workflow.

## 8. Supplementary report questions

1. Describe essential libpcap calls in a sniffer.
2. Why are elevated privileges required for packet capture?
3. Explain promiscuous vs non-promiscuous capture in switched virtual networks.
4. Can IPv4 total length be set independently of transmitted buffer length? Explain observed behavior.
5. For `IPPROTO_RAW`, what checksum work does the kernel perform, and what must the programmer calculate in other raw-socket modes?
6. Why do raw sockets require elevated privileges, and which system call reports failure?

These questions are supplementary and do not add points to the practical score.

## 9. Safety boundary

All packet generation and spoofing must remain inside the isolated lab subnet. Do not target public systems, capture third-party credentials, or perform actions outside the sandbox.
