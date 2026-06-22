from collections import defaultdict
import time
from scapy.all import IP, TCP

# Track SYN packets per source IP
syn_log = defaultdict(list)
WINDOW_SECONDS = 10
THRESHOLD = 20

def detect_port_scan(packet, logger):
    """
    Detects port scanning — flags any IP sending
    more than 20 SYN packets within 10 seconds.
    """
    if IP not in packet or TCP not in packet:
        return

    # Only look at SYN packets (flags = 0x002)
    if packet[TCP].flags != 0x002:
        return

    src = packet[IP].src
    now = time.time()

    # Keep only recent entries within the time window
    syn_log[src] = [t for t in syn_log[src] if now - t < WINDOW_SECONDS]
    syn_log[src].append(now)

    if len(syn_log[src]) > THRESHOLD:
        detail = f"{len(syn_log[src])} SYN packets in {WINDOW_SECONDS}s"
        print(f"[HIGH] PORT SCAN detected from {src} — {detail}")
        logger.log_alert(src, "PORT_SCAN", "HIGH", detail)
        # Reset to avoid duplicate alerts
        syn_log[src] = []