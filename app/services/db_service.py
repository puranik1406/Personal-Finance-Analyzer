import sqlite3
import json
from typing import List, Optional, Dict
import os
from app.config import settings
from app.models.schemas import Transaction, AIInsightsResponse

# Extract database path from DATABASE_URL (e.g. sqlite:///./finance.db -> ./finance.db)
db_path = settings.database_url.replace("sqlite:///", "")

def get_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date TEXT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'Other',
            confidence REAL DEFAULT 1.0,
            reason TEXT
        )
    """)
    
    # Create metadata/cache table for AI insights
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def clear_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM cache WHERE key = 'ai_insights'")
    conn.commit()
    conn.close()

def save_transactions(transactions: List[dict]):
    conn = get_connection()
    cursor = conn.cursor()
    
    for tx in transactions:
        cursor.execute("""
            INSERT OR REPLACE INTO transactions (id, date, description, amount, category, confidence, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tx["id"],
            tx.get("date"),
            tx["description"],
            tx["amount"],
            tx.get("category", "Other"),
            tx.get("confidence", 1.0),
            tx.get("reason")
        ))
        
    conn.commit()
    conn.close()

def get_all_transactions() -> List[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, description, amount, category, confidence, reason FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    
    transactions = []
    for r in rows:
        transactions.append(Transaction(
            id=r["id"],
            date=r["date"],
            description=r["description"],
            amount=r["amount"],
            category=r["category"],
            confidence=r["confidence"],
            reason=r["reason"]
        ))
    return transactions

def get_transaction_by_id(tx_id: str) -> Optional[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, description, amount, category, confidence, reason FROM transactions WHERE id = ?", (tx_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Transaction(
            id=row["id"],
            date=row["date"],
            description=row["description"],
            amount=row["amount"],
            category=row["category"],
            confidence=row["confidence"],
            reason=row["reason"]
        )
    return None

def update_transaction_category(tx_id: str, category: str, confidence: float, reason: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET category = ?, confidence = ?, reason = ?
        WHERE id = ?
    """, (category, confidence, reason, tx_id))
    conn.commit()
    conn.close()

def save_ai_insights(insights: AIInsightsResponse):
    conn = get_connection()
    cursor = conn.cursor()
    insights_json = json.dumps(insights.model_dump())
    cursor.execute("""
        INSERT OR REPLACE INTO cache (key, value)
        VALUES ('ai_insights', ?)
    """, (insights_json,))
    conn.commit()
    conn.close()

def get_ai_insights() -> Optional[AIInsightsResponse]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM cache WHERE key = 'ai_insights'")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        data = json.loads(row["value"])
        return AIInsightsResponse(**data)
    return None
