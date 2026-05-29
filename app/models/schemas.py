from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class TransactionBase(BaseModel):
    date: Optional[str] = None
    description: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: str
    category: str = "Other"
    confidence: float = 1.0
    reason: Optional[str] = None

    class Config:
        from_attributes = True

class TransactionCategorizeRequest(BaseModel):
    transaction_ids: List[str]

class TransactionCategorizeResponse(BaseModel):
    id: str
    category: str
    confidence: float
    reason: Optional[str] = None

class AIInsightsResponse(BaseModel):
    spending_pattern: str = Field(..., description="Spending pattern analysis")
    unusual_spending: str = Field(..., description="Unusual spending observations")
    subscriptions: List[str] = Field(default_factory=list, description="Subscription detection list")
    cost_saving: str = Field(..., description="Cost-saving suggestions")
    summary: str = Field(..., description="Monthly financial summary")

class FinancialSummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    savings: float
    top_spending_category: str
    category_wise_totals: Dict[str, float]
