import pytest
import pandas as pd
from data import load_claims_data  # assuming you have this function

def test_data_loads():
    """
    Test that claims data loads correctly from CSV.
    """
    df = load_claims_data()
    assert df is not None, "Data failed to load."
    assert not df.empty, "Dataframe is empty."
    
def test_required_columns_exist():
    """
    Test that all required columns exist in the dataset.
    """
    df = load_claims_data()
    required_columns = [
        'Claim_Type', 'Estimated_Claim_Amount', 'Traffic_Condition',
        'Weather_Condition', 'Vehicle_Type', 'Vehicle_Year',
        'Driver_age', 'License_age'
    ]
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"
