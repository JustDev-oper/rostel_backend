from fastapi import APIRouter, Query, HTTPException, Response
from .. import models
from ..schemas import ProjectIn, ProjectUpdate
from ..services.documents import make_csv
from .common import require, filters, page_result
router=APIRouter(prefix='/api/projects',tags=['Инвестиционный навигатор — проекты'])
def check_company(data):
    if data.get('company_id') and not models.exists('companies',data['company_id']): raise HTTPException(422,detail='Company does not exist')
@router.get('')
def list_projects(search:str|None=None,region:str|None=None,industry:str|None=None,stage:str|None=None,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100)):
    w,p=filters(search,{'region':region,'industry':industry,'stage':stage}); rows,total=models.list_rows('projects',w,p,page,page_size);return page_result(rows,total,page,page_size)
@router.post('',status_code=201)
def create_project(payload:ProjectIn): data=payload.model_dump();check_company(data);return models.create_row('projects',data)
@router.get('/export.csv')
def export_projects(): rows,_=models.list_rows('projects',page_size=10000);return Response(make_csv(rows),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=projects.csv'})
@router.get('/{project_id}')
def get_project(project_id:int):return require('projects',project_id)
@router.put('/{project_id}')
def update_project(project_id:int,payload:ProjectUpdate):require('projects',project_id);data=payload.model_dump();check_company(data);return models.update_row('projects',project_id,data)
@router.delete('/{project_id}',status_code=204)
def delete_project(project_id:int):require('projects',project_id);models.delete_row('projects',project_id)
