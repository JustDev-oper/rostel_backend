from fastapi import APIRouter
from ..database import get_connection
router=APIRouter(prefix='/api/stats',tags=['Статистика'])
@router.get('')
def stats():
    with get_connection() as c:
        counts={t:c.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in ('companies','projects','deals','proposals')}
        potential=c.execute('SELECT COUNT(*), COALESCE(SUM(revenue),0) FROM companies WHERE is_potential_client=1').fetchone()
        pipeline=c.execute("SELECT COALESCE(SUM(optimal_price),0) FROM deals WHERE status NOT IN ('lost','won')").fetchone()[0]
    return {'entities':counts,'potential_clients':potential[0],'potential_revenue':potential[1],'open_pipeline':pipeline,'demo_data_notice':'Initial records with is_test_data=true are test data.'}
