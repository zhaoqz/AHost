import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from src.config import config
from src.utils.logger import logger

class Database:
    def __init__(self):
        self.db_path = config.db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self._get_connection()
        cursor = conn.cursor()
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                view_count INTEGER DEFAULT 0,
                author TEXT
            )
        """)
        
        # Check if author column exists (for migration)
        cursor.execute("PRAGMA table_info(apps)")
        columns = [info[1] for info in cursor.fetchall()]
        if "author" not in columns:
            cursor.execute("ALTER TABLE apps ADD COLUMN author TEXT")
            
        conn.commit()
        conn.close()
        logger.info("Database initialized")

    def create_app(self, slug: str, name: str, description: str, author: str = None) -> int:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO apps (slug, name, description, author, created_at) VALUES (?, ?, ?, ?, ?)",
                (slug, name, description, author, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            logger.error(f"App with slug {slug} already exists")
            raise ValueError(f"App with slug {slug} already exists")
        finally:
            conn.close()

    def update_app(self, slug: str, name: str, description: str, author: str = None):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE apps SET name = ?, description = ?, author = ? WHERE slug = ?",
                (name, description, author, slug)
            )
            conn.commit()
        finally:
            conn.close()

    def get_app(self, slug: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apps WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def increment_view_count(self, slug: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE apps SET view_count = view_count + 1 WHERE slug = ?", (slug,))
        conn.commit()
        conn.close()

    def list_apps(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apps ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

db = Database()
