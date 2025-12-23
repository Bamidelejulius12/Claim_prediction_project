import pandas as pd
from models import load_model, predict_claim

def test_model_prediction():
    model = load_model()

    # Example test input
    test_input = pd.DataFrame([{
        "Claim_Type": "fire",
        "Estimated_Claim_Amount": 10000,
        "Traffic_Condition": "Low",
        "Weather_Condition": "Rainy",
        "Vehicle_Type": "Sedan",
        "Vehicle_Year": 2015,
        "Driver_age": 35,
        "License_age": 10
    }])

    prediction = predict_claim(model, test_input)
    
    # Assert prediction is non-negative
    assert prediction >= 0, "Prediction should be non-negative"

if __name__ == "__main__":
    test_model_prediction()
    print("All tests passed!")
