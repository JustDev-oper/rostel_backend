from fastapi import HTTPException
from .. import models

def require(table: str, row_id: int):
    row = models.get_row(table, row_id)
    if not row: raise HTTPException(404, detail=f"{table.rstrip('s').capitalize()} not found")
    return row

def filters(search: str | None, values: dict[str, str | int | float | bool | None], search_column: str = 'name'):
    where, params = [], []
    if search:
        where.append(f"{search_column} LIKE ?"); params.append(f"%{search}%")
    for column, value in values.items():
        if value is not None:
            where.append(f"{column} = ?"); params.append(value)
    return where, params

def page_result(items, total, page, page_size): return {"items": items, "total": total, "page": page, "page_size": page_size}
