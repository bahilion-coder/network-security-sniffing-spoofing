# Corrected draft v4 audit notes

Corrections addressing the audit feedback:
- Platform scoring is 100 points for automatic missions; manual evidence rubric is 100 points. The total academic grade is 20 points by instructor conversion, not a 200-point platform score.
- Automatic mission hint penalties changed to 2/4/6 platform points, below the smallest automatic mission value. Confirm score floors and cumulative behavior on the platform.
- Mission 4 replaced traceroute to a same-subnet destination with ARP/local-path analysis, because the router is not in that path.
- Client-side UDP marker file removed; the marker is generated only in a packet.
- Client SSH and stored trigger passwords removed. A fixed-action HTTP trigger service replaces SSH command execution; it accepts only five predefined POST actions and no arbitrary commands.
- Student account receives root on the isolated attacker VM for Scapy, tcpdump, libpcap and raw-socket exercises. This does not expose client credentials because no SSH credential is stored on attacker.
- All four machines use m1.medium per requirement; resource capacity for 30 students (up to 120 VMs) must be confirmed.
- APG values are serialized as JSON/Python-safe strings in templates.

Still not deployed or runtime-tested: image names/users, flavor availability, network setup, fixed trigger service, Telnet, mission completion, APG behavior, platform hint behavior, and instructor manual-score workflow.
