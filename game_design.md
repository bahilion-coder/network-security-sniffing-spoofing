# Game Design – Network Security: Packet Sniffing and Spoofing

## 1. Scenario overview

Students act as junior network security analysts investigating traffic in an isolated network. They use the SEED Ubuntu 20.04 workstation to inspect packets, build Scapy programs, write a libpcap sniffer, analyze an intentionally insecure Telnet exchange, and construct a packet using C raw sockets.

The scenario is adapted from the SEED Labs *Packet Sniffing and Spoofing Lab* (Wenliang Du, 2006–2020) and uses the Library Junior CyberRangeCZ scenario as its structural template.

## 2. Learning objectives

By the end of the exercise, students should be able to:

1. Identify interfaces, addresses, routes and hosts in a small IPv4 network.
2. Capture packets using Scapy and BPF filters.
3. Explain the effect of root privileges on packet capture and raw sockets.
4. Construct ICMP packets and verify packet fields.
5. Explain TTL-based traceroute and ICMP Time Exceeded messages.
6. Combine sniffing and spoofing in a controlled ICMP demonstration.
7. Implement a basic packet sniffer using C and libpcap.
8. Explain why Telnet exposes credentials in plaintext.
9. Construct and send an IPv4 packet using C raw sockets and understand byte order.

## 3. Topology

| Node | Role | Address | Image | Flavor |
|---|---|---:|---|---|
| attacker | Student workstation | 10.9.0.5 | SEED Ubuntu 20.04 (custom image) | m1.medium |
| client | Controlled traffic generator | 10.9.0.6 | Debian 12 | standard.small |
| server | HTTP token target | 10.9.0.7 | Debian 12 | standard.small |
| router | Default gateway / Internet egress | 10.9.0.1 | Debian 12 | standard.small |

All nodes are connected to `10.9.0.0/24`. The student works on the attacker. Client-side scripts generate controlled traffic. The target server publishes mission-specific tokens over HTTP. Outbound Internet access is used for the traceroute observation, but no mission flag depends on an external service.

**Deployment configuration:** `seed-ubuntu-20.04` is a proposed OpenStack image identifier and must be replaced with the exact image name registered in the target cloud if different. The management user is set to `seed`, which must match the image's sudo-capable management account. Confirm that `m1.medium` and `standard.small` exist in the target OpenStack environment.

## 4. Mission sequence and grading

The platform stores integer points (200 total). The displayed academic grade is calculated as `platform_points / 10`, giving a maximum of 20/20.

| Order | Mission | Platform points | Grade equivalent |
|---:|---|---:|---:|
| 1 | Scapy ICMP capture | 20 | 2.0 |
| 2 | TCP/BPF filtering | 25 | 2.5 |
| 3 | ICMP packet construction and spoofing | 25 | 2.5 |
| 4 | TTL and traceroute investigation | 20 | 2.0 |
| 5 | Sniff and spoof an ICMP reply | 25 | 2.5 |
| 6 | C/libpcap sniffer | 30 | 3.0 |
| 7 | Telnet traffic inspection | 25 | 2.5 |
| 8 | C raw sockets | 30 | 3.0 |
| **Total** | | **200** | **20.0** |

Each mission has three progressive hints. The intended penalties are 0.5, 1.0 and 2.0 academic points, represented internally as 5, 10 and 20 integer platform points. Penalties should be cumulative if the platform applies each requested hint cumulatively. The final score cannot fall below zero.

## 5. Automatic Problem Generation

The sandbox definition includes `variables.yml` with eight generated password-type values. Each training level enables Variant Answers and references the corresponding variable name. The same generated values are inserted during Ansible provisioning into the controlled traffic payloads, Telnet login, or server token files.

This provides one unique answer set per sandbox without maintaining 30 separate ZIP archives. CyberRangeCZ must be configured to generate variant sandboxes for the training instance. The exact APG behavior must be verified in a test pool before assigning students.

## 6. Traffic generation and visibility

Traffic is intentionally sent to the attacker interface so that it is observable without depending on promiscuous-mode visibility of unrelated unicast traffic on a virtual switch. The client helper scripts are root-owned and only specific commands are allowed through sudo. They generate ICMP, TCP, UDP and Telnet traffic with sandbox-specific markers.

The attacker is configured to ignore kernel ICMP Echo Requests so that students can demonstrate a user-space Scapy Echo Reply in Mission 5. Restore the normal setting after the exercise if the image is reused outside this scenario.

## 7. Instructor validation checklist

Before opening the training to students:

- Confirm the SEED image identifier and management user in OpenStack.
- Confirm `m1.medium` and `standard.small` are available.
- Deploy one sandbox and verify all Ansible roles complete successfully.
- Confirm the attacker can reach `10.9.0.6`, `10.9.0.7` and the Internet.
- Run all five `/opt/netsec-lab/trigger-client-*.sh` scripts from the attacker.
- Confirm Scapy/tcpdump can capture the generated ICMP, TCP, UDP and Telnet traffic.
- Confirm the server token URLs return the expected sandbox-specific values.
- Confirm the Telnet service is listening on TCP/23 and the test login is visible in a packet capture.
- Confirm libpcap headers and `gcc -lpcap` are available.
- Deploy two APG sandboxes and confirm that all eight flag values differ and validate independently.
- Confirm the platform accepts integer hint penalties and the instructor applies the /10 grade conversion.

## 8. Written report questions

The following conceptual questions are supplementary and do not add points to the 20-point practical grade:

1. Describe the essential library calls in a libpcap sniffer.
2. Why are elevated privileges required for packet capture, and where does an unprivileged program fail?
3. Explain the difference between promiscuous and non-promiscuous capture in a switched virtual network.
4. Can the IPv4 total-length field be set independently of the actual transmitted buffer length? Explain the observed behavior.
5. For `IPPROTO_RAW`, what checksum work is performed by the kernel and what must the programmer calculate for other raw-socket modes?
6. Why do raw sockets require elevated privileges, and which system call reports the failure?

Students submit screenshots, source code, and explanations of observations. Merely attaching code without explanation is insufficient.

## 9. Safety boundary

All packet generation and spoofing must remain inside the isolated lab subnet. The exercise does not ask students to spoof traffic toward public Internet hosts, capture third-party credentials, or attack systems outside their sandbox.
