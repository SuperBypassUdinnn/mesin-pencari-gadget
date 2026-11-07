import json
import sqlite3
from typing import Any, Dict, List, Optional

def init_db(db_path: str = "data/gadget.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                url TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT,
                specs_json TEXT,
                content TEXT NOT NULL
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_source ON documents(source);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_category ON documents(category);")
    return conn

def insert_document(conn: sqlite3.Connection, doc: Dict[str, Any]) -> None:
    specs_str = json.dumps(doc.get("specs", {}), ensure_ascii=False)
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO documents 
            (id, title, source, url, category, date, specs_json, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc["id"],
            doc["title"],
            doc["source"],
            doc["url"],
            doc.get("category", "gadget"),
            doc.get("date", ""),
            specs_str,
            doc["content"]
        ))

def get_all_documents(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, source, url, category, date, specs_json, content FROM documents")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "title": row["title"],
            "source": row["source"],
            "url": row["url"],
            "category": row["category"],
            "date": row["date"],
            "specs": json.loads(row["specs_json"] or "{}"),
            "content": row["content"]
        })
    return results

def get_document_by_id(conn: sqlite3.Connection, doc_id: str) -> Optional[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, source, url, category, date, specs_json, content FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "source": row["source"],
        "url": row["url"],
        "category": row["category"],
        "date": row["date"],
        "specs": json.loads(row["specs_json"] or "{}"),
        "content": row["content"]
    }
