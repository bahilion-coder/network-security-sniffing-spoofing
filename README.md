# Network Security: Packet Sniffing and Spoofing — v4 corrected draft

CyberRangeCZ training scenario adapted from SEED Labs Packet Sniffing and Spoofing Lab. **This package is not runtime-tested or ready for student release.**

## Structure

- `topology.yml`: attacker, client, server, router and network.
- `variables.yml`: APG values for the four automatically validated missions.
- `training.json`: missions, answers, hints and content.
- `game_design.md`: scenario design, mission flow and learning objectives.
- `INSTRUCTOR-GRADING.md`: manual rubric and score conversion.
- `provisioning/`: Ansible provisioning.

## Required OpenStack checks

1. Replace/check the SEED image identifier `seed-ubuntu-20.04` and management user `seed`.
2. Confirm Debian 12 image name and management user.
3. Confirm `m1.medium` exists. All four VMs use `m1.medium` as requested.
4. Capacity warning: 30 students may create as many as 120 VMs. Check resource capacity before scaling.
5. Confirm provisioning can reach package repositories.
6. Confirm CyberRangeCZ's APG injection and answer validation work with the four variable names.

## Student access and privileges

The intended entry point is the attacker/SEED VM. The account `user` is password-locked; access is through the platform's approved console/SSH access mechanism. The account receives passwordless sudo **on the isolated attacker VM only** so students can use Scapy, tcpdump, libpcap and raw sockets. No SSH password or private client credential is stored on the attacker.

The client has no student SSH account. It runs a root-owned fixed-action HTTP trigger service bound to `10.9.0.6:8080`. The service accepts only five fixed POST paths: `/icmp`, `/tcp`, `/udp`, `/telnet`, and `/spoof-test`; it does not accept commands, arbitrary payloads, or shell arguments. The attacker wrappers call these fixed endpoints. This service is intended only for the isolated lab network and must not be exposed outside it.

Trigger scripts on attacker:

```bash
/opt/netsec-lab/trigger-client-icmp.sh
/opt/netsec-lab/trigger-client-tcp.sh
/opt/netsec-lab/trigger-client-udp.sh
/opt/netsec-lab/trigger-client-telnet.sh
/opt/netsec-lab/trigger-client-spoof-test.sh
```

## Scoring

- Automatic missions M1, M2, M6 and M7: **100 platform points total = 10 academic points**.
- Manual evidence missions M3, M4, M5 and M8: **100 instructor rubric points total = 10 academic points**.
- Final academic grade: `(platform score + manual rubric score) / 10`, maximum 20.
- Automatic mission hint penalties: 2, 4 and 6 platform points (0.2, 0.4 and 0.6 academic points). Their cumulative sum is below each automatic mission's base score. Confirm the platform's hint accumulation and score-floor behavior.
- Do not claim the platform automatically scores 200 points. Manual evidence points require instructor workflow, which must be confirmed in the actual deployment.

## Mission 4 correction

Mission 4 is an ARP and same-subnet path investigation. It no longer asks students to traceroute to a same-subnet server through a router that is not on the path.

## Licensing and attribution

See `ATTRIBUTION.txt`, the included license files, and `LICENSE`. The combined package contains materials with different licensing conditions; do not represent the entire package as MIT-only.

## Deployment gate

Before release, deploy one test sandbox and verify provisioning, images/users/flavors, all five client trigger endpoints, automatic marker validation, Telnet startup, Scapy, tcpdump/tshark/Wireshark, GCC/libpcap, all manual missions, hint behavior, APG uniqueness across two sandboxes, and the instructor manual-scoring workflow. Do not distribute to 30 students until these checks pass.
