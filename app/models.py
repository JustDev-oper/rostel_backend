from typing import Any
from .database import get_connection

TABLES = {"companies", "projects", "deals", "proposals"}

def _check_table(table: str):
    if table not in TABLES:
        raise ValueError("Unsupported table")

def list_rows(table: str, where: list[str] | None = None, params: list[Any] | None = None, page: int = 1, page_size: int = 20, order_by: str = "id DESC"):
    _check_table(table); where = where or []; params = params or []
    clause = (" WHERE " + " AND ".join(where)) if where else ""
    with get_connection() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM {table}{clause}", params).fetchone()[0]
        rows = conn.execute(f"SELECT * FROM {table}{clause} ORDER BY {order_by} LIMIT ? OFFSET ?", [*params, page_size, (page-1)*page_size]).fetchall()
    return [dict(r) for r in rows], total

def get_row(table: str, row_id: int):
    _check_table(table)
    with get_connection() as conn:
        row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()
    return dict(row) if row else None

def create_row(table: str, data: dict):
    _check_table(table); keys = list(data)
    sql = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join('?' for _ in keys)})"
    with get_connection() as conn:
        cur = conn.execute(sql, [data[k] for k in keys]); row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)

def update_row(table: str, row_id: int, data: dict):
    _check_table(table)
    if not data: return get_row(table, row_id)
    assignments = ", ".join(f"{k} = ?" for k in data)
    with get_connection() as conn:
        conn.execute(f"UPDATE {table} SET {assignments}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", [*data.values(), row_id])
        row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()
    return dict(row) if row else None

def delete_row(table: str, row_id: int):
    _check_table(table)
    with get_connection() as conn:
        return conn.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,)).rowcount > 0

def exists(table: str, row_id: int): return get_row(table, row_id) is not None
