from fastapi import APIRouter, HTTPException, status
from app.models.schemas import FinancialSummaryResponse
from app.services import db_service
from collections import defaultdict

router = APIRouter(prefix="/api", tags=["Summary"])

@router.get("/summary", response_model=FinancialSummaryResponse)
async def get_financial_summary():
    """
    Computes mathematical summary statistics (Income, Expenses, Savings, Top Category)
    from all transactions currently stored in the SQLite database.
    """
    try:
        transactions = db_service.get_all_transactions()
        
        if not transactions:
            return FinancialSummaryResponse(
                total_income=0.0,
                total_expenses=0.0,
                savings=0.0,
                top_spending_category="None",
                category_wise_totals={}
            )
            
        total_income = 0.0
        total_expenses = 0.0
        category_totals = defaultdict(float)
        
        for tx in transactions:
            amount = tx.amount
            category = tx.category
            
            if amount > 0:
                total_income += amount
                # We can also track income categories if needed, but normally income goes to income
                category_totals[category] += amount
            else:
                abs_amount = abs(amount)
                total_expenses += abs_amount
                category_totals[category] += abs_amount
                
        savings = total_income - total_expenses
        
        # Determine Top Spending Category (exclude 'Income' from spending categories)
        spending_categories = {cat: val for cat, val in category_totals.items() if cat != "Income"}
        
        if spending_categories:
            top_spending_category = max(spending_categories, key=spending_categories.get)
        else:
            top_spending_category = "None"
            
        return FinancialSummaryResponse(
            total_income=round(total_income, 2),
            total_expenses=round(total_expenses, 2),
            savings=round(savings, 2),
            top_spending_category=top_spending_category,
            category_wise_totals={cat: round(val, 2) for cat, val in category_totals.items()}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute financial summary: {str(e)}"
        )
