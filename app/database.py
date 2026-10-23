import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/rostel.db")

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS companies (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, inn TEXT UNIQUE,
 industry TEXT NOT NULL, region TEXT NOT NULL, revenue REAL DEFAULT 0 CHECK(revenue >= 0),
 growth_percent REAL DEFAULT 0, potential_score INTEGER DEFAULT 0 CHECK(potential_score BETWEEN 0 AND 100),
 is_potential_client INTEGER NOT NULL DEFAULT 1, is_test_data INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS projects (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL,
 region TEXT NOT NULL, industry TEXT NOT NULL, stage TEXT NOT NULL,
 budget REAL DEFAULT 0 CHECK(budget >= 0), it_needs TEXT NOT NULL DEFAULT '', security_needs TEXT NOT NULL DEFAULT '',
 description TEXT NOT NULL DEFAULT '', is_test_data INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS deals (
 id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
 name TEXT NOT NULL, equipment_cost REAL NOT NULL DEFAULT 0 CHECK(equipment_cost >= 0),
 service_cost REAL NOT NULL DEFAULT 0 CHECK(service_cost >= 0), margin_percent REAL NOT NULL DEFAULT 20 CHECK(margin_percent BETWEEN 0 AND 100),
 risk_percent REAL NOT NULL DEFAULT 5 CHECK(risk_percent BETWEEN 0 AND 100), competitor_price REAL, status TEXT NOT NULL DEFAULT 'draft',
 minimum_price REAL NOT NULL DEFAULT 0, optimal_price REAL NOT NULL DEFAULT 0, is_test_data INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS proposals (
 id INTEGER PRIMARY KEY AUTOINCREMENT, deal_id INTEGER NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
 number TEXT NOT NULL UNIQUE, title TEXT NOT NULL, total_price REAL NOT NULL CHECK(total_price >= 0),
 valid_until TEXT, status TEXT NOT NULL DEFAULT 'draft', content TEXT NOT NULL DEFAULT '', is_test_data INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_companies_industry_region ON companies(industry, region);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
CREATE INDEX IF NOT EXISTS idx_projects_region_stage ON projects(region, stage);
CREATE INDEX IF NOT EXISTS idx_projects_company ON projects(company_id);
CREATE INDEX IF NOT EXISTS idx_deals_project_status ON deals(project_id, status);
CREATE INDEX IF NOT EXISTS idx_proposals_deal_status ON proposals(deal_id, status);
"""

@contextmanager
def get_connection():
    path = Path(DATABASE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initialize_database():
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        existing = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
        if existing:
            return
        conn.executemany("""INSERT INTO companies (name, inn, industry, region, revenue, growth_percent, potential_score, is_potential_client, is_test_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)""", [
            ("АО ТестПром", "7701000001", "Промышленность", "Москва", 1250000000, 12.5, 88, 1),
            ("ООО ДемоЛогистика", "7802000002", "Логистика", "Санкт-Петербург", 740000000, 8.2, 76, 1),
            ("ПАО Учебная Энергия", "5403000003", "Энергетика", "Новосибирская область", 3100000000, -2.0, 69, 1),
        ])
        conn.executemany("""INSERT INTO projects (name, company_id, region, industry, stage, budget, it_needs, security_needs, description, is_test_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""", [
            ("Цифровой завод", 1, "Москва", "Промышленность", "ТЭО", 180000000, "IoT, облако, сеть", "SOC, сегментация сети", "Тестовый инвестпроект"),
            ("Модернизация складов", 2, "Санкт-Петербург", "Логистика", "Реализация", 95000000, "Wi-Fi, видеоаналитика", "Видеонаблюдение, СКУД", "Тестовый инвестпроект"),
        ])
        conn.execute("""INSERT INTO deals (project_id,name,equipment_cost,service_cost,margin_percent,risk_percent,status,minimum_price,optimal_price,is_test_data)
        VALUES (1,'Связность цифрового завода',50000000,12000000,22,7,'calculated',68200000,75600000,1)""")
        conn.execute("""INSERT INTO proposals (deal_id,number,title,total_price,valid_until,status,content,is_test_data)
        VALUES (1,'TEST-2026-001','Тестовое коммерческое предложение',75600000,'2026-12-31','draft','Тестовое предложение для демонстрации.',1)""")
