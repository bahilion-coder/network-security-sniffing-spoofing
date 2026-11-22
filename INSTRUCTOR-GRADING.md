# Instructor Grading and Validation

## Score allocation (20 points total)

| Mission | Platform / manual points | Grade /20 | Validation |
|---|---:|---:|---|
| 1. Scapy ICMP capture | 20 | 2.0 | Automated APG marker |
| 2. TCP/BPF filter | 25 | 2.5 | Automated APG marker |
| 3. ICMP packet construction | 25 | 2.5 | Manual source + PCAP rubric |
| 4. TTL/traceroute | 20 | 2.0 | Manual PCAP + explanation rubric |
| 5. Sniff and spoof reply | 25 | 2.5 | Manual request/reply PCAP + code |
| 6. C/libpcap sniffer | 30 | 3.0 | Automated APG marker |
| 7. Telnet inspection | 25 | 2.5 | Automated APG credential marker |
| 8. C raw socket packet | 30 | 3.0 | Manual source + PCAP rubric |
| **Total** | **200** | **20.0** |

Platform automated flags only cover Missions 1, 2, 6, and 7. Missions 3, 4, 5, and 8 are converted to informational levels because a flag alone cannot verify the required technical work. Instructor must award these mission points using the evidence rubric and the platform's score/export workflow. Confirm how manual score adjustments are supported in your deployment before release.

## Manual evidence rubric (per mission; 25 points except M4=20 and M8=30)

### Mission 3 (25)
- 5: source code is readable and uses the required packet layers
- 5: correct source/destination addresses
- 5: correct ICMP type and meaningful payload
- 5: PCAP demonstrates the packet was sent within the sandbox
- 5: explanation of header/checksum observations

### Mission 4 (20)
- 5: correct TTL-limited probes and target within lab
- 5: PCAP evidence of probes and responses (or a clearly documented network limitation)
- 5: compares results across TTL values
- 5: explains TTL and Time Exceeded behavior

### Mission 5 (25)
- 5: captures and inspects the controlled request
- 5: preserves required ICMP fields
- 5: constructs a reply correctly
- 5: PCAP shows request and reply
- 5: explains matching identifier/sequence and payload

### Mission 8 (30)
- 5: correct raw-socket creation and error handling
- 5: correctly constructed IPv4 header
- 5: correctly constructed ICMP header
- 5: correct byte order and length handling
- 5: PCAP verifies the transmitted packet
- 5: explanation of checksum/kernel behavior

## Evidence submission
Students submit a folder or archive containing mission-numbered source files, PCAPs, screenshots if required, and short explanations. Use a consistent naming format such as `M3_packet.py`, `M3_capture.pcap`, and `M3_report.txt`.

## Deployment gate
Do not release to students until a test instructor has deployed one sandbox, completed every mission, verified the four manual-evidence missions can be performed, confirmed the automated flags are sandbox-specific, and tested score/hint behavior. Manual score-adjustment capability must be confirmed in the actual platform.
