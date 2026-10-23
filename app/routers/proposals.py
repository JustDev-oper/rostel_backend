from fastapi import APIRouter, HTTPException, Query, Response
from .. import models
from ..schemas import ProposalIn, ProposalUpdate
from ..services.documents import make_csv, make_proposal_docx
from .common import require, filters, page_result
router=APIRouter(prefix='/api/proposals',tags=['Коммерческие предложения'])
def check(data):
    if not models.exists('deals',data['deal_id']):raise HTTPException(422,detail='Deal does not exist')
    if data.get('valid_until'):data['valid_until']=str(data['valid_until'])
    return data
@router.get('')
def list_proposals(search:str|None=None,status:str|None=None,deal_id:int|None=None,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100)):
    w,p=filters(search,{'status':status,'deal_id':deal_id}, 'title');rows,total=models.list_rows('proposals',w,p,page,page_size);return page_result(rows,total,page,page_size)
@router.post('',status_code=201)
def create_proposal(payload:ProposalIn):return models.create_row('proposals',check(payload.model_dump()))
@router.get('/export.csv')
def export_proposals():rows,_=models.list_rows('proposals',page_size=10000);return Response(make_csv(rows),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=proposals.csv'})
@router.get('/{proposal_id}/document.docx')
def document(proposal_id:int):
    proposal=require('proposals',proposal_id);deal=models.get_row('deals',proposal['deal_id']);return Response(make_proposal_docx(proposal,deal),media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',headers={'Content-Disposition':f"attachment; filename={proposal['number']}.docx"})
@router.get('/{proposal_id}')
def get_proposal(proposal_id:int):return require('proposals',proposal_id)
@router.put('/{proposal_id}')
def update_proposal(proposal_id:int,payload:ProposalUpdate):require('proposals',proposal_id);return models.update_row('proposals',proposal_id,check(payload.model_dump()))
@router.delete('/{proposal_id}',status_code=204)
def delete_proposal(proposal_id:int):require('proposals',proposal_id);models.delete_row('proposals',proposal_id)
