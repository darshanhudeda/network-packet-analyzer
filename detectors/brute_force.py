from collections import defaultdict
import time
from scapy.all import IP, TCP

# Track connection attempts per src IP per port
conn_log = defaultdict(list)
WINDOW_SECONDS = 60
THRESHOLD = 10
WATCHED_PORTS = {22, 21, 3389, 23}  # SSH, FTP, RDP, Telnet

def detect_brute_force(packet, logger):
    """
    Detects brute force — flags any IP making more than
    10 connection attempts to auth ports within 60 seconds.
    """
    if IP not in packet or TCP not in packet:
        return

    dport = packet[TCP].dport
    if dport not in WATCHED_PORTS:
        return

    # Only SYN packets = new connection attempts
    if packet[TCP].flags != 0x002:
        return

    src = packet[IP].src
    key = f"{src}:{dport}"
    now = time.time()

    conn_log[key] = [t for t in conn_log[key] if now - t < WINDOW_SECONDS]
    conn_log[key].append(now)

    if len(conn_log[key]) > THRESHOLD:
        port_name = {22:"SSH", 21:"FTP", 3389:"RDP", 23:"Telnet"}[dport]
        detail = f"{len(conn_log[key])} attempts to {port_name} (port {dport}) in {WINDOW_SECONDS}s"
        print(f"[HIGH] BRUTE FORCE detected from {src} — {detail}")
        logger.log_alert(src, "BRUTE_FORCE", "HIGH", detail)
        conn_log[key] = []