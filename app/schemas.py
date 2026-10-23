from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class ORM(BaseModel): model_config = ConfigDict(from_attributes=True)
class Page(BaseModel): items: list[dict]; total: int; page: int; page_size: int
class CompanyIn(BaseModel):
    name: str = Field(min_length=2, max_length=200); inn: str | None = Field(None, pattern=r"^\d{10}(\d{2})?$")
    industry: str = Field(min_length=2, max_length=100); region: str = Field(min_length=2, max_length=100)
    revenue: float = Field(0, ge=0); growth_percent: float = 0; potential_score: int = Field(0, ge=0, le=100); is_potential_client: bool = True; is_test_data: bool = False
class CompanyUpdate(CompanyIn): pass
class ProjectIn(BaseModel):
    name: str = Field(min_length=2, max_length=200); company_id: int | None = Field(None, gt=0); region: str = Field(min_length=2, max_length=100); industry: str = Field(min_length=2, max_length=100)
    stage: Literal['Идея','ТЭО','Проектирование','Реализация','Завершён']; budget: float = Field(0, ge=0); it_needs: str = ''; security_needs: str = ''; description: str = ''; is_test_data: bool = False
class ProjectUpdate(ProjectIn): pass
class DealIn(BaseModel):
    project_id: int | None = Field(None, gt=0); name: str = Field(min_length=2, max_length=200); equipment_cost: float = Field(0, ge=0); service_cost: float = Field(0, ge=0)
    margin_percent: float = Field(20, ge=0, le=100); risk_percent: float = Field(5, ge=0, le=100); competitor_price: float | None = Field(None, ge=0); status: Literal['draft','calculated','offered','won','lost'] = 'draft'; is_test_data: bool = False
class DealUpdate(DealIn): pass
class ProposalIn(BaseModel):
    deal_id: int = Field(gt=0); number: str = Field(min_length=3, max_length=50); title: str = Field(min_length=2, max_length=200); total_price: float = Field(ge=0)
    valid_until: date | None = None; status: Literal['draft','sent','accepted','rejected','expired'] = 'draft'; content: str = ''; is_test_data: bool = False
class ProposalUpdate(ProposalIn): pass
