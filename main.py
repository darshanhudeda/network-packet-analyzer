import argparse
import threading
import sys
from db.logger import PacketLogger
from capture.sniffer import start_sniffer, stop_event
from dashboard.app import create_app

def parse_args():
    p = argparse.ArgumentParser(
        description="Network Packet Analyzer — real-time sniffer + dashboard"
    )
    p.add_argument(
        "--iface",
        default="eth0",
        help="Network interface to capture on (default: eth0)"
    )
    p.add_argument(
        "--filter",
        default="",
        help="BPF filter string e.g. 'tcp port 80' (default: capture all)"
    )
    p.add_argument(
        "--port",
        default=8050,
        type=int,
        help="Dashboard port (default: 8050)"
    )
    p.add_argument(
        "--db",
        default="packets.db",
        help="SQLite database file (default: packets.db)"
    )
    return p.parse_args()


def main():
    args = parse_args()

    # ── 1. Set up database ────────────────────────────
    print(f"[*] Initializing database: {args.db}")
    logger = PacketLogger(args.db)

    # ── 2. Start sniffer in background thread ─────────
    print(f"[*] Starting sniffer on interface: {args.iface}")
    sniffer_thread = threading.Thread(
        target=start_sniffer,
        args=(args.iface, args.filter, logger),
        daemon=True,
        name="sniffer-thread"
    )
    sniffer_thread.start()

    # ── 3. Start dashboard ────────────────────────────
    print(f"[*] Dashboard starting at http://localhost:{args.port}")
    print(f"[*] Open your browser and go to: http://localhost:{args.port}")
    print(f"[*] Press Ctrl+C to stop\n")

    app = create_app(logger)

    try:
        app.run(
            host="0.0.0.0",
            port=args.port,
            debug=False
        )
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        stop_event.set()
        logger.close()
        sys.exit(0)


if __name__ == "__main__":
    main()