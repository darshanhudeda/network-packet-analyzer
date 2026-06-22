from scapy.all import IP, TCP, Raw

def parse_http(packet):
    """
    Extract HTTP request details from raw TCP payload.
    Works on port 80 traffic without extra libraries.
    """
    if TCP not in packet or Raw not in packet:
        return None

    dport = packet[TCP].dport
    sport = packet[TCP].sport

    if dport != 80 and sport != 80:
        return None

    try:
        payload = packet[Raw].load.decode("utf-8", errors="ignore")

        if not payload.startswith(("GET", "POST", "PUT",
                                   "DELETE", "HEAD", "OPTIONS")):
            return None

        lines  = payload.split("\r\n")
        method = lines[0].split(" ")[0]
        path   = lines[0].split(" ")[1] if len(lines[0].split()) > 1 else "/"

        host = ""
        for line in lines[1:]:
            if line.lower().startswith("host:"):
                host = line.split(":", 1)[1].strip()
                break

        return {
            "src"   : packet[IP].src if IP in packet else "unknown",
            "dst"   : packet[IP].dst if IP in packet else "unknown",
            "method": method,
            "host"  : host,
            "path"  : path,
        }

    except Exception:
        return None