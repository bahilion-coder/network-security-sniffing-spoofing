PACKET SNIFFING AND SPOOFING - quick reference
==============================================
Network 10.1.26.0/24:  attacker 10.1.26.10 (this machine)  client 10.1.26.11  server 10.1.26.12
                      router 10.1.26.1

  lab-iface              name of the lab network interface (sniff / send on this one)
  lab-trigger list       scenarios the client can run for you
  lab-trigger <id>       make the client generate the traffic of a mission (e.g. lab-trigger m1)

Rules
  * Sniffing and spoofing need root:  sudo python3 mycode.py
  * You work ONLY on this machine. client, server and router are "user machines": you reach
    them with packets, never with a shell.
  * Flags look like   FLAG(<mission>)=<value>   in the traffic.  Submit only <value>.
    Traffic that does not belong to the mission carries look-alike values that are WRONG.
  * Flags are different in every sandbox.
