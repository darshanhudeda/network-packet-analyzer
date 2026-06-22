import sys
import importlib
import subprocess
import os

REQUIRED_PYTHON = (3, 10)

REQUIRED_PACKAGES = [
    "scapy",
    "pyshark",
    "dash",
    "plotly",
    "pandas",
    "colorama",
]

def check_python():
    print("\n[*] Checking Python version...")
    v = sys.version_info
    if v >= REQUIRED_PYTHON:
        print(f"    ✓ Python {v.major}.{v.minor}.{v.micro} — OK")
        return True
    else:
        print(f"    ✗ Need Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+")
        return False

def check_packages():
    print("\n[*] Checking required packages...")
    all_ok = True
    for pkg in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(pkg)
            ver = getattr(mod, "__version__", "installed")
            print(f"    ✓ {pkg} {ver} — OK")
        except ImportError:
            print(f"    ✗ {pkg} — NOT INSTALLED")
            all_ok = False
    return all_ok

def check_tshark():
    print("\n[*] Checking tshark...")
    try:
        result = subprocess.run(
            ["tshark", "--version"],
            capture_output=True, text=True
        )
        first_line = result.stdout.split("\n")[0]
        print(f"    ✓ {first_line}")
        return True
    except FileNotFoundError:
        print("    ✗ tshark not found — install Wireshark")
        return False

def check_project_structure():
    print("\n[*] Checking project structure...")
    required = [
        "main.py", "verify_setup.py",
        "capture/sniffer.py",
        "parsers/tcp_parser.py",
        "parsers/dns_parser.py",
        "parsers/http_parser.py",
        "parsers/arp_parser.py",
        "detectors/port_scan.py",
        "detectors/brute_force.py",
        "detectors/dns_tunnel.py",
        "db/logger.py",
        "dashboard/app.py",
        "dashboard/layouts.py",
        "dashboard/callbacks.py",
    ]
    all_ok = True
    for f in required:
        if os.path.exists(f):
            print(f"    ✓ {f}")
        else:
            print(f"    ✗ {f} — MISSING")
            all_ok = False
    return all_ok

def check_database():
    print("\n[*] Checking database...")
    try:
        from db.logger import PacketLogger
        logger = PacketLogger("packets.db")
        packets = logger.get_recent_packets(1)
        alerts  = logger.get_recent_alerts(1)
        print(f"    ✓ Database connected — packets.db")
        print(f"    ✓ Packet table accessible")
        print(f"    ✓ Alert table accessible")
        logger.close()
        return True
    except Exception as e:
        print(f"    ✗ Database error: {e}")
        return False

def check_scapy():
    print("\n[*] Testing Scapy packet craft...")
    try:
        from scapy.all import IP, TCP
        pkt = IP(src="192.168.1.1", dst="8.8.8.8") / TCP(dport=80, flags="S")
        print(f"    ✓ Crafted packet: {pkt.summary()}")
        return True
    except Exception as e:
        print(f"    ✗ Scapy error: {e}")
        return False

def main():
    print("=" * 52)
    print("  Network Packet Analyzer — Setup Verification")
    print("=" * 52)

    results = [
        check_python(),
        check_packages(),
        check_tshark(),
        check_project_structure(),
        check_database(),
        check_scapy(),
    ]

    print("\n" + "=" * 52)
    if all(results):
        print("  ✓ ALL CHECKS PASSED — Project is ready!")
    else:
        failed = results.count(False)
        print(f"  ✗ {failed} check(s) failed — see above for fixes")
    print("=" * 52 + "\n")

if __name__ == "__main__":
    main()