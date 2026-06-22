from scapy.all import IP, DNS, DNSQR

DOMAIN_LENGTH_THRESHOLD = 50

def detect_dns_tunnel(packet, logger):
    """
    Detects DNS tunneling — flags unusually long
    domain names which are used to smuggle data.
    Normal domains are rarely over 50 characters.
    """
    if DNS not in packet:
        return

    # Only look at DNS queries (qr=0)
    if packet[DNS].qr != 0:
        return

    if DNSQR not in packet:
        return

    try:
        query = packet[DNSQR].qname.decode().rstrip(".")
        src   = packet[IP].src if IP in packet else "unknown"

        if len(query) > DOMAIN_LENGTH_THRESHOLD:
            detail = f"Suspicious DNS query length {len(query)} chars: {query[:60]}..."
            print(f"[MEDIUM] DNS TUNNEL detected from {src} — {detail}")
            logger.log_alert(src, "DNS_TUNNEL", "MEDIUM", detail)

    except Exception as e:
        print(f"[!] DNS tunnel detector error: {e}")