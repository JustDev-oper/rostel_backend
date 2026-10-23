from fastapi import APIRouter, Query, Response
from .. import models
from ..schemas import CompanyIn, CompanyUpdate
from ..services.documents import make_csv
from .common import require, filters, page_result
router = APIRouter(prefix='/api/companies', tags=['Радар присутствия — компании'])

@router.get('')
def list_companies(search: str|None=None, industry: str|None=None, region: str|None=None, potential_only: bool|None=None, page: int=Query(1,ge=1), page_size: int=Query(20,ge=1,le=100)):
    w,p=filters(search, {'industry':industry,'region':region,'is_potential_client':potential_only}); rows,total=models.list_rows('companies',w,p,page,page_size); return page_result(rows,total,page,page_size)
@router.post('', status_code=201)
def create_company(payload: CompanyIn): return models.create_row('companies', payload.model_dump())
@router.get('/export.csv')
def export_companies():
    rows,_=models.list_rows('companies',page_size=10000); return Response(make_csv(rows),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=companies.csv'})
@router.get('/{company_id}')
def get_company(company_id:int): return require('companies',company_id)
@router.put('/{company_id}')
def update_company(company_id:int,payload:CompanyUpdate): require('companies',company_id); return models.update_row('companies',company_id,payload.model_dump())
@router.delete('/{company_id}',status_code=204)
def delete_company(company_id:int): require('companies',company_id); models.delete_row('companies',company_id)
