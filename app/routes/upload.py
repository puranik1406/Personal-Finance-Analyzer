from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
from app.utilities.helpers import parse_transactions_csv
from app.services import db_service
from app.models.schemas import Transaction

router = APIRouter(prefix="/api", tags=["Upload"])

@router.post("/upload", response_model=List[Transaction])
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts CSV bank statements, parses transactions using Pandas,
    and stores them in the local SQLite database.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only CSV files are supported."
        )
        
    try:
        content = await file.read()
        parsed_txs = parse_transactions_csv(content)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while parsing the file: {str(e)}"
        )
        
    try:
        # Clear database session for new upload
        db_service.clear_all_transactions()
        
        # Save transactions to SQLite db
        db_service.save_transactions(parsed_txs)
        
        # Retrieve freshly stored transactions from DB to match return schema
        stored_txs = db_service.get_all_transactions()
        return stored_txs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save parsed transactions to local database: {str(e)}"
        )
