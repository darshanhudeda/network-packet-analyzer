from scapy.all import IP, DNS, DNSQR, DNSRR

def parse_dns(packet):
    """Extract DNS query and response details."""
    if DNS not in packet:
        return None

    result = {
        "src"     : packet[IP].src if IP in packet else "unknown",
        "type"    : "query" if packet[DNS].qr == 0 else "response",
        "query"   : None,
        "response": None,
    }

    # DNS query
    if packet[DNS].qr == 0 and DNSQR in packet:
        result["query"] = packet[DNSQR].qname.decode().rstrip(".")

    # DNS response
    if packet[DNS].qr == 1 and packet[DNS].an:
        try:
            result["response"] = packet[DNS].an.rdata
        except Exception:
            result["response"] = "unknown"

    return result