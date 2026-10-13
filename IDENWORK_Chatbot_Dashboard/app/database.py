"""Tüm SQL işlemleri yalnızca bu dosyada yapılır."""
import sqlite3
from pathlib import Path
from flask import current_app, g

def get_db():
    if 'db' not in g:
        path = current_app.config['DATABASE_URL']
        if path != ':memory:':
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.execute("""CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT DEFAULT '',
            tarih TEXT NOT NULL DEFAULT (datetime('now'))
        )""")
        db.commit()

def lead_ekle(isim, telefon, mesaj=''):
    db = get_db()
    cur = db.execute('INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)', (isim, telefon, mesaj))
    db.commit()
    return cur.lastrowid

def tum_leadler():
    rows = get_db().execute('SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC').fetchall()
    return [dict(row) for row in rows]
