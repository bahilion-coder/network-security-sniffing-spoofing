#!/usr/bin/env python3
"""Services the client talks to on the attacker (no secret is stored here).

  TCP 23     fake Telnet server (prompts for login / password and always refuses)
  TCP 40443  TCP listener (decoy port of Mission 2)
  TCP 40444  TCP listener (real port of Mission 2)
"""
import socket
import threading


def telnet(conn):
    try:
        conn.settimeout(5)
        conn.sendall(b"Lab telnetd\r\nlogin: ")
        conn.recv(256)
        conn.sendall(b"Password: ")
        conn.recv(256)
        conn.sendall(b"\r\nLogin incorrect\r\n")
    except OSError:
        pass
    finally:
        conn.close()


def plain(conn):
    try:
        conn.settimeout(3)
        conn.recv(1024)
        conn.sendall(b"ACK\r\n")
    except OSError:
        pass
    finally:
        conn.close()


def serve(port, handler):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))
    srv.listen(16)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handler, args=(conn,), daemon=True).start()


def main():
    for port, handler in ((23, telnet), (40443, plain), (40444, plain)):
        threading.Thread(target=serve, args=(port, handler), daemon=True).start()
    threading.Event().wait()


if __name__ == "__main__":
    main()
