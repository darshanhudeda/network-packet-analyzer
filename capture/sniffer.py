import threading
from scapy.all import sniff, IP, TCP, UDP, DNS, ARP, ICMP
from db.logger import PacketLogger
from detectors.port_scan import detect_port_scan
from detectors.brute_force import detect_brute_force
from detectors.dns_tunnel import detect_dns_tunnel

# Shared stop event so main.py can stop the sniffer cleanly
stop_event = threading.Event()

def process_packet(packet, logger: PacketLogger):
    """Called for every captured packet."""
    try:
        if IP not in packet:
            return

        src   = packet[IP].src
        dst   = packet[IP].dst
        size  = len(packet)
        proto = "OTHER"
        sport = 0
        dport = 0

        # ── Identify protocol ──────────────────────────
        if TCP in packet:
            proto = "TCP"
            sport = packet[TCP].sport
            dport = packet[TCP].dport

        elif UDP in packet:
            proto = "UDP"
            sport = packet[UDP].sport
            dport = packet[UDP].dport

        elif ICMP in packet:
            proto = "ICMP"

        elif ARP in packet:
            proto = "ARP"
            src   = packet[ARP].psrc
            dst   = packet[ARP].pdst

        # ── DNS label ─────────────────────────────────
        if DNS in packet:
            proto = "DNS"

        # ── Log to database ───────────────────────────
        logger.log_packet(src, dst, proto, sport, dport, size)

        # ── Run threat detectors ──────────────────────
        detect_port_scan(packet, logger)
        detect_brute_force(packet, logger)
        detect_dns_tunnel(packet, logger)

    except Exception as e:
        print(f"[!] Packet processing error: {e}")


def start_sniffer(iface: str, bpf_filter: str, logger: PacketLogger):
    """
    Start capturing packets on the given interface.
    Runs until stop_event is set.
    """
    print(f"[*] Sniffer started on interface: {iface}")
    print(f"[*] BPF filter: '{bpf_filter}' (empty = capture all)")

    sniff(
        iface=iface,
        filter=bpf_filter,
        prn=lambda pkt: process_packet(pkt, logger),
        store=False,
        stop_filter=lambda _: stop_event.is_set()
    )

    print("[*] Sniffer stopped.")