# Corrected draft v3 — review notes

Changes from v2:
- Missions 3, 4, 5, and 8 no longer use ungrounded APG flags; they are instructor-reviewed evidence missions (INFO_LEVEL) with rubrics in `INSTRUCTOR-GRADING.md`.
- Mission 4 now uses an isolated lab target (`10.9.0.7`) rather than depending on an external traceroute target.
- Mission 5's traffic generator sends a generic controlled request marker, not a student answer token.
- Removed unused APG variables and private token-file provisioning for Missions 3, 4, 5, and 8.
- Added an instructor scoring rubric and evidence-submission guide.

Still not deployment-tested: exact OpenStack image IDs, management usernames, flavors, topology provisioning, APG integration, SSH access, Telnet behavior, traffic capture, and manual score-adjustment workflow. The four manual-evidence levels require instructor grading; confirm the platform workflow for recording those points before student release.
