from fastapi import APIRouter, HTTPException, status
from app.models.schemas import AIInsightsResponse
from app.services import db_service
from app.services.ollama_service import ollama_service
from app.routes.summary import get_financial_summary

router = APIRouter(prefix="/api", tags=["Analyze"])

@router.post("/analyze", response_model=AIInsightsResponse)
async def analyze_finances():
    """
    Triggers local Gemma AI inference via Ollama to generate comprehensive
    financial insights (spending patterns, subscriptions, savings recommendations, etc.)
    and caches the result in the local SQLite database.
    """
    try:
        # Get all transactions
        transactions = db_service.get_all_transactions()
        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No transaction data available. Please upload a CSV first."
            )
            
        # Get financial summary
        summary_response = await get_financial_summary()
        summary_dict = summary_response.model_dump()
        
        # Format transactions for AI prompt
        txs_list = []
        for tx in transactions:
            txs_list.append({
                "date": tx.date,
                "description": tx.description,
                "amount": tx.amount,
                "category": tx.category
            })
            
        # Run local Gemma analysis
        insights = ollama_service.analyze_finances(txs_list, summary_dict)
        
        # Cache AI insights in SQLite
        db_service.save_ai_insights(insights)
        
        return insights
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during AI financial analysis: {str(e)}"
        )

@router.get("/analyze", response_model=AIInsightsResponse)
async def get_cached_insights():
    """
    Retrieves the last cached AI Insights from the local SQLite database.
    If no insights are cached, triggers an analysis run automatically.
    """
    try:
        cached = db_service.get_ai_insights()
        if cached:
            return cached
            
        # No cache exists, trigger new analysis
        return await analyze_finances()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cached insights: {str(e)}"
        )
