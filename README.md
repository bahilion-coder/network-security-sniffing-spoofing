# Network Security: Packet Sniffing and Spoofing

A CyberRangeCZ linear training scenario based on the SEED Labs Packet Sniffing and Spoofing Lab. The scenario uses the Library Junior repository as its CyberRangeCZ structural template.

## Package contents

```text
network-security-sniffing-spoofing/
├── topology.yml
├── variables.yml
├── training.json
├── game_design.md
├── README.md
├── ATTRIBUTION.txt
├── LICENSE
└── provisioning/
    ├── playbook.yml
    ├── requirements.yml
    ├── host_vars/
    │   └── attacker.yml
    └── roles/
        ├── common/
        ├── attacker/
        ├── client/
        ├── server/
        └── router/
```

## Before importing

This is a scenario package prepared from the supplied template and TP. It is **not yet cloud-validated** because the exact OpenStack image identifier and available flavor catalog were not provided. Make these checks first:

1. In `topology.yml`, replace `seed-ubuntu-20.04` with the exact name of the imported SEED Ubuntu 20.04 image in your OpenStack catalog if it differs.
2. Confirm that the image's management account is `seed`. If the image uses another sudo-capable account, update `base_box.mgmt_user`.
3. Confirm the OpenStack flavors `m1.medium` and `standard.small` exist. The attacker uses `m1.medium`; the supporting machines use `standard.small` to avoid unnecessarily allocating four medium instances per student.
4. Confirm that the platform's provisioning environment can install packages from Ubuntu/Debian repositories. The scenario has outbound Internet access available for the traceroute observation, but no unique flag depends on Internet reachability.
5. Confirm that the platform's Ansible environment includes the `password_hash` filter (normally provided by Ansible's standard password/hash filters).

The topology currently uses the official SEED VM as the attacker image, Debian 12 for the client and server, and Debian 12 for the router. The `mgmt_user` values for the supporting images follow the known CyberRangeCZ Debian image convention.

## Import and APG configuration

1. Import the sandbox definition directory containing `topology.yml`, `variables.yml` and `provisioning/`.
2. Import `training.json` as a linear training definition.
3. Enable **Generate variant sandboxes** for the training definition / pool.
4. Ensure the training levels retain `variant_answers: true` and their `answer_variable_name` fields exactly match the keys in `variables.yml`.
5. Create a test pool with at least two sandboxes before assigning the training to students.
6. Confirm that generated values are injected into Ansible provisioning and are stored in the platform's answer storage.

The eight APG variables are password-type random values. They are placed into the corresponding lab traffic or token files by Ansible. Do not replace `answer_variable_name` with a literal flag.

## Student access

The intended student entry point is the `attacker` node. The local `user` account is password-locked; use the CyberRangeCZ-provided access mechanism or your instructor's approved credentials. Do not publish or reuse shared credentials. The client SSH password is generated per sandbox through APG and is used only by root-owned helper scripts.

The attacker provides these helper scripts:

```bash
sudo /opt/netsec-lab/trigger-client-icmp.sh
sudo /opt/netsec-lab/trigger-client-tcp.sh
sudo /opt/netsec-lab/trigger-client-udp.sh
sudo /opt/netsec-lab/trigger-client-telnet.sh
sudo /opt/netsec-lab/trigger-client-spoof-test.sh
```

The scripts connect to the client over SSH and invoke root-owned traffic generators. The client account `student` has narrowly scoped sudo permission for those generators, not unrestricted sudo access.

## Grading

The eight practical levels total **200 platform points**. The academic grade is `platform_points / 10`, so 200 points corresponds to 20/20. Each level has three hints with integer penalties of 5, 10 and 20 platform points, equivalent to 0.5, 1 and 2 academic points.

CyberRangeCZ's native score display may show the internal 200-point scale. If the platform does not support display scaling, instructors should export or record the platform score and divide by 10 when entering the academic grade. Do not claim that the UI automatically displays /20 unless this has been verified in your platform version.

## Validation status and known limitations

The JSON structure and YAML files are authored to follow the supplied Library Junior template and CyberRangeCZ sandbox/training conventions. The package has not been deployed against your OpenStack or CyberRangeCZ instance. In particular, verify:

