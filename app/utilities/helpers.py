import pandas as pd
import uuid
import re
import logging
from io import BytesIO
from typing import List, Dict, Any

logger = logging.getLogger("helpers")

def clean_amount(val) -> float:
    """
    Cleans currency strings (e.g. '$1,200.50', '($150.00)', '-$25') and converts to float.
    """
    if pd.isna(val) or val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
        
    s = str(val).strip()
    if not s:
        return 0.0
        
    # Check for parenthesis representing negative values, e.g. (120.00)
    is_negative = False
    if s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1]
        
    # Remove currency symbols, commas, and other non-numeric chars except . and -
    s = re.sub(r"[^\d.-]", "", s)
    
    try:
        amount = float(s)
        if is_negative and amount > 0:
            amount = -amount
        return amount
    except ValueError:
        logger.warning(f"Could not parse amount: {val}. Fallback to 0.0")
        return 0.0

def parse_transactions_csv(content: bytes) -> List[Dict[str, Any]]:
    """
    Parses a bank statement CSV using Pandas.
    Auto-detects Description, Amount, and Date columns.
    Returns a list of parsed transaction dictionaries.
    """
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(BytesIO(content))
    except Exception as e:
        logger.error(f"Failed to read CSV bytes: {e}")
        raise ValueError(f"Invalid CSV file format: {e}")
        
    if df.empty:
        raise ValueError("The uploaded CSV file is empty.")
        
    columns = [col.strip() for col in df.columns]
    df.columns = columns
    
    date_col = None
    desc_col = None
    amount_col = None
    debit_col = None
    credit_col = None
    
    # Try to identify Date column
    date_patterns = ["date", "time", "timestamp", "booking"]
    for col in columns:
        if any(p in col.lower() for p in date_patterns):
            date_col = col
            break
            
    # Try to identify Description column
    desc_patterns = ["description", "name", "payee", "memo", "details", "narrative", "merchant", "title"]
    for col in columns:
        if any(p in col.lower() for p in desc_patterns):
            desc_col = col
            break
            
    # Try to identify Amount column or Debit/Credit columns
    amount_patterns = ["amount", "value", "price", "charge", "total"]
    for col in columns:
        if any(p in col.lower() for p in amount_patterns):
            amount_col = col
            break
            
    if not amount_col:
        # Search for separate Debit and Credit columns
        for col in columns:
            if "debit" in col.lower():
                debit_col = col
            elif "credit" in col.lower():
                credit_col = col
                
    # Fallback to column index mapping if not auto-detected
    if not desc_col:
        # Fallback to column 1 or first text column
        desc_col = columns[1] if len(columns) > 1 else columns[0]
        
    if not amount_col and not (debit_col or credit_col):
        # Fallback to column 2 or last numeric/text column
        amount_col = columns[2] if len(columns) > 2 else columns[-1]
        
    if not date_col:
        # Fallback to column 0
        date_col = columns[0]
        
    logger.info(f"Auto-detected columns: Date='{date_col}', Description='{desc_col}', Amount='{amount_col or (debit_col, credit_col)}'")
    
    transactions = []
    
    for idx, row in df.iterrows():
        # Read description
        desc_val = str(row.get(desc_col, "")).strip()
        if not desc_val or desc_val.lower() == "nan":
            continue  # Skip rows with no description
            
        # Read amount
        amt = 0.0
        if amount_col:
            amt = clean_amount(row.get(amount_col))
        else:
            # Parse split debit/credit
            deb = clean_amount(row.get(debit_col)) if debit_col else 0.0
            cre = clean_amount(row.get(credit_col)) if credit_col else 0.0
            if deb != 0.0:
                # Debit is negative cashflow
                amt = -abs(deb)
            elif cre != 0.0:
                # Credit is positive cashflow
                amt = abs(cre)
                
        # Read date
        dt_val = str(row.get(date_col, "")).strip() if date_col else ""
        if dt_val.lower() == "nan":
            dt_val = ""
            
        transactions.append({
            "id": str(uuid.uuid4()),
            "date": dt_val,
            "description": desc_val,
            "amount": amt,
            "category": "Other",
            "confidence": 1.0,
            "reason": "Direct CSV parsing"
        })
        
    if not transactions:
        raise ValueError("No valid transaction rows could be parsed from the CSV.")
        
    return transactions
