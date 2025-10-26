import sqlite3
from contextlib import closing
from typing import Optional, List, Tuple

DEFAULT_DB = "data.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    name TEXT,
    target_price REAL
);

CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY,
    target_id INTEGER NOT NULL,
    price REAL NOT NULL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(target_id) REFERENCES targets(id)
);
"""


class DB:
    def __init__(self, path: str = DEFAULT_DB):
        self.path = path
        with closing(sqlite3.connect(self.path)) as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def add_target(self, url: str, name: Optional[str] = None, target_price: Optional[float] = None) -> int:
        with closing(sqlite3.connect(self.path)) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO targets (url, name, target_price) VALUES (?, ?, ?)", (url, name, target_price))
            conn.commit()
            cur.execute("SELECT id FROM targets WHERE url = ?", (url,))
            row = cur.fetchone()
            return row[0]

    def list_targets(self) -> List[Tuple[int, str, Optional[str], Optional[float]]]:
        with closing(sqlite3.connect(self.path)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, url, name, target_price FROM targets")
            return cur.fetchall()

    def record_price(self, target_id: int, price: float):
        with closing(sqlite3.connect(self.path)) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO prices (target_id, price) VALUES (?, ?)", (target_id, price))
            conn.commit()

    def get_price_history(self, target_id: int):
        with closing(sqlite3.connect(self.path)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT ts, price FROM prices WHERE target_id = ? ORDER BY ts", (target_id,))
            return cur.fetchall()

    def get_last_price(self, target_id: int) -> Optional[float]:
        with closing(sqlite3.connect(self.path)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT price FROM prices WHERE target_id = ? ORDER BY ts DESC LIMIT 1", (target_id,))
            row = cur.fetchone()
            return row[0] if row else None
