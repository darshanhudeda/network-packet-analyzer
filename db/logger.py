import sqlite3
import threading
import datetime

class PacketLogger:
    def __init__(self, db_path="packets.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        with self.lock:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS packets (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts      TEXT,
                    src     TEXT,
                    dst     TEXT,
                    proto   TEXT,
                    sport   INTEGER,
                    dport   INTEGER,
                    size    INTEGER
                );

                CREATE TABLE IF NOT EXISTS alerts (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts      TEXT,
                    src     TEXT,
                    type    TEXT,
                    severity TEXT,
                    detail  TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_packets_ts
                    ON packets(ts);

                CREATE INDEX IF NOT EXISTS idx_alerts_ts
                    ON alerts(ts);
            """)
            self.conn.commit()

    def log_packet(self, src, dst, proto, sport, dport, size):
        ts = datetime.datetime.utcnow().isoformat()
        with self.lock:
            self.conn.execute(
                "INSERT INTO packets VALUES (NULL,?,?,?,?,?,?,?)",
                (ts, src, dst, proto, sport, dport, size)
            )
            self.conn.commit()

    def log_alert(self, src, alert_type, severity, detail):
        ts = datetime.datetime.utcnow().isoformat()
        with self.lock:
            self.conn.execute(
                "INSERT INTO alerts VALUES (NULL,?,?,?,?,?)",
                (ts, src, alert_type, severity, detail)
            )
            self.conn.commit()

    def get_recent_packets(self, limit=100):
        with self.lock:
            cursor = self.conn.execute(
                "SELECT * FROM packets ORDER BY ts DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

    def get_recent_alerts(self, limit=50):
        with self.lock:
            cursor = self.conn.execute(
                "SELECT * FROM alerts ORDER BY ts DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

    def get_protocol_counts(self):
        with self.lock:
            cursor = self.conn.execute(
                "SELECT proto, COUNT(*) as cnt FROM packets GROUP BY proto"
            )
            return cursor.fetchall()

    def get_top_talkers(self, limit=10):
        with self.lock:
            cursor = self.conn.execute(
                """SELECT src, COUNT(*) as cnt FROM packets
                   GROUP BY src ORDER BY cnt DESC LIMIT ?""",
                (limit,)
            )
            return cursor.fetchall()

    def get_traffic_timeseries(self, seconds=60):
        with self.lock:
            cursor = self.conn.execute(
                """SELECT substr(ts,1,19) as t, COUNT(*) as cnt
                   FROM packets
                   WHERE ts >= datetime('now', ? || ' seconds')
                   GROUP BY t ORDER BY t""",
                (f"-{seconds}",)
            )
            return cursor.fetchall()

    def close(self):
        self.conn.close()