- Exact image identifier and management username for the SEED image.
- Availability and names of the requested OpenStack flavors.
- APG variable injection into Ansible and answer storage.
- Whether the SEED image already contains desktop components and whether Wireshark can be launched through the GUI.
- Whether the image's package repositories still provide all named packages.
- Telnet daemon startup and port 23 reachability in the sandbox network.
- Whether the virtual network allows the intended packet capture and ICMP spoofing behavior.

The mission traffic is directed to the attacker interface to avoid relying on promiscuous-mode visibility of arbitrary switched unicast traffic. Mission 5 disables the attacker's kernel Echo Reply behavior so that the student program can demonstrate its own reply. This is a lab-specific setting.

## Source-derived exercise coverage

The exercise covers the source TP's Scapy sniffing and filtering, ICMP spoofing, traceroute, sniff-and-spoof, C/libpcap sniffer, BPF filters, Telnet credential inspection, and C raw sockets. The source TP's conceptual questions are included as supplementary report questions in `game_design.md`; they do not add to the practical 20-point score.

## Licensing and attribution

This scenario combines material under different licenses. See `ATTRIBUTION.txt` and `LICENSE` before redistribution. The Library Junior template's code and game-design terms are retained separately from SEED-derived educational material. SEED-derived adaptations remain under CC BY-NC-SA 4.0; do not relicense the entire combined package under MIT alone.

## Useful documentation

- CyberRangeCZ APG variables: https://docs.platform.cyberrange.cz/user-guide-advanced/sandboxes/apg-variables/
- CyberRangeCZ sandbox definition: https://docs.platform.cyberrange.cz/user-guide-advanced/sandboxes/sandbox-definition/
- CyberRangeCZ training overview / APG: https://docs.platform.cyberrange.cz/user-guide-advanced/trainings/trainings-overview/
- SEED Labs: https://seedsecuritylabs.org/labsetup.html


## Corrected draft security changes

- Removed the shared static student/client password from the scenario files.
- Locked the local attacker account password so the package does not advertise a reusable login password.
- Added an APG-generated per-sandbox client SSH password used by the root-owned traffic trigger scripts.
- Removed public HTTP flag/token files from the server web root. Validation values are now stored under `/opt/netsec-lab/flags` with root-only permissions.
- Updated Mission 3, 4, and 8 instructions to require practical evidence and removed direct `curl` token retrieval instructions.
- Added explicit evidence expectations (source code, PCAP, and short explanations) to reduce flag-only assessment bypasses.

## Important validation limitation

This corrected draft is **not deployment-ready yet**. Missions 3, 4, and 8 still use APG answer variables in the training definition, but their values are no longer exposed to students through the old public token URLs. The next engineering step is to implement a proper per-mission validation mechanism (e.g., server-side packet validation or evidence-based instructor grading) and verify the exact CyberRangeCZ training-definition schema. Also validate the SEED image identifier, management user, flavors, APG behavior, and provisioning on your platform before student release.

## Pre-deployment test checklist

1. Validate JSON/YAML syntax.
2. Deploy one sandbox only.
3. Verify attacker access through the platform.
4. Verify Scapy, GCC, libpcap, tcpdump, tshark/Wireshark, and Telnet packages.
5. Verify client helper triggers work with the per-sandbox SSH credential.
6. Verify the Telnet service and capture.
7. Complete all missions and check score/hint behavior.
8. Deploy a second sandbox and verify generated APG values differ.
9. Do not scale to a 30-student class until resource capacity and all tests pass.


## Important validation/security notes (v3)
- The attacker-side trigger scripts are root-owned and mode `0700`; students invoke them through narrowly scoped sudo permissions. This prevents reading the embedded per-sandbox SSH credential from the trigger scripts.
- Missions 3, 4, 5, and 8 are instructor-reviewed evidence missions, not auto-flag levels. See `INSTRUCTOR-GRADING.md`. Confirm the platform's manual score workflow before release.
- Mission 4 uses only the isolated lab target, not an Internet destination.
- Do not deploy until image IDs, management usernames, flavors, access method, and all provisioning/runtime behavior are verified.
