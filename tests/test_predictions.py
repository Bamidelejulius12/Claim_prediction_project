import pytest
import pandas as pd
from models import load_model
from predictions import predict  # assuming you have a wrapper function

def test_predictions_function():
    """
    Test the prediction wrapper function from predictions.py
    """
    model = load_model()
    
    sample_input = pd.DataFrame({
        'Claim_Type': ['fire'],
        'Estimated_Claim_Amount': [12000.0],
        'Traffic_Condition': ['Low'],
        'Weather_Condition': ['Foggy'],
        'Vehicle_Type': ['Hatchback'],
        'Vehicle_Year': [2012],
        'Driver_age': [36],
        'License_age': [15]
    })
    
    output = predict(model, sample_input)
    
    assert output is not None, "Predictions wrapper returned None."
    assert isinstance(output, (float, int)), "Prediction output must be numeric."
