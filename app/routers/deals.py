from fastapi import APIRouter, Query, HTTPException, Response
from .. import models
from ..schemas import DealIn, DealUpdate
from ..services.pricing import calculate_pricing
from ..services.documents import make_csv
from .common import require, filters, page_result
router=APIRouter(prefix='/api/deals',tags=['Калькулятор сделок'])
def prepared(data):
    if data.get('project_id') and not models.exists('projects',data['project_id']): raise HTTPException(422,detail='Project does not exist')
    data.update(calculate_pricing(data['equipment_cost'],data['service_cost'],data['margin_percent'],data['risk_percent'],data.get('competitor_price')));return data
@router.get('')
def list_deals(search:str|None=None,status:str|None=None,project_id:int|None=None,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100)):
    w,p=filters(search,{'status':status,'project_id':project_id});rows,total=models.list_rows('deals',w,p,page,page_size);return page_result(rows,total,page,page_size)
@router.post('/calculate')
def preview(payload:DealIn): return calculate_pricing(payload.equipment_cost,payload.service_cost,payload.margin_percent,payload.risk_percent,payload.competitor_price)
@router.post('',status_code=201)
def create_deal(payload:DealIn):return models.create_row('deals',prepared(payload.model_dump()))
@router.get('/export.csv')
def export_deals():rows,_=models.list_rows('deals',page_size=10000);return Response(make_csv(rows),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=deals.csv'})
@router.get('/{deal_id}')
def get_deal(deal_id:int):return require('deals',deal_id)
@router.put('/{deal_id}')
def update_deal(deal_id:int,payload:DealUpdate):require('deals',deal_id);return models.update_row('deals',deal_id,prepared(payload.model_dump()))
@router.delete('/{deal_id}',status_code=204)
def delete_deal(deal_id:int):require('deals',deal_id);models.delete_row('deals',deal_id)
