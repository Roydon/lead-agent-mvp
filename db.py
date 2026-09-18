"""SQLite storage for classified leads."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = "leads.db"

AGENTS = ["Priya Sharma", "Alex Kim"]

SAMPLE_LEADS = [
    {
        "sender": "raj.metals@buildersupply.co",
        "text": (
            "Hi, we need a quote for 20 metric tons of hot-rolled steel coil, "
            "delivered to our Pune warehouse by end of next month. Please send "
            "pricing and lead time."
        ),
        "assigned_agent": "Priya Sharma",
    },
    {
        "sender": "j.okafor@primeinvest.com",
        "text": (
            "Looking for a 3-bedroom apartment in a good school district, "
            "budget up to $450k. Can someone send me current listings that "
            "match?"
        ),
        "assigned_agent": "Alex Kim",
    },
    {
        "sender": "unhappy.buyer@example.com",
        "text": (
            "The copper shipment I received yesterday is short by almost 2 "
            "tons compared to the invoice. This is holding up our production "
            "line — I need this resolved today."
        ),
        "assigned_agent": "Priya Sharma",
    },
    {
        "sender": "newsletter@randomdeals.biz",
        "text": (
            "CONGRATULATIONS! You've been selected for a FREE cruise giveaway! "
            "Click here to claim your prize before it expires!!!"
        ),
        "assigned_agent": "Alex Kim",
    },
    {
        "sender": "m.torres@torresrealty.net",
        "text": (
            "Do you handle commercial real estate listings as well as "
            "residential? We're scouting retail space in the downtown area "
            "and want to know if that's something you support."
        ),
        "assigned_agent": "Alex Kim",
    },
]


@contextmanager
def _connect(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DB_PATH) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                sender TEXT,
                raw_text TEXT NOT NULL,
                division TEXT,
                category TEXT,
                urgency TEXT,
                draft_response TEXT,
                assigned_agent TEXT
            )
            """
        )


def insert_lead(
    raw_text: str,
    classification: dict,
    sender: str = "",
    assigned_agent: str | None = None,
    db_path: str = DB_PATH,
) -> int:
    if assigned_agent is None:
        assigned_agent = AGENTS[0]
    with _connect(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO leads
                (created_at, sender, raw_text, division, category, urgency,
                 draft_response, assigned_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                sender,
                raw_text,
                classification.get("division"),
                classification.get("category"),
                classification.get("urgency"),
                classification.get("draft_response"),
                assigned_agent,
            ),
        )
        return cur.lastrowid


def get_leads(assigned_agent: str | None = None, db_path: str = DB_PATH) -> list[dict]:
    with _connect(db_path) as conn:
        if assigned_agent:
            rows = conn.execute(
                "SELECT * FROM leads WHERE assigned_agent = ? ORDER BY id DESC",
                (assigned_agent,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


def count_leads(db_path: str = DB_PATH) -> int:
    with _connect(db_path) as conn:
        return conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]


def seed_if_empty(classify_fn, db_path: str = DB_PATH) -> None:
    """Seed the DB with the 5 sample leads, classifying each via classify_fn,
    unless leads already exist."""
    init_db(db_path)
    if count_leads(db_path) > 0:
        return
    for lead in SAMPLE_LEADS:
        classification = classify_fn(lead["text"], sender=lead["sender"])
        insert_lead(
            lead["text"],
            classification,
            sender=lead["sender"],
            assigned_agent=lead["assigned_agent"],
            db_path=db_path,
        )
