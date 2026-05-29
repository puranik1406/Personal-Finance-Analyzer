from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.schemas import Transaction, TransactionCategorizeRequest, TransactionCategorizeResponse
from app.services import db_service
from app.services.ollama_service import ollama_service

router = APIRouter(prefix="/api", tags=["Categorize"])

@router.post("/categorize", response_model=List[Transaction])
async def categorize_transactions(request: Optional[TransactionCategorizeRequest] = None):
    """
    Triggers local Gemma AI inference via Ollama to categorize transactions.
    If no transaction IDs are provided, categorizes all stored transactions.
    """
    try:
        if request and request.transaction_ids:
            # Categorize specific transactions
            txs_to_process = []
            for tx_id in request.transaction_ids:
                tx = db_service.get_transaction_by_id(tx_id)
                if tx:
                    txs_to_process.append(tx)
        else:
            # Categorize all stored transactions
            txs_to_process = db_service.get_all_transactions()
            
        if not txs_to_process:
            return []
            
        updated_transactions = []
        
        for tx in txs_to_process:
            # Perform local inference
            result = ollama_service.categorize_transaction(
                description=tx.description,
                amount=tx.amount
            )
            
            category = result.get("category", "Other")
            confidence = result.get("confidence", 1.0)
            reason = result.get("reason", "Local analysis")
            
            # Save categorization to SQLite
            db_service.update_transaction_category(
                tx_id=tx.id,
                category=category,
                confidence=confidence,
                reason=reason
            )
            
            # Append updated model
            updated_tx = db_service.get_transaction_by_id(tx.id)
            if updated_tx:
                updated_transactions.append(updated_tx)
                
        return updated_transactions
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during categorization: {str(e)}"
        )
