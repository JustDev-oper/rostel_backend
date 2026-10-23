def calculate_pricing(equipment_cost: float, service_cost: float, margin_percent: float, risk_percent: float, competitor_price: float | None = None) -> dict:
    base = equipment_cost + service_cost
    minimum = round(base * (1 + risk_percent / 100), 2)
    optimal = round(base * (1 + (margin_percent + risk_percent) / 100), 2)
    if competitor_price is not None and competitor_price > minimum:
        optimal = round(min(optimal, competitor_price * 0.99), 2)
    return {"base_cost": round(base, 2), "minimum_price": minimum, "optimal_price": max(minimum, optimal)}
