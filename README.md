# 🔍 Network Packet Analyzer

A real-time network packet analyzer built in Python that captures live traffic,
decodes protocols, detects threats, and visualizes everything on a live web dashboard.

Built as a cybersecurity portfolio project on Kali Linux.

---

## 📸 Features

- ✅ Live packet capture using Scapy on any network interface
- ✅ Protocol detection — TCP, UDP, DNS, HTTP, ICMP, ARP
- ✅ Threat detection — Port scans, Brute force, DNS tunneling, ARP spoofing
- ✅ Real-time dashboard with live graphs (updates every 2 seconds)
- ✅ SQLite database logging for all packets and alerts
- ✅ Top talkers, protocol breakdown, and alert feed

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Scapy | Packet capture and crafting |
| PyShark | Deep packet inspection |
| Dash + Plotly | Real-time web dashboard |
| SQLite | Packet and alert storage |
| Pandas | Data handling |

---

## 📁 Project Structure
network-packet-analyzer/

├── main.py                  # Entry point

├── verify_setup.py          # Environment checker

├── capture/

│   └── sniffer.py           # Live packet capture engine

├── parsers/

│   ├── tcp_parser.py        # TCP flag decoder

│   ├── dns_parser.py        # DNS query/response parser

│   ├── http_parser.py       # HTTP request parser

│   └── arp_parser.py        # ARP spoof detector

├── detectors/

│   ├── port_scan.py         # SYN flood detection

│   ├── brute_force.py       # Auth brute force detection

│   └── dns_tunnel.py        # DNS tunneling detection

├── db/

│   └── logger.py            # SQLite read/write handler

├── dashboard/

│   ├── app.py               # Dash app setup

│   ├── layouts.py           # Dashboard UI layout

│   └── callbacks.py         # Live update callbacks

└── tests/

---

## ⚙️ Setup & Installation

### Requirements
- Kali Linux (or any Debian-based Linux)
- Python 3.10+
- Wireshark / tshark

### Install

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/network-packet-analyzer.git
cd network-packet-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
python3 verify_setup.py
```

### Run

```bash
sudo /path/to/venv/bin/python3 main.py --iface eth0
```

Then open your browser at **http://localhost:8050**

---

## 🧪 Testing the Detectors

Open a second terminal and run these to trigger alerts:

```bash
# Trigger port scan detection
nmap -sS 127.0.0.1 -p 1-1000

# Trigger DNS detection
dig google.com
dig facebook.com
dig youtube.com

# Generate HTTP traffic
curl http://example.com

# Generate ICMP traffic
ping -c 10 google.com
```

---

## 📊 Dashboard Preview

The dashboard shows:
- **Live traffic graph** — packets per second over 60 second window
- **Protocol pie chart** — breakdown of TCP/UDP/DNS/ICMP/ARP
- **Top talkers** — most active IP addresses
- **Alert feed** — real-time threat alerts with severity levels

---

## 💡 What I Learned

- How network packets are structured at each OSI layer
- How to use Scapy for raw packet capture and crafting
- How sliding window algorithms detect port scans and brute force
- How to build real-time dashboards with Dash and Plotly
- How SQLite handles concurrent reads/writes with threading locks
- How DNS tunneling works and how to detect it

---

## 📄 License

MIT License — free to use and modify.


