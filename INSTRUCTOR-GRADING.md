# Instructor Grading and Validation (v4)

## Score model (20 academic points)

- Platform-validated missions (M1, M2, M6, M7): 100 platform points total = 10 academic points.
- Instructor-reviewed evidence missions (M3, M4, M5, M8): 100 rubric points total = 10 academic points.
- Final grade: `(platform points + manual rubric points) / 10`, maximum 20.
- Hint penalties for auto levels are 2, 4, and 6 platform points (0.2, 0.4, 0.6 academic points), totaling at most 12 per auto mission. They cannot exceed the mission's base value. Confirm platform hint accumulation/floor behavior before release.
- This score model is external/manual for the evidence missions; do not claim the platform automatically totals 200. Confirm instructor score recording/export workflow.

| Mission | Automatic platform points | Manual rubric points |
|---|---:|---:|
| M1 Scapy ICMP | 20 | 0 |
| M2 TCP/BPF | 25 | 0 |
| M3 ICMP packet construction | 0 | 25 |
| M4 ARP/local-path investigation | 0 | 20 |
| M5 sniff and spoof | 0 | 25 |
| M6 C/libpcap | 30 | 0 |
| M7 Telnet | 25 | 0 |
| M8 C raw socket | 0 | 30 |
| **Total** | **100** | **100** |

## Evidence rubric

### M3 (25)
- 5: readable Scapy source
- 5: required packet source/destination fields
- 5: correct ICMP type and payload
- 5: PCAP proves packet sent only within lab
- 5: checksum/header explanation

### M4 (20) — ARP and same-subnet path (replaces traceroute)
- 5: interface, address, route and neighbor table evidence
- 5: ARP request/reply capture
- 5: ICMP capture to server and gateway comparison
- 5: explains same-subnet direct delivery and why router is not a hop

### M5 (25)
- 5: captures controlled request
- 5: preserves required ICMP fields
- 5: constructs reply correctly
- 5: PCAP shows request and student's reply
- 5: explains identifier, sequence and payload matching

### M8 (30)
- 5: raw socket creation/error handling
- 5: IPv4 header construction
- 5: ICMP header construction
- 5: byte order and length handling
- 5: PCAP verification
- 5: checksum/kernel behavior explanation

## Evidence submission
Submit mission-numbered source, PCAPs, screenshots where needed, and concise explanations.

## Deployment gate
Test one sandbox, all traffic endpoints, each automatic marker, all manual tasks, scoring/hint behavior, and two APG sandboxes before release. Manual score recording must be confirmed on the actual platform.
