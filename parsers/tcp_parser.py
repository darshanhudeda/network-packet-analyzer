from scapy.all import IP, TCP

TCP_FLAGS = {
    0x001: "FIN",
    0x002: "SYN",
    0x004: "RST",
    0x008: "PSH",
    0x010: "ACK",
    0x012: "SYN-ACK",
    0x014: "RST-ACK",
}

def parse_tcp(packet):
    """Extract TCP layer details from a packet."""
    if IP not in packet or TCP not in packet:
        return None

    flags = packet[TCP].flags
    flag_name = TCP_FLAGS.get(int(flags), str(flags))

    return {
        "src"  : packet[IP].src,
        "dst"  : packet[IP].dst,
        "sport": packet[TCP].sport,
        "dport": packet[TCP].dport,
        "flags": flag_name,
        "size" : len(packet),
    }