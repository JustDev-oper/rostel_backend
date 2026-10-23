# Экосистема коммерческого блока Ростелекома — Backend

FastAPI + SQLite backend для трёх модулей: радар присутствия, инвестиционный навигатор и калькулятор сделок.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API доступно по `http://127.0.0.1:8000`, Swagger — `/docs`, OpenAPI — `/openapi.json`.

## Возможности

- CRUD для `/api/companies`, `/api/projects`, `/api/deals`, `/api/proposals`;
- фильтры, поиск и пагинация (`page`, `page_size`, максимум 100);
- расчёт минимальной и оптимальной цены: `POST /api/deals/calculate`;
- CSV: `GET /api/{companies|projects|deals|proposals}/export.csv`;
- DOCX коммерческого предложения: `GET /api/proposals/{id}/document.docx`;
- агрегаты для дашборда: `GET /api/stats`.

При первом запуске база создаётся автоматически, а в неё добавляются исключительно демонстрационные записи. Их отличает `is_test_data: true` и уведомление в `/api/stats`.

## Модель расчёта сделки

`base_cost = equipment_cost + service_cost`  
`minimum_price = base_cost × (1 + risk_percent / 100)`  
`optimal_price = base_cost × (1 + (margin_percent + risk_percent) / 100)`

Если задана цена конкурента выше минимума, оптимальная цена не превышает 99% от неё. Расчёт применяется и при создании, и при обновлении сделки.

## Безопасность и развитие

Все значения в SQL передаются параметрами; имена таблиц зафиксированы в allow-list. Параметры среды и будущие секреты находятся вне кода (`.env`, не коммитить). Контракты `CRMConnector` и `TwoFactorProvider` в `app/services/integrations.py` — это только точки расширения: фактических CRM-вызовов, хранения OTP или имитации 2FA нет.

Для production добавьте аутентификацию, миграции, аудит, TLS и ограничение запросов.
