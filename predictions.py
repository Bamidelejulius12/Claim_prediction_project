import streamlit as st
import pandas as pd
import numpy as np
from models import load_model


def FNOL_prediction(claims_data):
    st.title("🔮 FNOL Claim Prediction")
    st.markdown("### Predict ultimate claim amount based on incident details")

    # Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Enter Claim Details")

        with st.form("prediction_form"):
            col1a, col1b = st.columns(2)

            with col1a:
                claim_type = st.selectbox(
                    "Claim Type",
                    options=claims_data["Claim_Type"].unique()
                )

                estimated_claim = st.number_input(
                    "Estimated Claim Amount ($)",
                    min_value=0,
                    value=1000,
                    step=100
                )

                traffic_condition = st.selectbox(
                    "Traffic Condition",
                    options=claims_data["Traffic_Condition"].unique()
                )

                weather_condition = st.selectbox(
                    "Weather Condition",
                    options=claims_data["Weather_Condition"].unique()
                )

            with col1b:
                vehicle_type = st.selectbox(
                    "Vehicle Type",
                    options=claims_data["Vehicle_Type"].unique()
                )

                vehicle_year = st.number_input(
                    "Vehicle Year",
                    min_value=1900,
                    max_value=2100,
                    value=2020
                )

                driver_age = st.number_input(
                    "Driver Age",
                    min_value=18,
                    max_value=100,
                    value=35
                )

                license_age = st.number_input(
                    "License Age (years)",
                    min_value=0,
                    max_value=80,
                    value=10
                )

            predict_button = st.form_submit_button(
                "🚀 Predict Ultimate Claim Amount",
                use_container_width=True
            )

    with col2:
        st.subheader("ℹ️ Input Summary")
        st.info(f"""
        **Selected Parameters:**
        - Claim Type: {claim_type}
        - Vehicle Type: {vehicle_type}
        - Traffic: {traffic_condition}
        - Weather: {weather_condition}
        - Driver Age: {driver_age}
        - License Age: {license_age} years
        - Vehicle Year: {vehicle_year}
        - Estimated Claim: ${estimated_claim:,.2f}
        """)

    if predict_button:
        st.markdown("---")
        st.subheader("📊 Prediction Results")

        try:
            # Load model + feature columns
            model, feature_columns = load_model()

            # Raw input (NO manual category expansion here)
            input_data = pd.DataFrame({
                "Claim_Type": [str(claim_type)],
                "Estimated_Claim_Amount": [estimated_claim],
                "Traffic_Condition": [str(traffic_condition)],
                "Weather_Condition": [str(weather_condition)],
                "Vehicle_Type": [str(vehicle_type)],
                "Vehicle_Year": [vehicle_year],
                "Driver_age": [driver_age],
                "License_age": [license_age]
            })

            # One-hot encode exactly as during training
            input_encoded = pd.get_dummies(input_data, drop_first=False)

            # Align feature space with training
            input_encoded = input_encoded.reindex(
                columns=feature_columns,
                fill_value=0
            )

            with st.spinner("Making prediction..."):
                prediction = model.predict(input_encoded)
                predicted_amount = np.expm1(prediction[0])

            col_result1, col_result2, col_result3 = st.columns(3)

            with col_result1:
                st.metric(
                    "Estimated Claim Amount",
                    f"${estimated_claim:,.2f}"
                )

            with col_result2:
                st.metric(
                    "Predicted Ultimate Amount",
                    f"${predicted_amount:,.2f}",
                    f"${predicted_amount - estimated_claim:,.2f}"
                )

            with col_result3:
                variance = ((predicted_amount - estimated_claim) / estimated_claim) * 100
                st.metric(
                    "Variance",
                    f"{variance:+.1f}%"
                )

            st.success("✅ Prediction completed successfully!")

            if predicted_amount > estimated_claim:
                st.warning(
                    "⚠️ Predicted amount is higher than estimated. Additional review may be required."
                )
            else:
                st.info(
                    "💡 Predicted amount is within or below the estimate."
                )

        except Exception as e:
            st.error(f"❌ Error making prediction: {e}")
            st.info("Please check if the model and feature columns are correctly loaded.")
